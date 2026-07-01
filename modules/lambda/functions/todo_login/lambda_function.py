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
        secrets  = get_secrets()
        body     = json.loads(event['body'])
        email    = body['email']
        password = body['password']

        response = cognito.initiate_auth(
            ClientId=secrets['client_id'],
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password,
                'SECRET_HASH': get_secret_hash(email)
            }
        )

        return {
            'statusCode': 200,
            'headers': CORS_HEADERS,
            'body': json.dumps({
                'idToken':      response['AuthenticationResult']['IdToken'],
                'accessToken':  response['AuthenticationResult']['AccessToken'],
                'refreshToken': response['AuthenticationResult']['RefreshToken'],
                'expiresIn':    response['AuthenticationResult']['ExpiresIn']
            })
        }
    except ClientError as e:
        return {
            'statusCode': 401,
            'headers': CORS_HEADERS,
            'body': json.dumps({'message': e.response['Error']['Message']})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': CORS_HEADERS,
            'body': json.dumps({'message': str(e)})
        }
