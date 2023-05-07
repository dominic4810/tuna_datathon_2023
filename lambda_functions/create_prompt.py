import json
import os
import boto3

bucket_name = os.environ['BUCKET_NAME']
s3 = boto3.client("s3")


def lambda_handler(event, context):
    data = json.loads(json.dumps(event))
    question = data['data']['text_inputs']
    document_keys = data['top_keys']
    documents = []
    for key in document_keys:
        response = s3.get_object(Bucket=bucket_name, Key=key)
        file_content = response['Body'].read().decode('utf-8')
        json_data = json.loads(file_content)
        documents.append(json_data['paragraph'])
    documents = '\n'.join(documents)
    prompt = f"These are some swiss laws: {documents}. Answer the question: {question}"
    data['data']['text_inputs'] = prompt
    data.pop('embedding')
    return data