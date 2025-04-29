# Import required AWS CDK constructs and libraries
from constructs import Construct
from aws_cdk import (
    aws_lambda as _lambda,
    aws_dynamodb as ddb
)

# HitCounter construct that creates a Lambda function and DynamoDB table
class HitCounter(Construct):

    # Property to expose the Lambda handler
    @property
    def handler(self):
        return self._handler

    # Initialize the construct with scope, id and downstream Lambda function
    def __init__(self, scope: Construct, id: str, downstream: _lambda.IFunction, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Create DynamoDB table to store hit counts
        table=ddb.Table(
            self, 'Hits',
            partition_key={'name': 'path', 'type': ddb.AttributeType.STRING}
        )
        
        # Create Lambda function that will handle counting hits
        self._handler = _lambda.Function(
            self, 'HitCounterHandler',
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler='hitcount_lambda.handler',
            code=_lambda.Code.from_asset('cdk_workshop/lambda'),
            environment={
                'DOWNSTREAM_FUNCTION_NAME': downstream.function_name,
                'HITS_TABLE_NAME': 'Hits'
            }
        )

        
