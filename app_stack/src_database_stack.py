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

        db_security_group = aws_ec2.SecurityGroup(self, 'sg-src-db',
            vpc=vpc
        )

        db_security_group.add_ingress_rule(
            peer=aws_ec2.Peer.ipv4('10.0.5.192/26'),
            connection=aws_ec2.Port(
                protocol=aws_ec2.Protocol.TCP,
                string_representation="to allow traffic from the cmd",
                from_port=5432,
                to_port=5432
            )
        )

        _postgres_instance=rds.DatabaseInstance(self, 'src_ora',
            engine=rds.DatabaseInstanceEngine.POSTGRES,
            vpc=vpc,
            vpc_subnets=aws_ec2.SubnetSelection(subnets=_subnets),
            security_groups=[db_security_group]
        )

        core.CfnOutput(self, 'secret_name', value=_postgres_instance.secret.secret_name)

        self._secret_name=_postgres_instance.secret.secret_name
        self._secret_arn=_postgres_instance.secret.secret_arn

    @property
    def secret_name(self):
        return self._secret_name

    @property
    def secret_arn(self):
        return self._secret_arn