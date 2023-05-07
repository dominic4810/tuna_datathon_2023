import json
import boto3
import json
from dataclasses import dataclass
from typing import Optional, Generator
import xml
import xml.etree.ElementTree as ET
import logging

s3 = boto3.client('s3')

@dataclass
class Leaf:
    chapter: Optional[int] = None
    chapter_name: Optional[str] = None
    section: Optional[int] = None
    section_name: Optional[str] = None
    article: Optional[int] = None
    article_name: Optional[str] = None
    paragraph_id: Optional[int] = None
    paragraph: Optional[str] = None

    def as_dict(self):
        return {
            "chapter": self.chapter,
            "chapter_name": self.chapter_name,
            "section": self.section,
            "section_name": self.section_name,
            "article": self.article,
            "article_name": self.article_name,
            "paragraph_id": self.paragraph_id,
            "paragraph": self.paragraph,
        }


def get_leaves(
    root: xml.etree.ElementTree.Element,
    leaf: Leaf
) -> Generator[xml.etree.ElementTree.Element, None, None]:
    """Get all leaves of an XML tree.

    Args:
        root (xml.etree.ElementTree.Element): root of the XML tree

    Yields:
        Generator[xml.etree.ElementTree.Element, None, None]: leaves of the XML tree
    """
    if root.tag.endswith('chapter'):
        leaf = extract_eid(root, leaf)
    if root.tag.endswith('section'):
        leaf = extract_eid(root, leaf)
    if root.tag.endswith('article'):
        leaf = extract_eid(root, leaf)
    if root.tag.endswith('paragraph'):
        yield extract_paragraph(root, leaf)
    else:
        for child in root:
            yield from get_leaves(child, leaf)


def extract_eid(node: xml.etree.ElementTree, leaf: Leaf) -> Leaf:
    eid = node.get("eId")
    if node.tag.endswith('chapter'):
        eid = eid.split('/')[0]
        leaf.chapter = eid.split('_')[-1]
        leaf.chapter_name = eid.replace('_', '-')
    if node.tag.endswith('section'):
        eid = eid.split('/')[-1]
        leaf.section = eid.split('_')[-1]
        leaf.section_name = eid.replace('_', '-')
    if node.tag.endswith('article'):
        leaf.article = eid.split('_')[-1]
        leaf.article_name = eid.replace('_', '-')
    return leaf

def extract_paragraph(paragraph_node: xml.etree.ElementTree, leaf: Leaf) -> Leaf:
    for child in paragraph_node:
        if child.tag.endswith('content'):
            paragraph = child[0].text
            if not paragraph:
                continue
            paragraph = paragraph.replace('\u00a0', ' ')
            leaf.paragraph = paragraph
        if child.tag.endswith('num'):
            leaf.paragraph_id = child.text
    return leaf


def lambda_handler(event, context):
    # Retrieve the uploaded file
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    response = s3.get_object(Bucket=bucket_name, Key=key)
    logging.info("Retrieved object with key {} from s3 bucket {}".format(key, bucket_name))
    file_content = response['Body'].read().decode('utf-8')
    xml_filename = key[:-4]
    # Process the uploaded file and create some files to upload to S3
    xml_tree = ET.fromstring(file_content)
    leaf = Leaf()
    keys = []
    for leaf in get_leaves(xml_tree, leaf):
        # Upload the created files to a separate S3 bucket
        new_bucket_name = 'datathon-tuna-json-docs'
        new_key = (
            f"{xml_filename}_{leaf.chapter_name}_{leaf.section_name}_{leaf.article_name}_{leaf.paragraph_id}.json"
        )
        s3.put_object(Bucket=new_bucket_name, Key=new_key, Body=json.dumps(leaf.as_dict()))
        logging.info("Writing JSON object with key {} to s3 bucket {}".format(new_bucket_name, new_key))
        keys.append(new_key)
    return {
        'statusCode': 200,
        'body': {
            "new_keys": keys
        }
    }