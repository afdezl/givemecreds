#!/usr/bin/env python

from __future__ import print_function
from os.path import expanduser

import argparse
import boto3
import ConfigParser
import yaml
import os


# SESSION CONFIG location relative to this script
SESSION_CONFIG_LOCATION = "sessionconfig.yml"

# AWS CONFIG file location relative to the current user
AWS_CONFIG_LOCATION = "~/.aws/config"

# Define required sessionconfig variables
REQUISITES = {
    "account": True,
    "role": True,
    "source_profile": True,
    "target_profile": False
}


class RequiredParameterException(Exception):
    "Exception is raised when a required parameter is missing from the config"


def load_config(session_name, location=SESSION_CONFIG_LOCATION):
    with open(os.path.join(os.path.dirname(__file__), location), 'r') as f:
        config = yaml.load(f)
    return config["sessions"][session_name]


def check_config(config):
    for item, opt in REQUISITES.items():
        if item not in config and opt is True:
            raise RequiredParameterException(
                "{item} needs to be specified in the configuration!".format(
                    item=item))


def arn(account, role):
    return "arn:aws:iam::{account}:role/{role}".format(
        account=account,
        role=role)


def generate_credentials(arn, session_name, profile):
    os.environ["AWS_DEFAULT_PROFILE"] = profile
    sts_client = boto3.client('sts')
    response = sts_client.assume_role(
        RoleArn=arn,
        RoleSessionName=session_name)
    os.environ["AWS_DEFAULT_PROFILE"] = ""
    return response["Credentials"]


def replace_aws_config(profile, credentials, aws_config=AWS_CONFIG_LOCATION):
    config = ConfigParser.SafeConfigParser()
    config.read(os.path.abspath(expanduser(aws_config)))
    config.set(
        "profile " + profile,
        "aws_access_key_id",
        credentials["AccessKeyId"])
    config.set(
        "profile " + profile,
        "aws_secret_access_key",
        credentials["SecretAccessKey"])
    config.set(
        "profile " + profile,
        "aws_session_token",
        credentials["SessionToken"])

    with open(os.path.abspath(expanduser(aws_config)), 'wb') as configfile:
        config.write(configfile)


def main(args):
    config = load_config(args.session)
    check_config(config)
    credentials = generate_credentials(
        arn(config["account"], config["role"]),
        config.get("target_profile", "temp_profile"),
        config["source_profile"])
    if config.get("target_profile"):
        replace_aws_config(
            config["target_profile"],
            credentials)
        print(
            "Credentials set for profile {profile}".format(
                profile=config["target_profile"]))
    else:
        print(
            "No target profile found, credentials are as follows:\n{}".format(
                credentials
            ))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        'session', type=str, help="session name")
    args = parser.parse_args()
    main(args)
