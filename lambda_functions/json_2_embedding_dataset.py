import json
import boto3
import os
import logging

s3 = boto3.client("s3")# grab environment variables
ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
sagemaker= boto3.client('runtime.sagemaker')


def lambda_handler(event, context):
    
    # Load embedding dataset
    embedding_db_bucket_name = "embedding-test-3"
    embedding_db_key = "dictionary_dataset.json"
    objects_in_embedding_db = s3.list_objects(Bucket=embedding_db_bucket_name)
    embedding_db_exists = False
    if 'Contents' in objects_in_embedding_db:
        keys_in_embedding_db = [obj['Key'] for obj in s3.list_objects(Bucket=embedding_db_bucket_name)['Contents']]
        embedding_db_exists = any(obj == embedding_db_key for obj in keys_in_embedding_db)
    if embedding_db_exists:
        response = s3.get_object(Bucket=embedding_db_bucket_name, Key=embedding_db_key)
        logging.info("Retrieved embedding DB with key {} from s3 bucket {}".format(embedding_db_key, embedding_db_bucket_name))
        file_content = response['Body'].read().decode('utf-8')
        embedding_dataset = json.loads(file_content)
    else:
        embedding_dataset = {}
    
    # Load new json files (only the paragraphs)
    json_docs_bucket_name = "datathon-tuna-json-docs"
    event = json.loads(json.dumps(event))
    json_object_keys = event['body']['new_keys']
    paragraphs = {}
    for json_key in json_object_keys:
        response = s3.get_object(Bucket=json_docs_bucket_name, Key=json_key)
        file_content = response['Body'].read().decode('utf-8')
        json_data = json.loads(file_content)
        logging.info("Retrieve json file with key {} from s3 bucket {}".format(json_key, json_docs_bucket_name))
        paragraphs[json_key] = json_data['paragraph'] if json_data['paragraph'] else ""
        
    
    # Get embeddings
    num_paragraphs = len(paragraphs)
    batch_size = 64
    paragraph_texts = list(paragraphs.values())
    new_embeddings = {}
    for batch_num in range(num_paragraphs // batch_size + 1):
        batch = paragraph_texts[batch_num * batch_size:(batch_num + 1) * batch_size]
        payload = {
            'text_inputs': batch
        }
        payload = json.dumps(payload).encode('utf-8')
        query_response = sagemaker.invoke_endpoint(
            EndpointName=ENDPOINT_NAME,
            ContentType='application/json', 
            Body=payload)
        response_dict = json.loads(query_response['Body'].read())
        for json_key, embedding in zip(paragraphs, response_dict['embedding']):
            embedding_dataset[json_key] = embedding
            new_embeddings[json_key] = embedding
    
    # Write dataset to s3
    
        # Upload the created files to a separate S3 bucket
    s3.put_object(Bucket=embedding_db_bucket_name, Key=embedding_db_key, Body=json.dumps(embedding_dataset))
    logging.info("Writing embedding DB with key {} to s3 bucket {}".format(embedding_db_bucket_name, embedding_db_key))
    
    return {
        "statusCode": 200,
        "body": event['body']
    }