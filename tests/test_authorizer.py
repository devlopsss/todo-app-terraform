import json
import sys
import os
import base64

sys.path.insert(0, os.path.join(os.path.dirname(__file__),
    '../modules/lambda/functions/todo_authorizer'))

from lambda_function import lambda_handler, generate_policy

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
    response = lambda_handler(event, None)
    assert response['policyDocument']['Statement'][0]['Effect'] == 'Allow'
    assert response['context']['sub'] == 'test-user-123'
    print("✅ test_authorizer_valid_token passed")

def test_authorizer_invalid_token():
    event = {
        'authorizationToken': 'Bearer invalid.token',
        'methodArn': 'arn:aws:execute-api:us-east-1:123:abc/prod/GET/read'
    }
    response = lambda_handler(event, None)
    assert response['policyDocument']['Statement'][0]['Effect'] == 'Deny'
    print("✅ test_authorizer_invalid_token passed")

def test_authorizer_missing_bearer():
    event = {
        'authorizationToken': 'notabearer',
        'methodArn': 'arn:aws:execute-api:us-east-1:123:abc/prod/GET/read'
    }
    response = lambda_handler(event, None)
    assert response['policyDocument']['Statement'][0]['Effect'] == 'Deny'
    print("✅ test_authorizer_missing_bearer passed")

if __name__ == '__main__':
    test_authorizer_valid_token()
    test_authorizer_invalid_token()
    test_authorizer_missing_bearer()
    print("All tests passed!")
