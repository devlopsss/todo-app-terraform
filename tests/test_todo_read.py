import json
import sys
import os
import unittest.mock as mock
import importlib.util

spec = importlib.util.spec_from_file_location(
    "todo_read",
    os.path.join(os.path.dirname(__file__),
    '../modules/lambda/functions/todo_read/lambda_function.py')
)
todo_read = importlib.util.module_from_spec(spec)
spec.loader.exec_module(todo_read)

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

    with mock.patch.object(todo_read, 'get_table', return_value=mock_table):
        event = {
            'requestContext': {'authorizer': {'sub': 'test-user-123'}}
        }
        response = todo_read.lambda_handler(event, None)
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert len(body['todos']) == 1
        assert body['todos'][0]['title'] == 'Test todo'

def test_read_todos_empty():
    mock_table = mock.MagicMock()
    mock_table.query.return_value = {'Items': []}

    with mock.patch.object(todo_read, 'get_table', return_value=mock_table):
        event = {
            'requestContext': {'authorizer': {'sub': 'test-user-123'}}
        }
        response = todo_read.lambda_handler(event, None)
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['todos'] == []
