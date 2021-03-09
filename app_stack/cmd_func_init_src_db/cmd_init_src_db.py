import boto3
from botocore.exceptions import ClientError
import psycopg2

import json
import os

def init(event, context):

    db_secret_name = os.environ.get('db_secret')

    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager')

    try:
        secret_response = client.get_secret_value(SecretId=db_secret_name)
    except ClientError as e:
        print(e.response)
        print(e.response['Error']['Code'])
    else:
        if 'SecretString' in secret_response:
            secret_data = json.loads(secret_response['SecretString'])
            print("##########################")
            print("host: %s"%secret_data['host'])

            db_conn = psycopg2.connect(
                host=secret_data['host'],
                dbname='postgres',
                user=secret_data['username'],
                password=secret_data['password']
            )
            cur = db_conn.cursor()
            cur.execute("select tablename from pg_catalog.pg_tables;")
            print("########################## executing query")
            print(cur.fetchone())


    print('########################## cmd_init_src_db.init')

    return {
        'statusCode': 200,
    }