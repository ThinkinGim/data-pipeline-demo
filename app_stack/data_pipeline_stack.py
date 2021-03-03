from aws_cdk import (
    core,
    aws_ec2,
    aws_rds as rds,
    aws_dms as dms,
)

class DataPipelineStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc: aws_ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        aws_ec2.SecurityGroup(self, 'dms-securitygroup',
            vpc=vpc
        )

        _subnets=[]
        _subnets.append(
            aws_ec2.Subnet(self, 'sbn-dms-1',
                availability_zone=vpc.availability_zones[0],
                vpc_id=vpc.vpc_id,
                cidr_block='10.0.3.0/25'
            ).subnet_id
        )

        _subnets.append(
            aws_ec2.Subnet(self, 'sbn-dms-2',
                availability_zone=vpc.availability_zones[1],
                vpc_id=vpc.vpc_id,
                cidr_block='10.0.3.128/25'
            ).subnet_id
        )

        _subnet_group_id='deta-pipeline-dms-subnet'

        dms.CfnReplicationSubnetGroup(self, 'dms-subnet-group',
            replication_subnet_group_description='subnet group for dms',
            subnet_ids=_subnets,
            replication_subnet_group_identifier=_subnet_group_id
        )
       
        dms.CfnReplicationInstance(self, 'dms-demo',
            replication_instance_class='dms.t3.medium',
            allocated_storage=50,
            allow_major_version_upgrade=False,
            auto_minor_version_upgrade=False,
            publicly_accessible=False,
            multi_az=False,
            replication_subnet_group_identifier=_subnet_group_id
        )

        # dms.CfnEndpoint(self, 'dms-src',
        #     endpoint_type='source',
        #     engine_name='demo-dms-src',

        # )

