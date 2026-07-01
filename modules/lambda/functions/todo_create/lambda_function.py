import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('todo-app-table')

CORS_HEADERS = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type,Authorization',
    'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
}

def lambda_handler(event, context):
    try:
        user_id = event['requestContext']['authorizer']['sub']
        body = json.loads(event['body'])

        item = {
            'userId': user_id,
            'todoId': str(uuid.uuid4()),
            'title': body['title'],
            'status': 'pending',
            'createdAt': datetime.utcnow().isoformat()
        }

        table.put_item(Item=item)

        return {
            'statusCode': 201,
            'headers': CORS_HEADERS,
            'body': json.dumps({'message': 'Todo created', 'todo': item})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': CORS_HEADERS,
            'body': json.dumps({'message': str(e)})
        }
