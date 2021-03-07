import boto3
from botocore.exceptions import ClientError

import json
import os

def init(event, context):

    print('########################## cmd_init_src_db.init')

    return {
        'statusCode': 200,
    }