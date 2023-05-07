import json
import boto3

client = boto3.client('stepfunctions')

def lambda_handler(event, context):
    response = client.start_execution(
        stateMachineArn='arn:aws:states:us-east-1:070515415235:stateMachine:UpdateEmbeddingDB',
        input=json.dumps(event),
    )
    return {
        'statusCode': 200,
    }