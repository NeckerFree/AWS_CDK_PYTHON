import os
import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    body = json.loads(event['body'])
    person_id = body['PersonID']
    name = body['Name']
    age = body['Age']

    table.put_item(
        Item={
            'PersonID': person_id,
            'Name': name,
            'Age': age
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'message': f'Person {person_id} created successfully.'})
    }
