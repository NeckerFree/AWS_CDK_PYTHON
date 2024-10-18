from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_apigateway as apigateway,
    aws_lambda as lambda_,
)
from constructs import Construct


class ClientsDatabaseStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create the DynamoDB table for Person
        person_table = dynamodb.Table(
            self,
            "PersonTable",
            table_name="Person",
            partition_key=dynamodb.Attribute(
                name="PersonID", type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
        )
        # Define the Lambda function for Create, Read, Update, Delete (CRUD)
        create_lambda = self.create_lambda_function(
            "CreatePersonLambda", "create_person.lambda_handler", person_table
        )
        read_lambda = self.create_lambda_function(
            "ReadPersonLambda", "read_person.lambda_handler", person_table
        )
        update_lambda = self.create_lambda_function(
            "UpdatePersonLambda", "update_person.lambda_handler", person_table
        )
        delete_lambda = self.create_lambda_function(
            "DeletePersonLambda", "delete_person.lambda_handler", person_table
        )

        # Create API Gateway to expose the CRUD operations
        api = apigateway.RestApi(
            self,
            "PersonApi",
            rest_api_name="Person Service",
            description="Service to manage Person records in DynamoDB.",
        )

        # Define API resources and methods
        person_resource = api.root.add_resource("person")

        # POST /person (Create)
        person_resource.add_method("POST", apigateway.LambdaIntegration(create_lambda))

        # GET /person/{id} (Read)
        person_id_resource = person_resource.add_resource("{id}")
        person_id_resource.add_method("GET", apigateway.LambdaIntegration(read_lambda))

        # PUT /person/{id} (Update)
        person_id_resource.add_method(
            "PUT", apigateway.LambdaIntegration(update_lambda)
        )

        # DELETE /person/{id} (Delete)
        person_id_resource.add_method(
            "DELETE", apigateway.LambdaIntegration(delete_lambda)
        )

    # Helper method to create Lambda functions
    def create_lambda_function(self, id, handler, table):
        return lambda_.Function(
            self,
            id,
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler=handler,
            code=lambda_.Code.from_asset(
                "lambda"
            ),  # Directory containing the Lambda function code
            environment={"TABLE_NAME": table.table_name},
        )
