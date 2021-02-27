from aws_cdk import core

from app_stack.src_database_stack import SrcDatabaseStack

class SrcDatabaseStage(core.Stage):
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        SrcDatabaseStack(self, 'Src-DB')