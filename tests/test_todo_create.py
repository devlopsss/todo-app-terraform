import json
import sys
import os

# Add the function directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 
    '../modules/lambda/functions/todo_create'))

from lambda_function import lambda_handler

def test_create_todo_success():
    event = {
        'requestContext': {
            'authorizer': {
                'sub': 'test-user-123'
            }
        },
        'body': json.dumps({'title': 'Test todo'})
    }
    
    # Mock DynamoDB
    import unittest.mock as mock
    with mock.patch('lambda_function.table') as mock_table:
        mock_table.put_item.return_value = {}
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 201
        body = json.loads(response['body'])
        assert body['message'] == 'Todo created'
        assert body['todo']['title'] == 'Test todo'
        assert body['todo']['userId'] == 'test-user-123'
        assert body['todo']['status'] == 'pending'
        print("✅ test_create_todo_success passed")

def test_create_todo_missing_body():
    event = {
        'requestContext': {
            'authorizer': {
                'sub': 'test-user-123'
            }
        },
        'body': json.dumps({})  # missing title
    }
    
    import unittest.mock as mock
    with mock.patch('lambda_function.table'):
        response = lambda_handler(event, None)
        assert response['statusCode'] == 500
        print("✅ test_create_todo_missing_body passed")

if __name__ == '__main__':
    test_create_todo_success()
    test_create_todo_missing_body()
    print("All tests passed!")
