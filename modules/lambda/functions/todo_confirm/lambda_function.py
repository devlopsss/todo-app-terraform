import json
import boto3
import hmac
import hashlib
import base64
import os
from botocore.exceptions import ClientError

cognito        = boto3.client('cognito-idp')
secrets_client = boto3.client('secretsmanager')

_secrets = None

def get_secrets():
    global _secrets
    if _secrets is None:
        response = secrets_client.get_secret_value(
            SecretId=os.environ['SECRET_NAME']
        )
        _secrets = json.loads(response['SecretString'])
    return _secrets

CORS_HEADERS = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type,Authorization',
    'Access-Control-Allow-Methods': 'POST,OPTIONS'
}

def get_secret_hash(username):
    secrets = get_secrets()
    message = username + secrets['client_id']
    dig = hmac.new(
        secrets['client_secret'].encode('utf-8'),
        msg=message.encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    return base64.b64encode(dig).decode()

def lambda_handler(event, context):
    try:
        secrets = get_secrets()
        body    = json.loads(event['body'])
        email   = body['email']
        code    = body['code']

        cognito.confirm_sign_up(
            ClientId=secrets['client_id'],
            Username=email,
            ConfirmationCode=code,
            SecretHash=get_secret_hash(email)
        )

        return {
            'statusCode': 200,
            'headers': CORS_HEADERS,
            'body': json.dumps({'message': 'Account verified successfully'})
        }
    except ClientError as e:
        return {
            'statusCode': 400,
            'headers': CORS_HEADERS,
            'body': json.dumps({'message': e.response['Error']['Message']})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': CORS_HEADERS,
            'body': json.dumps({'message': str(e)})
        }
