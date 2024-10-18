import os
import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    person_id = event['pathParameters']['id']

    response = table.get_item(
        Key={
            'PersonID': person_id
        }
    )
    
    item = response.get('Item', None)
    
    if item:
        return {
            'statusCode': 200,
            'body': json.dumps(item)
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Person not found'})
        }
