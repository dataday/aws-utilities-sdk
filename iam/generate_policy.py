# -*- coding: utf-8 -*-

import awacs
from awacs.aws import Policy, Allow, Statement, Principal
from awacs.sts import AssumeRole

import argparse
import namedtupled


# PEP 8 formatted code
class GeneratePolicy:
    version = '0.1.0'
    description = 'Generates AWS IAM policy JSON structures.'

    """Class tasked with generating AWS policy JSON structures.

    This class provides basic skeleton JSON for stating AWS policies.
    """

    def __init__(self, arguments):
        """Class initialisation method from arguments.

        :param dict arguments: list of arguments
        :returns: None
        """

        self.account_id = '123456789012'
        self.policy_name = arguments.policy

    def get_policy_name(self):
        """Gets predefined policy name

        :returns: str -- policy name

        >>> print self.get_policy_name()
        assumed-role
        """
        return self.policy_name

    def get_account_id(self):
        """Gets predefined policy name

        :returns: str -- policy name

        >>> print self.get_account_id('admin')
        123456789123
        """
        return self.account_id


    def get_assumed_role(self, params):
        """Generates JSON for a assumed role statement

        :param dict params: list of parameters
        """
        return Policy(
            Statement=[
                Statement(
                    Sid='AssumeRolePrincipalService',
                    Effect=Allow,
                    Action=[AssumeRole],
                    Principal=Principal(
                        'Service', ['ec2.amazonaws.com']
                    )
                ),
                Statement(
                    Sid="AssumeRolePrincipalAWS",
                    Effect=Allow,
                    Action=[AssumeRole],
                    Principal=Principal(
                        'AWS', ["arn:aws:iam::%s:root" % (self.get_account_id())]
                    )
                )
            ]
        )

    def get_default_role(self, params):
        """Generates JSON for a default role statement

        :param dict params: list of parameters
        """
        return Policy(
            Statement=[
                Statement(
                    Effect=Allow,
                    NotAction=[
                        '*'
                    ],
                    Resource=[
                        '*'
                    ]
                )
            ]
        )

    def get_default_group(self, params):
        """Generates JSON for a default group statement

        :param dict params: list of parameters
        """
        return Policy(
            Statement=[
                Statement(
                    Effect=Allow,
                    NotAction=[
                        '*'
                    ],
                    Resource=[
                        '*'
                    ]
                )
            ]
        )

    def main(self):
        """Calls associated template policy name

        :param str arg: template policy name
        :returns: return: -- JSON structure
        """
        # parameters tuple
        params = namedtupled.map({
            'group': ['admin', 'development', 'staff'],
            'role': ['publisher', 'service', 'support']
        })

        # # named policy function
        generate_policy = {
            'assumed-role': self.get_assumed_role,
            'default-role': self.get_default_role,
            'default-group': self.get_default_group
        }.get(self.get_policy_name(), lambda: 'unknown')

        policy = generate_policy(params)

        print(policy.to_json())


def parse_args():
    """Processes command line arguments
    """
    parser = argparse.ArgumentParser(description='Creates IAM policy JSON templates.')
    parser.add_argument('--policy', '-p', help='Policy name', required=True)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    PolicyData = GeneratePolicy(args)
    PolicyData.main()
