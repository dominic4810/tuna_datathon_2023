# AWS Step Functions

We use the `State machines` feature in AWS Step Functions to chain our lambda functions.
This allows use to:
1. Perform question embedding, document retrieval, prompt engineering and answer generation sequentially.
2. Automatically process `XML` files uploaded to s3, to extract the articles into `JSON` files and update our embedding database with the new articles. The `XML` files are swiss laws downloaded from [this website](https://www.fedlex.admin.ch/en/cc/internal-law/1)

# UpdateEmbeddingDB

This state machine calls two AWS Lambda functions in sequence: `Xml2Json` and `json2EmbeddingDataset`.

The state machine itself is called by the AWS Lambda function `OnXmlUpload`, which is triggered when an object is uploaded to the s3 bucket `datathon-tuna-xml-docs`.

The output of this state machine is the updated embedding database, which is dumped into the s3 bucket `embedding-test-3`.

# TunaBackend

This state machine is the state machine that our API calls.
It calls the following lambda functions in order:
1. `gpt6jInference`: Embed question
2. `retrieveDocuments`: Get most relevant articles
3. `createPrompt`: Prompt engineering
4. `flanInference`: Generate answer

# State machine configurations

The configuration of the state machines are given here in `UpdateEmbeddingDB.json` and `TunaBackend.json`.
Note that the values of `Resource` (i.e. the Arn values) could be different.