import json
import boto3

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
        todo_id = event['pathParameters']['todoId']

        table.delete_item(
            Key={'userId': user_id, 'todoId': todo_id}
        )

        return {
            'statusCode': 200,
            'headers': CORS_HEADERS,
            'body': json.dumps({'message': f'Todo {todo_id} deleted successfully'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': CORS_HEADERS,
            'body': json.dumps({'message': str(e)})
        }
