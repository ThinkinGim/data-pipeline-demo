from aws_cdk import core

from app_stack.network_stack import NetworkStack
from app_stack.src_database_stack import SrcDatabaseStack
from app_stack.data_pipeline_stack import DataPipelineStack

class DeploymentStage(core.Stage):
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        _network = NetworkStack(self, 'Network')
        SrcDatabaseStack(self, 'SrcDatabase', vpc=_network.vpc)
        DataPipelineStack(self, 'DataPipeline', vpc=_network.vpc)
