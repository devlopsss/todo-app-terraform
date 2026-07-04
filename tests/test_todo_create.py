import json
import sys
import os
import unittest.mock as mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__),
    '../modules/lambda/functions/todo_create'))

def test_create_todo_success():
    mock_table = mock.MagicMock()
    mock_table.put_item.return_value = {}

    with mock.patch('lambda_function.get_table', return_value=mock_table):
        from lambda_function import lambda_handler
        event = {
            'requestContext': {'authorizer': {'sub': 'test-user-123'}},
            'body': json.dumps({'title': 'Test todo'})
        }
        response = lambda_handler(event, None)

        assert response['statusCode'] == 201
        body = json.loads(response['body'])
        assert body['message'] == 'Todo created'
        assert body['todo']['title'] == 'Test todo'
        assert body['todo']['userId'] == 'test-user-123'
        assert body['todo']['status'] == 'pending'
        print("✅ test_create_todo_success passed")

def test_create_todo_missing_title():
    mock_table = mock.MagicMock()

    with mock.patch('lambda_function.get_table', return_value=mock_table):
        from lambda_function import lambda_handler
        event = {
            'requestContext': {'authorizer': {'sub': 'test-user-123'}},
            'body': json.dumps({})
        }
        response = lambda_handler(event, None)
        assert response['statusCode'] == 500
        print("✅ test_create_todo_missing_title passed")

if __name__ == '__main__':
    test_create_todo_success()
    test_create_todo_missing_title()
    print("All tests passed!")
