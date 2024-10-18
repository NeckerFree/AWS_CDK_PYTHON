from aws_cdk import App
# from ec2_vpc_stack import Ec2VpcStack
from dynamo_db import ClientsDatabaseStack

app = App()
#  Ec2VpcStack(app, "vpc")
ClientsDatabaseStack(app, "clients-database")
app.synth()