import os
import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    person_id = event['pathParameters']['id']
    body = json.loads(event['body'])
    name = body.get('Name')
    age = body.get('Age')

    update_expression = []
    expression_attribute_values = {}

    if name:
        update_expression.append('Name = :name')
        expression_attribute_values[':name'] = name

    if age:
        update_expression.append('Age = :age')
        expression_attribute_values[':age'] = age

    update_expr = "SET " + ", ".join(update_expression)

    table.update_item(
        Key={
            'PersonID': person_id
        },
        UpdateExpression=update_expr,
        ExpressionAttributeValues=expression_attribute_values
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'message': f'Person {person_id} updated successfully.'})
    }
