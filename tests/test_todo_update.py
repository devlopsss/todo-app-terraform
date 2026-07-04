import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__),
    '../modules/lambda/functions/todo_update'))

from lambda_function import lambda_handler

def test_update_todo_success():
    event = {
        'requestContext': {
            'authorizer': {
                'sub': 'test-user-123'
            }
        },
        'pathParameters': {
            'todoId': 'abc-123'
        },
        'body': json.dumps({
            'title': 'Updated todo',
            'status': 'completed'
        })
    }

    import unittest.mock as mock
    with mock.patch('lambda_function.table') as mock_table:
        mock_table.update_item.return_value = {
            'Attributes': {
                'userId': 'test-user-123',
                'todoId': 'abc-123',
                'title': 'Updated todo',
                'status': 'completed'
            }
        }
        response = lambda_handler(event, None)

        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['updated']['title'] == 'Updated todo'
        assert body['updated']['status'] == 'completed'
        print("✅ test_update_todo_success passed")

if __name__ == '__main__':
    test_update_todo_success()
    print("All tests passed!")
