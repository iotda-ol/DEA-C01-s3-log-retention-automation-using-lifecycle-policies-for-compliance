"""
S3 Operations Module
Provides reusable S3 client operations
"""

import boto3
from typing import List, Dict, Optional, BinaryIO
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger(__name__)


class S3Operations:
    """S3 client wrapper with common operations"""

    def __init__(self, region: str = 'us-east-1', profile: Optional[str] = None):
        """
        Initialize S3 operations client

        Args:
            region: AWS region
            profile: AWS profile name
        """
        session = boto3.Session(profile_name=profile) if profile else boto3.Session()
        self.client = session.client('s3', region_name=region)
        self.region = region
        logger.info(f"S3 client initialized for region: {region}")

    def list_buckets(self) -> List[Dict]:
        """
        List all S3 buckets in the account

        Returns:
            List of bucket dictionaries
        """
        try:
            response = self.client.list_buckets()
            buckets = response.get('Buckets', [])
            logger.info(f"Found {len(buckets)} buckets")
            return buckets
        except ClientError as e:
            logger.error(f"Error listing buckets: {e}")
            raise

    def bucket_exists(self, bucket_name: str) -> bool:
        """
        Check if a bucket exists and is accessible

        Args:
            bucket_name: Name of the bucket

        Returns:
            True if bucket exists, False otherwise
        """
        try:
            self.client.head_bucket(Bucket=bucket_name)
            return True
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code in ('404', 'NoSuchBucket'):
                return False
            # Re-raise other errors (permissions, etc.)
            logger.error(f"Error checking bucket {bucket_name}: {e}")
            raise

    def create_bucket(self, bucket_name: str, region: Optional[str] = None) -> bool:
        """
        Create a new S3 bucket

        Args:
            bucket_name: Name of the bucket to create
            region: AWS region (defaults to client region)

        Returns:
            True if successful
        """
        try:
            region = region or self.region
            if region == 'us-east-1':
                self.client.create_bucket(Bucket=bucket_name)
            else:
                self.client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': region}
                )
            logger.info(f"Created bucket: {bucket_name}")
            return True
        except ClientError as e:
            logger.error(f"Error creating bucket {bucket_name}: {e}")
            raise

    def upload_file(self, file_path: str, bucket: str, key: str,
                    extra_args: Optional[Dict] = None) -> bool:
        """
        Upload a file to S3

        Args:
            file_path: Local file path
            bucket: Target bucket name
            key: Object key in S3
            extra_args: Additional upload arguments

        Returns:
            True if successful
        """
        import os
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            self.client.upload_file(file_path, bucket, key, ExtraArgs=extra_args)
            logger.info(f"Uploaded {file_path} to s3://{bucket}/{key}")
            return True
        except ClientError as e:
            logger.error(f"Error uploading {file_path}: {e}")
            raise

    def upload_fileobj(self, fileobj: BinaryIO, bucket: str, key: str,
                       extra_args: Optional[Dict] = None) -> bool:
        """
        Upload a file object to S3

        Args:
            fileobj: File-like object
            bucket: Target bucket name
            key: Object key in S3
            extra_args: Additional upload arguments

        Returns:
            True if successful
        """
        try:
            self.client.upload_fileobj(fileobj, bucket, key, ExtraArgs=extra_args)
            logger.info(f"Uploaded file object to s3://{bucket}/{key}")
            return True
        except ClientError as e:
            logger.error(f"Error uploading file object: {e}")
            raise

    def download_file(self, bucket: str, key: str, file_path: str) -> bool:
        """
        Download a file from S3

        Args:
            bucket: Source bucket name
            key: Object key in S3
            file_path: Local file path to save

        Returns:
            True if successful
        """
        try:
            self.client.download_file(bucket, key, file_path)
            logger.info(f"Downloaded s3://{bucket}/{key} to {file_path}")
            return True
        except ClientError as e:
            logger.error(f"Error downloading {key}: {e}")
            raise

    def list_objects(self, bucket: str, prefix: str = '', 
                     max_keys: int = 1000) -> List[Dict]:
        """
        List objects in a bucket

        Args:
            bucket: Bucket name
            prefix: Object key prefix filter
            max_keys: Maximum number of keys to return

        Returns:
            List of object dictionaries
        """
        try:
            response = self.client.list_objects_v2(
                Bucket=bucket,
                Prefix=prefix,
                MaxKeys=max_keys
            )
            objects = response.get('Contents', [])
            logger.info(f"Found {len(objects)} objects in {bucket}")
            return objects
        except ClientError as e:
            logger.error(f"Error listing objects in {bucket}: {e}")
            raise

    def delete_object(self, bucket: str, key: str) -> bool:
        """
        Delete an object from S3

        Args:
            bucket: Bucket name
            key: Object key

        Returns:
            True if successful
        """
        try:
            self.client.delete_object(Bucket=bucket, Key=key)
            logger.info(f"Deleted s3://{bucket}/{key}")
            return True
        except ClientError as e:
            logger.error(f"Error deleting {key}: {e}")
            raise

    def copy_object(self, source_bucket: str, source_key: str,
                    dest_bucket: str, dest_key: str) -> bool:
        """
        Copy an object within S3

        Args:
            source_bucket: Source bucket name
            source_key: Source object key
            dest_bucket: Destination bucket name
            dest_key: Destination object key

        Returns:
            True if successful
        """
        try:
            copy_source = {'Bucket': source_bucket, 'Key': source_key}
            self.client.copy_object(
                CopySource=copy_source,
                Bucket=dest_bucket,
                Key=dest_key
            )
            logger.info(f"Copied s3://{source_bucket}/{source_key} to "
                       f"s3://{dest_bucket}/{dest_key}")
            return True
        except ClientError as e:
            logger.error(f"Error copying object: {e}")
            raise

    def get_object_metadata(self, bucket: str, key: str) -> Dict:
        """
        Get object metadata

        Args:
            bucket: Bucket name
            key: Object key

        Returns:
            Object metadata dictionary
        """
        try:
            response = self.client.head_object(Bucket=bucket, Key=key)
            return response
        except ClientError as e:
            logger.error(f"Error getting metadata for {key}: {e}")
            raise
