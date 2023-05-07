# AWS Lambda
In this markdown, we describe the AWS Lambda functions we implemented.
We include the implementation of the `lambda_handler` methods, in the `*.py` files


## createPrompt
Generates prompt from the given question and relevant documents retrieved by `retrieve_documents`

## flanInference
Interface with `FLAN-T5-XL` endpoint

## gpt6jInference
Interface with `GPT-J 6B Embedding FP16` endpoint

## json2Embedding
Generates/Updates the embedding database with new articles

## OnXmlUpload
Triggered when an `XML` file is uploaded to s3. This triggers the `UpdateEmbeddingDB` state machine

## retrieveDocuments
Searches for articles that are relevant to a given question, based on our embedding database.

## Xml2Json
Processed `XML` documents into `JSON` files, each containing an article
