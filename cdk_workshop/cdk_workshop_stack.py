# Import required AWS CDK constructs and services
from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,  # AWS Lambda service construct
    aws_apigateway as apigw # API Gateway service construct
)

# Import custom hit counter construct
from hitcounter_costruct import HitCounter

class CdkWorkshopStack(Stack):

    """
    CDK Stack that creates a Lambda function with API Gateway and hit counter
    """
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create Lambda function that will handle requests
        my_lambda = _lambda.Function(
            self, 'HelloHandler',
            runtime=_lambda.Runtime.PYTHON_3_12,
            code=_lambda.Code.from_asset('cdk_workshop/lambda/'),  # Lambda code location
            handler='hello.handler',  # Handler function
        )

        # Create hit counter construct that will track invocations
        hitcounter = HitCounter(
            self, 'HitCounter',
            downstream=my_lambda,  # Pass Lambda function as downstream target
        )

        # Create API Gateway REST API with Lambda integration
        apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=hitcounter.handler,  # Use hit counter Lambda as handler
        )

    
