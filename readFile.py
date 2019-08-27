import argparse
import boto3
import json
import os
import sys
from botocore.exceptions import ClientError

AWS_ENDPOINT = "https://secretsmanager.us-east-1.amazonaws.com"
SERVICE = "secretsmanager"
REGION = "us-east-1"


def output_to_file(service_secrets, output_file, verbosity):
    if not os.path.exists('output'):
        os.makedirs('output')

    # generate passwords.properties file
    with open(output_file, 'w') as passwords_file:
        for key, value in service_secrets.items():
            # for key, value in secrets.items():
            passwords_file.write("%s=%s\n" % (key, value))

    if verbosity > 0:
        print("saved to " + output_file)


def generate_passwords(services, verbosity):
    # store all the secrets here
    secrets = {}

    session = boto3.session.Session()
    client = session.client(
        service_name=SERVICE,
        region_name=REGION,
        endpoint_url=AWS_ENDPOINT
    )

    for service in services:
        service = service.rstrip()
        if verbosity > 0:
            print(service + "...")

        try:
            get_secret_value_response = client.get_secret_value(SecretId=service.rstrip())
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                print("The requested service " + service + " was not found")
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                print("The request was invalid due to:", e)
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                print("The request had invalid params:", e)
            else:
                print("Unexpected error: %s" % e)
                quit()
        except Exception as e:  # catch all
            print("Unexpected error: %s" % e)
            quit()
        else:
            secret = get_secret_value_response['SecretString']
            secrets.update(json.loads(secret))

    return secrets


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("env", help="environment to get passwords for. int, qa, etc")
    parser.add_argument("-v", "--verbose", type=int, help="increase output verbosity")
    parser.add_argument("-o", "--output_file", help="specify an output file to store keys")
    args = parser.parse_args()

    verbosity = 0
    if args.verbose is not None:
        verbosity = args.verbose

    # read secret config file
    with open('C:/Utility/Learning/K8s/spring-cloud-k8s/aws-secrets/secrets_name.txt', 'r') as secret_config_file:
        services = secret_config_file.readlines()

    if verbosity > 0:
        print("Getting secrets for " + args.env + " environment:")

    service_secrets = generate_passwords(services, verbosity)
    secrets_json = json.dumps(service_secrets)
    print(secrets_json)

    if args.output_file is not None:
        output_to_file(service_secrets, args.output_file, verbosity)


if __name__ == "__main__":
    main(sys.argv[1:])
