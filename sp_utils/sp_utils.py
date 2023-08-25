import requests
import os
import uuid
import boto3

tmp_path = "./tmp"

bucket = os.environ.get("AWS_BUCKET")
aws_access_key_id = os.environ.get("AWS_S3_ACCESS_KEY_ID")
aws_secret_access_key = os.environ.get(
    "AWS_S3_ACCESS_SECRET")
region_name = os.environ.get("AWS_S3_REGION")


def download_from_source(url):
    random_uuid = uuid.uuid4()

    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)

    filename = f'{tmp_path}/{random_uuid}.{extract_file_type(url)}'

    if not os.path.exists(filename):
        try:
            # Add a timeout and stream the content
            stream = True
            # 5 seconds connect timeout, 10 seconds read timeout
            timeout = (5, 10)
            r = requests.get(url, stream=stream, timeout=timeout)

            # Raise an error for failed HTTP requests
            r.raise_for_status()

            with open(filename, 'wb') as outfile:
                for chunk in r.iter_content(chunk_size=8192):
                    outfile.write(chunk)
        except requests.RequestException as e:
            print(f"Error downloading image: {e}")
            return None

    return filename


def extract_file_type(url):
    # Split the URL into parts using the last occurrence of the '/' character
    parts = url.rsplit('/', 1)
    if len(parts) == 2:
        # Split the second part into filename and file extension using the last occurrence of the '.' character
        filename, file_extension = parts[1].rsplit('.', 1)
        return file_extension
    else:
        return ''


def get_boto_client():
    return boto3.client('s3',
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                        region_name=region_name)


def upload_to_s3(filename, folder):
    s3 = get_boto_client()
    key = f"conversions/{folder}/{os.path.basename(filename)}"
    s3.upload_file(
        Bucket=bucket,
        Filename=filename,
        Key=key,
        ExtraArgs={'ACL': 'public-read'}
    )
    return f"https://{bucket}.s3.amazonaws.com/{key}"
