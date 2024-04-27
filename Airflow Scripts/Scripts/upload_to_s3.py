import boto3
import logging
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def upload_to_s3():
    # Set your AWS credentials and bucket details
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
    bucket_name = 'xxx'
    local_file_path = 'Airflow Scripts/Data/stock_info_2years.pdf'
    s3_file_key = 'Stock_Market_Information/stock_info.pdf'

    # Initialize the S3 client
    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )

    try:
        # Upload the file
        s3.upload_file(local_file_path, bucket_name, s3_file_key)
        logging.info(f"Successfully uploaded {local_file_path} to s3://{bucket_name}/{s3_file_key}")
    except Exception as e:
        logging.error(f"Failed to upload file to S3: {e}")

if __name__ == "__main__":
    upload_to_s3()
