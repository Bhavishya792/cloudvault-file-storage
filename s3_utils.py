import os
import boto3

from botocore.exceptions import ClientError

from dotenv import load_dotenv

load_dotenv()


s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)


BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")


def upload_file_to_s3(file, s3_key):

    s3.upload_fileobj(file, BUCKET_NAME, s3_key)

    return True


def generate_download_url(s3_key):

    try:

        url = s3.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": BUCKET_NAME,
                "Key": s3_key,
            },
            ExpiresIn=3600,
        )

        return url

    except ClientError:

        return None


def delete_file_from_s3(s3_key):

    s3.delete_object(
        Bucket=BUCKET_NAME,
        Key=s3_key
    )

    return True