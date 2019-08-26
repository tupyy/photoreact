import boto3
from botocore.config import Config
from src.photogallery import settings


def sign_url(http_method, filename):
    """
    Sign the url for S3
    :param http_method: method to be used
    :param filename: filename
    :return: s3 signed url
    """
    s3 = boto3.client('s3', config=Config(signature_version='s3v4'))
    return s3.generate_presigned_url(
        ClientMethod=http_method,
        Params={
            'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
            'Key': filename
        },
        ExpiresIn=3600
    )


def get_put_signed_url(filename):
    return sign_url('put_object', filename)


def get_get_signed_url(filename):
    return sign_url('get_object', filename)