from aws_cdk import (
    core,
    aws_ec2,
    aws_redshift,
)

class DesRedshiftStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc: aws_ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        _subnets=[]
        _subnets.append(
            aws_ec2.Subnet(self, 'sbn-redshift-1',
                availability_zone=vpc.availability_zones[0],
                vpc_id=vpc.vpc_id,
                cidr_block='10.0.4.0/25'
            )
        )

        _subnets.append(
            aws_ec2.Subnet(self, 'sbn-redshift-2',
                availability_zone=vpc.availability_zones[1],
                vpc_id=vpc.vpc_id,
                cidr_block='10.0.4.128/25'
            )
        )

        _cluster_subnet_group = aws_redshift.ClusterSubnetGroup(self, 'deta-pipeline-redshift-subnet',
            description='redshift cluster subnet',
            vpc=vpc,
            vpc_subnets=aws_ec2.SubnetSelection(subnets=_subnets)
        )

        aws_redshift.Cluster(self, 'destination-redshift',
            master_user=aws_redshift.Login(master_username='admin'),
            vpc=vpc,
            subnet_group=_cluster_subnet_group
        )
