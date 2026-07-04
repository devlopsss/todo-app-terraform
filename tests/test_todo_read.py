import json
import sys
import os
import unittest.mock as mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__),
    '../modules/lambda/functions/todo_read'))

def test_read_todos_success():
    mock_table = mock.MagicMock()
    mock_table.query.return_value = {
        'Items': [
            {
                'userId': 'test-user-123',
                'todoId': 'abc-123',
                'title': 'Test todo',
                'status': 'pending',
                'createdAt': '2026-06-29T00:00:00'
            }
        ]
    }

    with mock.patch('lambda_function.get_table', return_value=mock_table):
        from lambda_function import lambda_handler
        event = {
            'requestContext': {'authorizer': {'sub': 'test-user-123'}}
        }
        response = lambda_handler(event, None)

        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert len(body['todos']) == 1
        assert body['todos'][0]['title'] == 'Test todo'
        print("✅ test_read_todos_success passed")

def test_read_todos_empty():
    mock_table = mock.MagicMock()
    mock_table.query.return_value = {'Items': []}

    with mock.patch('lambda_function.get_table', return_value=mock_table):
        from lambda_function import lambda_handler
        event = {
            'requestContext': {'authorizer': {'sub': 'test-user-123'}}
        }
        response = lambda_handler(event, None)

        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['todos'] == []
        print("✅ test_read_todos_empty passed")

if __name__ == '__main__':
    test_read_todos_success()
    test_read_todos_empty()
    print("All tests passed!")
