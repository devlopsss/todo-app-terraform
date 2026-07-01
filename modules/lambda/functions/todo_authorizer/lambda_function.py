import json
import base64

def lambda_handler(event, context):
    token = event.get('authorizationToken', '')
    method_arn = event['methodArn']

    if token.startswith('Bearer '):
        token = token[7:]

    try:
        parts = token.split('.')
        if len(parts) != 3:
            raise Exception('Invalid token format')

        payload = parts[1]
        payload += '=' * (4 - len(payload) % 4)
        decoded = json.loads(base64.b64decode(payload).decode('utf-8'))

        user_id = decoded.get('sub')
        if not user_id:
            raise Exception('No user ID in token')

        return generate_policy(user_id, 'Allow', method_arn)

    except Exception as e:
        print(f'Authorization failed: {str(e)}')
        return generate_policy('user', 'Deny', method_arn)


def generate_policy(principal_id, effect, resource):
    return {
        'principalId': principal_id,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [{
                'Action': 'execute-api:Invoke',
                'Effect': effect,
                'Resource': resource
            }]
        },
        'context': {'sub': principal_id}
    }
