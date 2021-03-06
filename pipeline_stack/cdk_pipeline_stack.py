from aws_cdk import (
    core,
    aws_iam,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as cpactions,
    pipelines,
)

from .deployment_stage import DeploymentStage

class CdkPipelineStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, params: dict, **kwargs):
        super().__init__(scope, id, **kwargs)

        source_artifact = codepipeline.Artifact()
        cloud_assembly_artifact = codepipeline.Artifact()

        pipeline = pipelines.CdkPipeline(self, 'datapipeline-demo-cd', 
            cloud_assembly_artifact=cloud_assembly_artifact,
            pipeline_name=params['pipeline_name'],            
            source_action=cpactions.BitBucketSourceAction(
                action_name='GithubAction',
                output=source_artifact,
                connection_arn=params['connection_arn'],
                owner=params['github_owner'],
                repo=params['github_repo'],
                branch=params['github_branch']
            ),
            synth_action=pipelines.SimpleSynthAction(
                source_artifact=source_artifact,
                cloud_assembly_artifact=cloud_assembly_artifact,
                role_policy_statements=[
                    aws_iam.PolicyStatement(
                        actions=["secretsmanager:GetSecretValue"],
                        resources=[params['secret_arn']]
                    ),
                    aws_iam.PolicyStatement(
                        actions=[
                            "ec2:CreateNetworkInterface",
                            "ec2:DescribeAvailabilityZones",
                            "ec2:DescribeInternetGateways",
                            "ec2:DescribeSecurityGroups",
                            "ec2:DescribeSubnets",
                            "ec2:DescribeVpcs",
                            "ec2:DeleteNetworkInterface",
                            "ec2:ModifyNetworkInterfaceAttribute"
                        ],
                        resources=['*']
                    ),
                ],
                install_command='npm install -g aws-cdk && pip install --upgrade pip && pip install -r requirements.txt',
                synth_command="cdk synth -v -c region=%s -c secret_name=%s"%(params['region'],params['secret_name']),
            )
        )

        pipeline.add_application_stage(DeploymentStage(self, 'datapipeline-demo'))