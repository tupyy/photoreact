import boto3
from botocore.config import Config


def sign_url(method, filename, filetype):
    """
    Sign the url for S3
    :param method: method to be used
    :param filename: filename
    :param filetype: type of the file
    :return: s3 signed url
    """
    s3 = boto3.client('s3', config=Config(signature_version='s3v4'))
    return s3.generate_presigned_url(
        ClientMethod=method,
        Params={
            'Bucket': S3_BUCKET,
            'Key': filename,
            'ContentType': filetype
        }
    )


def put_signed(filename, filetype):
    return sign_url('put_object', filename, filetype)


def get_signed_url(filename, filetype):
    return sign_url('get_object', filename, filetype)