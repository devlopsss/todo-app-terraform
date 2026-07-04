import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = None
table = None

def get_table():
    global dynamodb, table
    if table is None:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('todo-app-table')
    return table

CORS_HEADERS = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type,Authorization',
    'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
}

def lambda_handler(event, context):
    try:
        user_id = event['requestContext']['authorizer']['sub']

        response = get_table().query(
            KeyConditionExpression=Key('userId').eq(user_id)
        )

        return {
            'statusCode': 200,
            'headers': CORS_HEADERS,
            'body': json.dumps({'todos': response['Items']})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': CORS_HEADERS,
            'body': json.dumps({'message': str(e)})
        }
