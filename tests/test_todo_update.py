import json
import sys
import os
import unittest.mock as mock
import importlib.util

spec = importlib.util.spec_from_file_location(
    "todo_update",
    os.path.join(os.path.dirname(__file__),
    '../modules/lambda/functions/todo_update/lambda_function.py')
)
todo_update = importlib.util.module_from_spec(spec)
spec.loader.exec_module(todo_update)

def test_update_todo_success():
    mock_table = mock.MagicMock()
    mock_table.update_item.return_value = {
        'Attributes': {
            'userId': 'test-user-123',
            'todoId': 'abc-123',
            'title': 'Updated todo',
            'status': 'completed'
        }
    }

    with mock.patch.object(todo_update, 'get_table', return_value=mock_table):
        event = {
            'requestContext': {'authorizer': {'sub': 'test-user-123'}},
            'pathParameters': {'todoId': 'abc-123'},
            'body': json.dumps({'title': 'Updated todo', 'status': 'completed'})
        }
        response = todo_update.lambda_handler(event, None)
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['updated']['title'] == 'Updated todo'
        assert body['updated']['status'] == 'completed'
