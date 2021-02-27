from aws_cdk import (
    core,
    aws_ec2,
)

class SourceDBStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        core.CfnOutput(self, 'MyService', value='completed bootstrapping')

        self.vpc = aws_ec2.Vpc(self, "EksVpc",
            cidr="10.0.0.0/16",
            max_azs=2,
            subnet_configuration=[
                aws_ec2.SubnetConfiguration(
                    name='DB-Subnets',
                    subnet_type=aws_ec2.SubnetType.ISOLATED,
                    cidr_mask=24
                ),
                aws_ec2.SubnetConfiguration(
                    name='OPS-Subnets',
                    subnet_type=aws_ec2.SubnetType.PRIVATE,
                    cidr_mask=24
                ),
                aws_ec2.SubnetConfiguration(
                    name='NAT-Subnets',
                    subnet_type=aws_ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                )
            ]
        )



