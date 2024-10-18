import os
import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    person_id = event['pathParameters']['id']

    table.delete_item(
        Key={
            'PersonID': person_id
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'message': f'Person {person_id} deleted successfully.'})
    }
