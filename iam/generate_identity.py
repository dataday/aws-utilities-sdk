# -*- coding: utf-8 -*-

import os.path
import json
import logging
import boto3
import argparse
import inflect

pluralise = inflect.engine()


# PEP 8 formatted code
class GenerateIdentity:
    version = '0.1.0'
    description = 'Generates AWS IAM roles and groups and associated policies.'

    """Class tasked with generating AWS identities associated to a valid AWS
    user account.

    This class provides some of the basic methods for generating roles, groups
    and associated policies.

    .. note::

        This class depends on structured JSON data provided via the root level
        'src' directory.
    """
    def __init__(self, arguments):
        """Class initialisation method from arguments.

        :param list arguments: input group and role arguments
        :returns: None
        """
        # assign IAM client and data path
        self.client = boto3.client('iam')
        self.base_path = os.path.dirname(os.path.realpath(__file__))
        self.data_path = self.base_path.replace('bin', 'src')

        # set logging level
        logging.basicConfig(
            # TODO: change to use datetime, apply '.%f' microseconds
            format='%(asctime)s - %(levelname)s:%(message)s',
            datefmt='%m/%d/%YT%I:%M:%S',
            level=logging.INFO
        )

        # create identities tuple
        self.identities = ({
            'group': arguments.group,
            'role': arguments.role
        })

        # add identity, policy name, path and arn
        self.identity = None
        self.policy_name = None
        self.policy_path = None
        self.policy_arn = None

    def plural(self, word):
        """This function pluralises a word.
        This method relies on the 'inflect' package

        :param str word: word to make plural
        :returns: str -- a pluralised word

        >>> print self.plural('role')
        roles
        """
        return pluralise.plural(word)

    def make_path(self, path):
        """Makes a data file path reference absolute.

        :param str path: a data file path reference
        :returns: str -- a absolute data file path
        """
        return "%s/%s.json" % (self.data_path, path)

    def get_data(self, path, as_string=False):
        """Gets data from specified path.

        :param str path: a absolute data file path
        :param bool as_string: flag to return data object as type string
        :returns: str or dict: JSON response data
        :raises: Exception
        """
        if not os.path.isfile(path):
            raise Exception("Path not found: %s" % path)
        data = json.load(open(path))
        return json.dumps(data) if as_string else data

    def get_policy_name(self):
        """Gets predefined policy name

        :returns: str -- policy name

        >>> print self.get_policy_name('admin')
        GroupsPolicyAdmin
        """
        return self.policy_name

    def get_policy_path(self):
        """Gets predefined policy path

        :returns: str -- policy path

        >>> print self.get_policy_path('admin')
        /path/to/data/files/groups/policy-admin.json
        """
        return self.policy_path

    def get_policy_arn(self):
        """Gets predefined policy ARN (AWS)

        :returns: str -- policy ARN

        >>> print self.get_policy_arn('AdministratorAccess')
        arn:aws:iam::aws:policy/AdministratorAccess
        """
        return self.policy_arn

    def get_identity(self):
        """Gets predefined identity type, e.g., 'role' or 'group'

        :returns: str -- identity type
        """
        return self.identity

    def set_identity(self, identity):
        """Sets identity, e.g., 'role' and 'group' data

        :param str identity: identity type, e.g., role
        """
        self.identity = identity

    def set_policy_arn(self, policy):
        """Sets policy ARN (AWS)

        :param str policy: policy ARN
        """
        arn = "arn:aws:iam::aws:policy/%s" % policy
        self.policy_arn = arn

    def set_policy_name(self, name):
        """Sets policy name

        :param str name: policy name
        """
        name = "%sPolicy%s" % (self.get_identity().title(), name.title())
        self.policy_name = name

    def set_policy_path(self, name):
        """Sets policy path from name

        :param str name: policy name
        """
        path = "%s/policy-%s" % (self.plural(self.get_identity()), name)
        self.policy_path = self.make_path(path)

    def generate_role(self, name, policies):
        """Generates AWS role based on policy name and path

        :param str name: associated role name
        :param str policies: AWS access policies associated to the role
        """
        policy_name = self.get_policy_name()
        policy_path = self.get_policy_path()

        # create role
        global_policy_path = policy_path.replace('-' + name, '')

        if os.path.isfile(global_policy_path):
            self.client.create_role(
                RoleName=name,
                AssumeRolePolicyDocument=self.get_data(
                    global_policy_path,
                    True
                )
            )

        logging.info("Created role %s" % name)

        # attach policies to role
        if policies:
            for policy in policies:
                self.set_policy_arn(policy)
                self.client.attach_role_policy(
                    RoleName=name,
                    PolicyArn=self.get_policy_arn()
                )

                logging.info("Added policy %s" % self.get_policy_arn())

        # add custom policy to role
        if os.path.isfile(policy_path):
            policy_data = self.get_data(
                policy_path,
                True
            )

            self.client.put_role_policy(
                RoleName=name,
                PolicyName=policy_name,
                PolicyDocument=policy_data
            )

            logging.info("Added policy %s %s" % (policy_name, policy_path))

    def generate_group(self, name, policies):
        """Generates AWS group based on policy name and path

        :param str name: associated group name
        :param str policies: AWS access policies associated to the group
        """
        policy_name = self.get_policy_name()
        policy_path = self.get_policy_path()

        # create group
        self.client.create_group(GroupName=name)
        logging.info("Created group %s" % name)

        # attach policies to group
        if policies:
            for policy in policies:
                self.set_policy_arn(policy)
                self.client.attach_group_policy(
                    GroupName=name,
                    PolicyArn=self.get_policy_arn()
                )
                logging.info("Added policy %s" % self.get_policy_arn())

        # add custom policy to group
        if os.path.isfile(policy_path):
            policy_data = self.get_data(policy_path, True)
            self.client.put_group_policy(
                GroupName=name,
                PolicyName=policy_name,
                PolicyDocument=policy_data
            )
            logging.info("Added local policy %s %s" % (policy_name, policy_path))

    def main(self):
        """Generates identities from predefined role and group data.
        """
        for identity in self.identities:
            if self.identities[identity]:
                try:

                    # set identity, e.g., 'group' or 'role'
                    self.set_identity(identity)

                    # assign identity file path
                    identity_path = self.make_path(self.plural(self.get_identity()))

                    # get identity data
                    identity_data = self.get_data(identity_path)

                    logging.info("Creating %s from %s" % (identity, identity_path))

                    # set identity options
                    generate_identity = {
                        'role': self.generate_role,
                        'group': self.generate_group
                    }.get(self.get_identity(), lambda: 'unknown')

                    for data in identity_data:
                        for name, policies in data.iteritems():
                            self.set_policy_name(name)
                            self.set_policy_path(name)

                            generate_identity(name, policies)

                    # create identity report
                    generate_report = {
                        'role': self.client.list_roles,
                        'group': self.client.list_groups
                    }.get(self.get_identity(), lambda: 'unknown')

                    logging.info("Reporting on %s" % identity)
                    generate_report()

                except Exception as e:
                    logging.error("%s" % e)

            else:
                logging.info("Skipping %s" % identity)


def parse_args():
    """Processes command line arguments
    """
    parser = argparse.ArgumentParser(description='Generate AWS IAM roles and groups with associated policies.')
    parser.add_argument('--group', action='store_true', help='Creates group identities')
    parser.add_argument('--role', action='store_true', help='Creates role identities')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    IdentityData = GenerateIdentity(args)
    IdentityData.main()
