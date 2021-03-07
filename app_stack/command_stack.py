from aws_cdk import (
    core,
    aws_ec2,
    aws_iam,
    aws_lambda,
)

class CommandStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, 
            vpc: aws_ec2.Vpc,
            cmd_subnet: aws_ec2.Subnet,
            db_secret_name: str,
            db_secret_arn: str,
            **kwargs) -> None:

        super().__init__(scope, id, **kwargs)

        cmd_role_init_src_db = aws_iam.Role(self, 'cmd_role_init_src_db',
            assumed_by=aws_iam.ServicePrincipal("lambda.amazonaws.com")
        )

        cmd_role_init_src_db.add_to_policy(
            aws_iam.PolicyStatement(
                resources=['*'],
                actions=[
                    'logs:CreateLogGroup',
                    'logs:CreateLogStream',
                    'logs:PutLogEvents',
                    "ec2:CreateNetworkInterface",
                    "ec2:DescribeNetworkInterfaces",
                    "ec2:DeleteNetworkInterface",
                ]
            )
        )

        cmd_role_init_src_db.add_to_policy(
            aws_iam.PolicyStatement(
                resources=[db_secret_arn],
                actions=[
                    "secretsmanager:GetResourcePolicy",
                    "secretsmanager:GetSecretValue",
                    "secretsmanager:DescribeSecret",
                    "secretsmanager:ListSecretVersionIds"
                ]
            )
        )

        cmd_func_init_src_db = aws_lambda.Function(self, 'cmd_func_init_src_db',
            function_name='demo_cmd_func_init_src_db',
            handler='cmd_init_src_db.init',
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            code=aws_lambda.Code.asset('./app_stack/cmd_func_init_src_db'),
            role=cmd_role_init_src_db,
            timeout=core.Duration.seconds(900),
            allow_public_subnet=False,
            vpc=vpc,
            vpc_subnets=aws_ec2.SubnetSelection(subnets=[cmd_subnet]),
            environment={
                'db_secret': db_secret_name
            }
        )
    