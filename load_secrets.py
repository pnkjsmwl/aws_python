import argparse
import sys

import boto3
import json
import os
from botocore.exceptions import ClientError

AWS_ENDPOINT = "https://secretsmanager.us-east-1.amazonaws.com"
SERVICE = "secretsmanager"
REGION = "us-east-1"
OUTPUT_FILE = "/etc/config/secrets.json"


def output_to_file(service_secrets, output_file):
    if not os.path.exists('output'):
        os.makedirs('output')

    # generate passwords.properties file
    with open(output_file, 'w') as passwords_file:
        for key, value in service_secrets.items():
            # for key, value in secrets.items():
            passwords_file.write("%s=%s\n" % (key, value))

    print("Secrets saved to " + output_file)


def generate_passwords(services):
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

        try:
            get_secret_value_response = client.get_secret_value(SecretId=service.rstrip())
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                print("The requested service " + service + " was not found")
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                print("The request was invalid due to:", e)
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                print("The request had invalid params:", e)
            elif e.response['Error']['Code'] == 'AccessDeniedException':
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


def create_secrets_list(args):

    secrets_list = [args.prefix + "/" + "application", args.prefix + "/" + args.microservice_name]

    for profile in args.profiles:
        secrets_list.append(args.prefix + "/" + "application" + "_" + profile)
        secrets_list.append(args.prefix + "/" + args.microservice_name + "_" + profile)

    return secrets_list


def main():
    parser = argparse.ArgumentParser('Python script to fetch AWS secrets.')
    parser.add_argument('-pfx', '--prefix',  help='Prefix for the secret', default='/secret')
    parser.add_argument('-msn', '--microservice_name', help='Microservice name', required=True)
    # parser.add_argument('-prf', '--profiles', nargs='+', help='Space separated activated profile')
    parser.add_argument('-prf', '--profiles', type=lambda x: x.split(','), help='Comma separated activated profile')
    args = parser.parse_args()

    print(args.profiles)
    '''
    prefix = input("Enter prefix : ") or "/secret"
    microservice_name = input("Enter service name : ")
    profile = input("Enter profile name : ")

    if not microservice_name:
        raise Exception("Microservice name cannot be null")

    
    
    
    secrets_list = [prefix + "/" + "application",
                    prefix + "/" + "application" + "_" + profile,
                    prefix + "/" + microservice_name,
                    prefix + "/" + microservice_name + "_" + profile]
    '''
    secrets_list = create_secrets_list(args)

    print(secrets_list)

    # read secret config file
    '''with open('C:/Utility/Learning/K8s/spring-cloud-k8s/aws-secrets/secrets_name.txt', 'r') as secret_config_file:
        services = secret_config_file.readlines()
    '''

    service_secrets = generate_passwords(secrets_list)
    secrets_json = json.dumps(service_secrets)
    print(secrets_json)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    with open(OUTPUT_FILE, 'w') as secretDataFile:
        secrets_json = json.dump(service_secrets, secretDataFile)

    # if OUTPUT_FILE is not None:
    #    output_to_file(service_secrets, OUTPUT_FILE)


if __name__ == "__main__":
    main()
