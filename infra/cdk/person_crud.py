import boto3

# Initialize the DynamoDB resource
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Person")


# Create (Add) a new Person
def create_person(person_id, name, age):
    table.put_item(Item={"PersonID": person_id, "Name": name, "Age": age})
    print(f"Person {person_id} created successfully.")


# Read (Get) a Person by PersonID
def get_person(person_id):
    response = table.get_item(Key={"PersonID": person_id})
    return response.get("Item", None)


# Update an existing Person's data
def update_person(person_id, name=None, age=None):
    update_expression = []
    expression_attribute_values = {}

    if name:
        update_expression.append("Name = :name")
        expression_attribute_values[":name"] = name

    if age:
        update_expression.append("Age = :age")
        expression_attribute_values[":age"] = age

    update_expr = "SET " + ", ".join(update_expression)

    table.update_item(
        Key={"PersonID": person_id},
        UpdateExpression=update_expr,
        ExpressionAttributeValues=expression_attribute_values,
    )
    print(f"Person {person_id} updated successfully.")


# Delete a Person by PersonID
def delete_person(person_id):
    table.delete_item(Key={"PersonID": person_id})
    print(f"Person {person_id} deleted successfully.")
