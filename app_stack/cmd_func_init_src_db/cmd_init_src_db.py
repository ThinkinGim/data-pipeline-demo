import boto3
from botocore.exceptions import ClientError

import json
import os

def init(event, context):

    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager')

    try:
        secret_response = client.get_secret_value(SecretId='srcoraSecret5F1A3316-8BqwkVEoUgXv-0w9zQw')
    except ClientError as e:
        print(e.response)
        print(e.response['Error']['Code'])
    else:
        if 'SecretString' in secret_response:
            secret_data = secret_response['SecretString']
            print(secret_data)

    print('########################## cmd_init_src_db.init')

    return {
        'statusCode': 200,
    }