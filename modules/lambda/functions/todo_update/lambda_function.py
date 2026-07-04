import json
import boto3

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
        todo_id = event['pathParameters']['todoId']
        body = json.loads(event['body'])

        response = get_table().update_item(
            Key={'userId': user_id, 'todoId': todo_id},
            UpdateExpression='SET #t = :title, #s = :status',
            ExpressionAttributeNames={'#t': 'title', '#s': 'status'},
            ExpressionAttributeValues={
                ':title': body.get('title'),
                ':status': body.get('status')
            },
            ReturnValues='ALL_NEW'
        )

        return {
            'statusCode': 200,
            'headers': CORS_HEADERS,
            'body': json.dumps({'updated': response['Attributes']})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': CORS_HEADERS,
            'body': json.dumps({'message': str(e)})
        }
