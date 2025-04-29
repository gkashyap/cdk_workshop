# Import required libraries
import json
import os
import boto3

# Initialize DynamoDB and Lambda clients
ddb = boto3.resource('dynamodb')
table = ddb.Table(os.environ['HITS_TABLE_NAME'])
_lambda = boto3.client('lambda')

def handler(event, context):
    # Log the incoming request
    print('request: {}'.format(json.dumps(event)))
    
    # Increment the hit counter for this path in DynamoDB
    table.update_item(
        Key={
            'path': event['path']
        },
        UpdateExpression='ADD hits :incr',
        ExpressionAttributeValues={
            ':incr': 1
        }
    )
    
    # Invoke downstream Lambda function
    resp = _lambda.invoke(
        FunctionName=os.environ['DOWNSTREAM_FUNCTION_NAME'],
        Payload=json.dumps(event),
    )
    
    # Get and decode the response
    body = resp['Payload'].read().decode("utf-8")
    print('downstream response: {}'.format(body))
    
    # Return the parsed response
    return json.loads(body)
