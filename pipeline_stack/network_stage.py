from aws_cdk import core

from app_stack.network_stack import NetworkStack

class NetworkStage(core.Stage):
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        NetworkStack(self, 'Network')