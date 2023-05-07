We utilized S3 buckets to store .xml files with law paragraphs and parsed .json files separately for each paragraph.

The configuration of an S3 bucket is as follows:
* bucket names: datathon-tuna-json-docs, datathon-tuna-xml-docs, embedding-test3,
* AWS region: us-east-1,
* ACL: activated,
* public access: granted.

###### datathon-tuna-json-docs

This bucket contains data parsed from XML to JSON format. Each json corresponds to one specific paragraph and stores data regarding its correspondance to a law document, title, chapter, section and/or article.

###### datathon-tuna-xml-docs

In this bucket, we upload law documents in XML format (divided into titles, chapters, sections, articles and paragraphs).

###### embedding-test3

Here, we store our embedding database with data retrieved from json files.