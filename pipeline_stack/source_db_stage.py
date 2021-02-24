from aws_cdk import core

from app_stack.source_db_stack import SourceDBStack

class SourceDBStage(core.Stage):
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        SourceDBStack(self, 'SourceDBStack')