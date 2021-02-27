from aws_cdk import (
    core,
    aws_ec2,
)

class NetworkStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = aws_ec2.Vpc(self, "network",
            cidr="10.0.0.0/16",
            max_azs=2,
            subnet_configuration=[]
        )

        self.vpc=vpc
