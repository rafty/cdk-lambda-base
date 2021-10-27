from aws_cdk import core as cdk
from aws_cdk import aws_lambda
from aws_cdk import aws_sam
from aws_cdk.core import Tags

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class CdkLambdaBaseStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        POWERTOOLS_ARN = 'arn:aws:serverlessrepo:eu-west-1:057560766410:applications/aws-lambda-powertools-python-layer'
        POWERTOOLS_VER = '1.21.1'

        power_tools_layer = aws_sam.CfnApplication(
            scope=self,
            id='AWSLambdaPowertoolsLayer',
            location={
                'applicationId': POWERTOOLS_ARN,
                'semanticVersion': POWERTOOLS_VER
            }
        )
        power_tools_layer_arn = power_tools_layer.get_att(
            'Outputs.LayerVersionArn').to_string()
        power_tools_layer_version = aws_lambda\
            .LayerVersion.from_layer_version_arn(
                scope=self,
                id='AWSLambdaPowertoolsLayerVersion',
                layer_version_arn=power_tools_layer_arn)

        fn_base_app = aws_lambda.Function(
            scope=self,
            id='BaseAppFunction',
            function_name='cdk_base_app',
            description='deployed by AWS CDK Python',
            code=aws_lambda.Code.from_asset(
                'src/lambda/base'),
            handler='base_app.handler',
            # role=lambda_role,
            # tracing=aws_lambda.Tracing.ACTIVE,
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            # environment={},
            layers=[power_tools_layer_version]
        )

        Tags.of(fn_base_app).add('Application', 'Base')

        cdk.CfnOutput(
            scope=self,
            id='CdkBaseLambdaName',
            value=fn_base_app.function_name
        )
        cdk.CfnOutput(
            scope=self,
            id='CdkBaseLambdaArn',
            value=fn_base_app.function_arn
        )
