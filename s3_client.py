import logging
import boto3
from botocore.exceptions import ClientError


class S3Client:
    def __init__(self, endpoint, access_key, secret_key, bucket_name, sticker_file='stickers.json'):
        self.client = boto3.client('s3',
                                   endpoint_url=endpoint,
                                   aws_access_key_id=access_key,
                                   aws_secret_access_key=secret_key, verify=False)
        self.bucket = bucket_name
        self.sticker_file = sticker_file
        # try to create the bucket_name
        try:
            self.client.create_bucket(Bucket=self.bucket)
        except ClientError:
            logging.info("bucket already exists")

    def upload_file(self, file_name, object_name=None):
        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = file_name

        try:
            self.client.upload_file(file_name, self.bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def download_file(self, object_name, file_name=None):
        # If file_name was not specified, use object_name
        if file_name is None:
            file_name = object_name

        try:
            self.client.download_file(self.bucket, object_name, file_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def download_index(self, file_path):
        return self.download_file(self.sticker_file, file_path)

    def sticker_exists(self, sticker_name):
        try:
            r = self.client.head_object(Bucket=self.bucket, Key=sticker_name+"/pack.zip")
            return True if r["ResponseMetadata"]['HTTPStatusCode'] == 200 else False
        except ClientError as e:
            logging.error(e)
