from aws_cdk import core

from app_stack.network_stack import NetworkStack
from app_stack.src_database_stack import SrcDatabaseStack

class DeploymentStage(core.Stage):
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        _network = NetworkStack(self, 'Network')
        SrcDatabaseStack(self, 'SrcDatabase', vpc=_network.vpc)
