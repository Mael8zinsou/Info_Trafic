import boto3
import os

def upload_file(file_path, bucket_name, s3_key, aws_profile=None):
    session = boto3.Session(profile_name=aws_profile) if aws_profile else boto3.Session()
    s3 = session.resource('s3')
    s3.Bucket(bucket_name).upload_file(file_path, s3_key)

def download_file(bucket_name, s3_key, local_path, aws_profile=None):
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    session = boto3.Session(profile_name=aws_profile) if aws_profile else boto3.Session()
    s3 = session.resource('s3')
    s3.Bucket(bucket_name).download_file(s3_key, local_path)
