import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__),
    '../modules/lambda/functions/todo_delete'))

from lambda_function import lambda_handler

def test_delete_todo_success():
    event = {
        'requestContext': {
            'authorizer': {
                'sub': 'test-user-123'
            }
        },
        'pathParameters': {
            'todoId': 'abc-123'
        }
    }

    import unittest.mock as mock
    with mock.patch('lambda_function.table') as mock_table:
        mock_table.delete_item.return_value = {}
        response = lambda_handler(event, None)

        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert 'deleted successfully' in body['message']
        print("✅ test_delete_todo_success passed")

if __name__ == '__main__':
    test_delete_todo_success()
    print("All tests passed!")
