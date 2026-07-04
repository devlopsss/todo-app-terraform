import json
import sys
import os
import unittest.mock as mock
import importlib.util

# Load module directly by file path — avoids name conflicts
spec = importlib.util.spec_from_file_location(
    "todo_create",
    os.path.join(os.path.dirname(__file__),
    '../modules/lambda/functions/todo_create/lambda_function.py')
)
todo_create = importlib.util.module_from_spec(spec)
spec.loader.exec_module(todo_create)

def test_create_todo_success():
    mock_table = mock.MagicMock()
    mock_table.put_item.return_value = {}

    with mock.patch.object(todo_create, 'get_table', return_value=mock_table):
        event = {
            'requestContext': {'authorizer': {'sub': 'test-user-123'}},
            'body': json.dumps({'title': 'Test todo'})
        }
        response = todo_create.lambda_handler(event, None)
        assert response['statusCode'] == 201
        body = json.loads(response['body'])
        assert body['message'] == 'Todo created'
        assert body['todo']['title'] == 'Test todo'
        assert body['todo']['userId'] == 'test-user-123'
        assert body['todo']['status'] == 'pending'

def test_create_todo_missing_title():
    mock_table = mock.MagicMock()
    with mock.patch.object(todo_create, 'get_table', return_value=mock_table):
        event = {
            'requestContext': {'authorizer': {'sub': 'test-user-123'}},
            'body': json.dumps({})
        }
        response = todo_create.lambda_handler(event, None)
        assert response['statusCode'] == 500
