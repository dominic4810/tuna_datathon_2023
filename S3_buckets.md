We utilized S3 buckets to store .xml files with law paragraphs and parsed .json files separately for each paragraph.

The configuration of an S3 bucket is as follows:
* bucket names: datathon-tuna-json-docs, datathon-tuna-xml-docs,
* AWS region: us-east-1,
* ACL: activated,
* public access: granted.