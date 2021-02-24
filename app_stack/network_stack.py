from aws_cdk import (
    core,
    aws_ec2,
)

class NetworkStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.vpc = aws_ec2.Vpc(self, "network",
            cidr="10.0.0.0/16",
            max_azs=2,
            subnet_configuration=[]
        )

        az_src = self.vpc.availability_zones[0];
        az_dst = self.vpc.availability_zones[1];

        aws_ec2.Subnet(self, "sbn-sourcedb",
            availability_zone=az_src,
            vpc_id=self.vpc.vpc_id,
            cidr_block='10.0.1.0/24'
        )
