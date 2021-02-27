from aws_cdk import (
    core,
    aws_ec2,
)

class SrcDatabaseStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
