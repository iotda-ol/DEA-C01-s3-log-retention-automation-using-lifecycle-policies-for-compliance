"""
S3 Operations Module
Provides high-level interface for S3 operations
"""

import logging
from typing import List, Dict, Optional, Any
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)


class S3Client:
    """High-level S3 client for log retention operations"""

    def __init__(self, region_name: Optional[str] = None, profile_name: Optional[str] = None):
        """
        Initialize S3 client

        Args:
            region_name: AWS region name
            profile_name: AWS profile name
        """
        session_kwargs = {}
        if region_name:
            session_kwargs['region_name'] = region_name
        if profile_name:
            session_kwargs['profile_name'] = profile_name

        self.session = boto3.Session(**session_kwargs)
        self.s3_client = self.session.client('s3')
        self.s3_resource = self.session.resource('s3')
        logger.info(f"Initialized S3 client for region: {self.s3_client.meta.region_name}")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def list_buckets(self) -> List[Dict[str, Any]]:
        """
        List all S3 buckets in the account

        Returns:
            List of bucket dictionaries with name and creation date
        """
        try:
            response = self.s3_client.list_buckets()
            buckets = [
                {
                    'name': bucket['Name'],
                    'creation_date': bucket['CreationDate']
                }
                for bucket in response.get('Buckets', [])
            ]
            logger.info(f"Found {len(buckets)} buckets")
            return buckets
        except ClientError as e:
            logger.error(f"Error listing buckets: {e}")
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def get_bucket_location(self, bucket_name: str) -> str:
        """
        Get bucket location

        Args:
            bucket_name: Name of the S3 bucket

        Returns:
            AWS region name
        """
        try:
            response = self.s3_client.get_bucket_location(Bucket=bucket_name)
            location = response.get('LocationConstraint', 'us-east-1')
            # us-east-1 returns None
            return location if location else 'us-east-1'
        except ClientError as e:
            logger.error(f"Error getting bucket location for {bucket_name}: {e}")
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def get_lifecycle_configuration(self, bucket_name: str) -> Optional[Dict[str, Any]]:
        """
        Get lifecycle configuration for a bucket

        Args:
            bucket_name: Name of the S3 bucket

        Returns:
            Lifecycle configuration dict or None if not configured
        """
        try:
            response = self.s3_client.get_bucket_lifecycle_configuration(Bucket=bucket_name)
            logger.info(f"Retrieved lifecycle configuration for {bucket_name}")
            return response
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchLifecycleConfiguration':
                logger.info(f"No lifecycle configuration for {bucket_name}")
                return None
            logger.error(f"Error getting lifecycle configuration for {bucket_name}: {e}")
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def list_objects(
        self,
        bucket_name: str,
        prefix: str = '',
        max_keys: int = 1000
    ) -> List[Dict[str, Any]]:
        """
        List objects in a bucket with optional prefix

        Args:
            bucket_name: Name of the S3 bucket
            prefix: Prefix filter for objects
            max_keys: Maximum number of keys to return

        Returns:
            List of object dictionaries
        """
        try:
            objects = []
            paginator = self.s3_client.get_paginator('list_objects_v2')
            page_iterator = paginator.paginate(
                Bucket=bucket_name,
                Prefix=prefix,
                PaginationConfig={'MaxItems': max_keys}
            )

            for page in page_iterator:
                if 'Contents' in page:
                    for obj in page['Contents']:
                        objects.append({
                            'key': obj['Key'],
                            'size': obj['Size'],
                            'last_modified': obj['LastModified'],
                            'storage_class': obj.get('StorageClass', 'STANDARD')
                        })

            logger.info(f"Found {len(objects)} objects in {bucket_name} with prefix '{prefix}'")
            return objects
        except ClientError as e:
            logger.error(f"Error listing objects in {bucket_name}: {e}")
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def get_bucket_size(self, bucket_name: str, prefix: str = '') -> Dict[str, Any]:
        """
        Calculate bucket size and object count

        Args:
            bucket_name: Name of the S3 bucket
            prefix: Prefix filter for objects

        Returns:
            Dictionary with total size and count
        """
        try:
            total_size = 0
            object_count = 0

            paginator = self.s3_client.get_paginator('list_objects_v2')
            page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

            for page in page_iterator:
                if 'Contents' in page:
                    for obj in page['Contents']:
                        total_size += obj['Size']
                        object_count += 1

            result = {
                'bucket_name': bucket_name,
                'prefix': prefix,
                'total_size_bytes': total_size,
                'total_size_gb': round(total_size / (1024**3), 2),
                'object_count': object_count
            }
            logger.info(f"Bucket {bucket_name} size: {result['total_size_gb']} GB, {object_count} objects")
            return result
        except ClientError as e:
            logger.error(f"Error calculating bucket size for {bucket_name}: {e}")
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def upload_file(self, file_path: str, bucket_name: str, object_key: str) -> bool:
        """
        Upload file to S3

        Args:
            file_path: Local file path
            bucket_name: Name of the S3 bucket
            object_key: S3 object key

        Returns:
            True if successful
        """
        try:
            self.s3_client.upload_file(file_path, bucket_name, object_key)
            logger.info(f"Uploaded {file_path} to s3://{bucket_name}/{object_key}")
            return True
        except ClientError as e:
            logger.error(f"Error uploading file to {bucket_name}: {e}")
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def delete_object(self, bucket_name: str, object_key: str) -> bool:
        """
        Delete object from S3

        Args:
            bucket_name: Name of the S3 bucket
            object_key: S3 object key

        Returns:
            True if successful
        """
        try:
            self.s3_client.delete_object(Bucket=bucket_name, Key=object_key)
            logger.info(f"Deleted s3://{bucket_name}/{object_key}")
            return True
        except ClientError as e:
            logger.error(f"Error deleting object from {bucket_name}: {e}")
            raise

    def get_bucket_tags(self, bucket_name: str) -> Dict[str, str]:
        """
        Get bucket tags

        Args:
            bucket_name: Name of the S3 bucket

        Returns:
            Dictionary of tags
        """
        try:
            response = self.s3_client.get_bucket_tagging(Bucket=bucket_name)
            tags = {tag['Key']: tag['Value'] for tag in response.get('TagSet', [])}
            logger.info(f"Retrieved {len(tags)} tags for {bucket_name}")
            return tags
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchTagSet':
                logger.info(f"No tags for {bucket_name}")
                return {}
            logger.error(f"Error getting tags for {bucket_name}: {e}")
            raise
