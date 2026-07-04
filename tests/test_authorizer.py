import json
import sys
import os
import base64
import importlib.util

spec = importlib.util.spec_from_file_location(
    "todo_authorizer",
    os.path.join(os.path.dirname(__file__),
    '../modules/lambda/functions/todo_authorizer/lambda_function.py')
)
todo_authorizer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(todo_authorizer)

def make_token(sub):
    payload = base64.b64encode(
        json.dumps({'sub': sub}).encode()
    ).decode().rstrip('=')
    return f"eyJ.{payload}.signature"

def test_authorizer_valid_token():
    token = make_token('test-user-123')
    event = {
        'authorizationToken': f'Bearer {token}',
        'methodArn': 'arn:aws:execute-api:us-east-1:123:abc/prod/GET/read'
    }
    response = todo_authorizer.lambda_handler(event, None)
    assert response['policyDocument']['Statement'][0]['Effect'] == 'Allow'
    assert response['context']['sub'] == 'test-user-123'

def test_authorizer_invalid_token():
    event = {
        'authorizationToken': 'Bearer invalid.token',
        'methodArn': 'arn:aws:execute-api:us-east-1:123:abc/prod/GET/read'
    }
    response = todo_authorizer.lambda_handler(event, None)
    assert response['policyDocument']['Statement'][0]['Effect'] == 'Deny'

def test_authorizer_missing_sub():
    payload = base64.b64encode(
        json.dumps({'email': 'test@test.com'}).encode()
    ).decode().rstrip('=')
    token = f"eyJ.{payload}.signature"
    event = {
        'authorizationToken': f'Bearer {token}',
        'methodArn': 'arn:aws:execute-api:us-east-1:123:abc/prod/GET/read'
    }
    response = todo_authorizer.lambda_handler(event, None)
    assert response['policyDocument']['Statement'][0]['Effect'] == 'Deny'
