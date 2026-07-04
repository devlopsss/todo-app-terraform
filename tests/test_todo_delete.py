import json
import sys
import os
import unittest.mock as mock
import importlib.util

spec = importlib.util.spec_from_file_location(
    "todo_delete",
    os.path.join(os.path.dirname(__file__),
    '../modules/lambda/functions/todo_delete/lambda_function.py')
)
todo_delete = importlib.util.module_from_spec(spec)
spec.loader.exec_module(todo_delete)

def test_delete_todo_success():
    mock_table = mock.MagicMock()
    mock_table.delete_item.return_value = {}

    with mock.patch.object(todo_delete, 'get_table', return_value=mock_table):
        event = {
            'requestContext': {'authorizer': {'sub': 'test-user-123'}},
            'pathParameters': {'todoId': 'abc-123'}
        }
        response = todo_delete.lambda_handler(event, None)
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert 'deleted successfully' in body['message']
