import sys

import boto3
import base64
from botocore.exceptions import ClientError

SERVICE_NAME = "secretsmanager"
REGION = "us-east-1"


def get_secret():
    secret_name = "/secret/profile/aws-secrets-app_aws"
    # secret_name = "/secret/profile/application"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name=SERVICE_NAME,
        region_name=REGION
    )

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            raise e
    else:
        if 'SecretString' in get_secret_value_response:
            print(get_secret_value_response)
            secret = get_secret_value_response['SecretString']
            print(secret)
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])


def main(argv):
    get_secret()


if __name__ == "__main__":
    main(sys.argv[1:])
