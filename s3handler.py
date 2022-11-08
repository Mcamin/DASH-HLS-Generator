import os
from tqdm import tqdm
import boto3
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
BUCKET_NAME = os.environ.get("BUCKET_NAME")
s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)


def upload_folder_to_s3(input_dir, s3_path):
    """
    Upload a folder to a predefined s3 bucket
    Args:
        input_dir:  the local folder path to upload
        s3_path:  the s3 path
    """
    pbar = tqdm(os.walk(input_dir))
    for path, subdirs, files in pbar:
        for file in files:
            dest_path = path.replace(input_dir, "").replace(os.sep, '/')
            s3_file = f'{s3_path}/{dest_path}/{file}'.replace('//', '/')
            local_file = os.path.join(path, file)
            s3_client.upload_file(local_file, BUCKET_NAME, s3_file)
            pbar.set_description(f'Uploaded {local_file} to {s3_file}')
    print(f"Successfully uploaded {input_dir} to S3 {s3_path}")
