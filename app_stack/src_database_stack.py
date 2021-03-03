from aws_cdk import (
    core,
    aws_ec2,
    aws_rds as rds,
    aws_dms as dms,
)

class SrcDatabaseStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc: aws_ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        _subnets=[]
        _subnets.append(
            aws_ec2.Subnet(self, 'sbn-sourcedb-1',
                availability_zone=vpc.availability_zones[0],
                vpc_id=vpc.vpc_id,
                cidr_block='10.0.1.0/24'
            )
        )

        _subnets.append(
            aws_ec2.Subnet(self, 'sbn-sourcedb-2',
                availability_zone=vpc.availability_zones[1],
                vpc_id=vpc.vpc_id,
                cidr_block='10.0.2.0/24'
            )
        )

        _postgres_instance=rds.DatabaseInstance(self, 'src_ora',
            engine=rds.DatabaseInstanceEngine.POSTGRES,
            vpc=vpc,
            vpc_subnets=aws_ec2.SubnetSelection(subnets=_subnets)
        )

        self._db_secret=_postgres_instance.secret

    @property
    def db_secret(self):
        return self._db_secret
    

