# Amazon Web Services (AWS) Utilities SDK

## AWS Identity and Access Management (IAM)

The scripts contained in this project are work in progress.

### Introduction

The identity script adds roles, groups and associated access policies. The script uses the [AWS SDK](https://boto3.readthedocs.io/en/latest/) to create relationships between a named group and/or role and it's stated policy file or a pre-existing policy [ARN](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html).

Each policy file, associated to a [role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html) or [group](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_groups.html) requires a valid [AWS account](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) ID to create identities against. The AWS account ID must be added directly to policy file prior to executing the script.

For context, a group can consist of a collection of [users](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html) and also be used to cascade relevant access policies to those users. Users can also assume a role that can temporarily extend their access policies, to include access to new services, or restrict their access. AWS services, e.g., [EC2](https://aws.amazon.com/documentation/ec2/) or [Lambda](https://aws.amazon.com/documentation/lambda/), can also assume roles to perform specific actions stated as part of role specific access policies, e.g., a Lambda script that is allowed to read data from [DynamoDB](https://aws.amazon.com/dynamodb/), etc.

#### Key

Key of the scripted terms.

- `policy_name` - the policy name associated to the statically derived policy file, e.g., `RolesPolicyAdmin`.
- `policy_path` - the policy file path, e.g., `/path/to/data/files/groups/policy-admin.json`.
- `policy_arn` - the pre-existing policy ARN, e.g., `arn:aws:iam::aws:policy/AdministratorAccess`.

### Configuration

Project specific group and role identities can be extended to include more roles, groups and policies.

- [src/iam/groups.json](./src/iam/groups.json) - Role identities.
- [src/iam/roles.json](./src/iam/roles.json) - Group identities.

### Scripts

Tested with `Python 2.7.14`.

#### Generate IAM  identities.
creates role or group policies using python AWS SDK.

```bash
$ pip install boto3 argparse inflect # install required support modules
$ chmod +x ./iam/generate_identities.py
$ python ./iam/generate_identities.py --group --role
```

#### Generate IAM policy JSON.
Creates some very basic JSON to base role or group policies on.


```bash
$ pip install awacs argparse namedtupled # install required support modules
$ chmod +x ./iam/generate_policy.py
$ python ./iam/generate_policy.py --policy [assumed-role, default-role, default-group] # select one option
```

### Documentation

You can generate documentation for the modules included in this project using the following commands.

```bash
$ pip install sphinx # install required support modules
$ cd ./docs
$ # sphinx-apidoc -f -o source/ ../iam # used to create associated *.rst files, already done :)
$ make clean && make html # make module documentation
$ open build/html/index.html # MacOS X
```

## Versioning

This project uses [Semantic Versioning](http://semver.org).

## License

This gem is licensed under the [MIT LICENSE](./MIT-LICENSE).

## Author

Author: [dataday](http://github.com/dataday)
