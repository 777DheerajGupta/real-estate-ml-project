import boto3
import os
import pickle
import pandas as pd

BUCKET_NAME = "realestate-ml-models-413027378663-ap-southeast-2-an"


print(sts.get_caller_identity())

def download_file(filename):
    """Download a single file from S3 if not already present"""
    local_path = f"datasets/{filename}"
    os.makedirs("datasets", exist_ok=True)

    if not os.path.exists(local_path):
        print(f"Downloading {filename} from S3...")
        s3 = boto3.client(
            's3',
            aws_access_key_id     = os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY'),
            region_name = os.environ.get('AWS_REGION', 'ap-southeast-2')
        )
        s3.download_file(BUCKET_NAME, filename, local_path)
        print(f"✅ {filename} downloaded")

        print("AWS Identity:", sts.get_caller_identity())

        s3 = boto3.client(
            's3',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            region_name=os.environ.get('AWS_REGION', 'ap-southeast-2')
        )

        s3.download_file(BUCKET_NAME, filename, local_path)
        print(f"✅ {filename} downloaded")
    else:
        print(f"⏭️ {filename} already exists")

    return local_path

def load_pickle(filename):
    local_path = download_file(filename)
    with open(local_path, 'rb') as f:
        return pickle.load(f)

def load_csv(filename):
    local_path = download_file(filename)
    return pd.read_csv(local_path)