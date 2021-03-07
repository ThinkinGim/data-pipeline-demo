from aws_cdk import core

from app_stack.network_stack import NetworkStack
from app_stack.src_database_stack import SrcDatabaseStack
from app_stack.des_redshift_stack import DesRedshiftStack
from app_stack.data_pipeline_stack import DataPipelineStack
from app_stack.command_stack import CommandStack

class DeploymentStage(core.Stage):
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        _network = NetworkStack(self, 'Network')

        _src_database=SrcDatabaseStack(self, 'SrcDatabase', vpc=_network.vpc)
        DesRedshiftStack(self, 'DesRedshift', vpc=_network.vpc)
        _data_pipeline_stack=DataPipelineStack(self, 'DataPipeline', vpc=_network.vpc)
        _cmd = CommandStack(self, 'Command', 
            vpc=_network.vpc,
            cmd_subnet=_network.cmd_subnet
        )