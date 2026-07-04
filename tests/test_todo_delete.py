import json
import sys
import os
import unittest.mock as mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__),
    '../modules/lambda/functions/todo_delete'))

def test_delete_todo_success():
    mock_table = mock.MagicMock()
    mock_table.delete_item.return_value = {}

    with mock.patch('lambda_function.get_table', return_value=mock_table):
        from lambda_function import lambda_handler
        event = {
            'requestContext': {'authorizer': {'sub': 'test-user-123'}},
            'pathParameters': {'todoId': 'abc-123'}
        }
        response = lambda_handler(event, None)

        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert 'deleted successfully' in body['message']
        print("✅ test_delete_todo_success passed")

if __name__ == '__main__':
    test_delete_todo_success()
    print("All tests passed!")
