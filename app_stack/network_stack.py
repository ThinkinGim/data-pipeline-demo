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

        cmd_subnet = aws_ec2.Subnet(self, 'sbn-cmd-1',
            availability_zone=vpc.availability_zones[0],
            vpc_id=vpc.vpc_id,
            cidr_block='10.0.5.192/26'
        )

        vpc.add_interface_endpoint('secretmanager',
            service=aws_ec2.InterfaceVpcEndpointAwsService.SECRETS_MANAGER,
            subnets=aws_ec2.SubnetSelection(subnets=[cmd_subnet])
        )

        self.vpc=vpc
        self.cmd_subnet=cmd_subnet