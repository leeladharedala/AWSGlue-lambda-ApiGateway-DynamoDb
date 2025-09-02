import json
import boto3
import os
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def create_customer(event, context):
    body = json.loads(event['body'])
    item = {
        'id': str(uuid.uuid4()),
        'firstname': body.get('firstname', ''),
        'lastname': body.get('lastname', ''),
        'email': body.get('email', ''),
        'phone': body.get('phone', ''),
        'city': body.get('city', ''),
        'state': body.get('state', ''),
        'country': body.get('country', ''),
        'zipcode': body.get('zipcode', '')

    }
    table.put_item(Item=item)
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Customer created', 'item': item})
    }