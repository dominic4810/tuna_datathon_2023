import os
import io
import boto3
import json
import csv

# grab environment variables
ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
runtime= boto3.client('runtime.sagemaker')


def lambda_handler(event, context):
    data = json.loads(json.dumps(event))
    payload = json.dumps(data['data']).encode('utf-8')

    query_response = runtime.invoke_endpoint(
        EndpointName=ENDPOINT_NAME,
        ContentType='application/json', 
        Body=payload)

    response_dict = json.loads(query_response['Body'].read())

    return response_dict['generated_texts']