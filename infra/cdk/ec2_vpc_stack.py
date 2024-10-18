from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
    )
from constructs import Construct


class Ec2VpcStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = ec2.Vpc(
            self,
            id="MyVpcClass",
            max_azs=3,
            nat_gateways=0,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                   cidr_mask=24,
                   name="PublicSubnet",
                   subnet_type=ec2.SubnetType.PUBLIC
               ),
            ]
        )

# AMI                
        ubuntu_linux = ec2.MachineImage.generic_linux({
            "us-east-1": "ami-0866a3c8686eaeeba"
        })

        security_group = ec2.SecurityGroup(self, "MySecurityGroup",
                                           vpc=vpc,
                                           description="Allow SSH access",
                                           allow_all_outbound=True)
        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Allow SSH access from anywhere")
        # Security Group Ingress Rule
        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "Allow HTTP access from anywhere")


 # Instance Role and SSM Managed Policy
        role = iam.Role(self, "InstanceSSM", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))

        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))
        with open('configure.sh', 'r') as f: user_data_script = f.read()
        # Instance
        instance = ec2.Instance(self, "Instance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ubuntu_linux,
            vpc = vpc,
            security_group = security_group,
            role = role,
            user_data=ec2.UserData.custom(user_data_script)
            )
