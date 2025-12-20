"""S3 utility functions for log management."""

import logging
from typing import Dict, List, Optional
from datetime import datetime

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class S3LogManager:
    """Manage S3 log operations."""

    def __init__(self, bucket_name: str, region: Optional[str] = None):
        """Initialize S3 log manager.

        Args:
            bucket_name: Name of the S3 bucket
            region: AWS region (optional, uses default if not provided)
        """
        self.bucket_name = bucket_name
        self.region = region
        self.s3_client = boto3.client('s3', region_name=region)
        logger.info(f"Initialized S3LogManager for bucket: {bucket_name}")

    def list_logs(self, prefix: str = "", max_keys: int = 1000) -> List[Dict]:
        """List log files in the bucket.

        Args:
            prefix: Filter objects by prefix
            max_keys: Maximum number of keys to return

        Returns:
            List of object metadata dictionaries
        """
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix,
                MaxKeys=max_keys
            )
            objects = response.get('Contents', [])
            logger.info(f"Listed {len(objects)} objects with prefix: {prefix}")
            return objects
        except ClientError as e:
            logger.error(f"Error listing objects: {e}")
            raise

    def get_log_metadata(self, key: str) -> Dict:
        """Get metadata for a specific log file.

        Args:
            key: Object key

        Returns:
            Object metadata dictionary
        """
        try:
            response = self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=key
            )
            logger.debug(f"Retrieved metadata for: {key}")
            return response
        except ClientError as e:
            logger.error(f"Error getting object metadata: {e}")
            raise

    def get_storage_class(self, key: str) -> str:
        """Get the storage class of a log file.

        Args:
            key: Object key

        Returns:
            Storage class name (e.g., 'STANDARD', 'GLACIER')
        """
        metadata = self.get_log_metadata(key)
        return metadata.get('StorageClass', 'STANDARD')

    def upload_log(self, file_path: str, key: str, metadata: Optional[Dict] = None) -> bool:
        """Upload a log file to S3.

        Args:
            file_path: Local file path
            key: S3 object key
            metadata: Optional metadata to attach

        Returns:
            True if successful, False otherwise
        """
        try:
            extra_args = {}
            if metadata:
                extra_args['Metadata'] = metadata

            self.s3_client.upload_file(
                file_path,
                self.bucket_name,
                key,
                ExtraArgs=extra_args
            )
            logger.info(f"Uploaded {file_path} to s3://{self.bucket_name}/{key}")
            return True
        except ClientError as e:
            logger.error(f"Error uploading file: {e}")
            return False

    def delete_log(self, key: str) -> bool:
        """Delete a log file from S3.

        Args:
            key: Object key to delete

        Returns:
            True if successful, False otherwise
        """
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=key
            )
            logger.info(f"Deleted s3://{self.bucket_name}/{key}")
            return True
        except ClientError as e:
            logger.error(f"Error deleting object: {e}")
            return False

    def get_bucket_size(self, prefix: str = "") -> int:
        """Calculate total size of logs in bucket.

        Args:
            prefix: Filter objects by prefix

        Returns:
            Total size in bytes
        """
        total_size = 0
        paginator = self.s3_client.get_paginator('list_objects_v2')

        try:
            for page in paginator.paginate(Bucket=self.bucket_name, Prefix=prefix):
                for obj in page.get('Contents', []):
                    total_size += obj.get('Size', 0)

            logger.info(f"Total bucket size: {total_size} bytes")
            return total_size
        except ClientError as e:
            logger.error(f"Error calculating bucket size: {e}")
            raise

    def tag_object(self, key: str, tags: Dict[str, str]) -> bool:
        """Add tags to an S3 object.

        Args:
            key: Object key
            tags: Dictionary of tag key-value pairs

        Returns:
            True if successful, False otherwise
        """
        try:
            tag_set = [{'Key': k, 'Value': v} for k, v in tags.items()]
            self.s3_client.put_object_tagging(
                Bucket=self.bucket_name,
                Key=key,
                Tagging={'TagSet': tag_set}
            )
            logger.info(f"Tagged object {key} with {len(tags)} tags")
            return True
        except ClientError as e:
            logger.error(f"Error tagging object: {e}")
            return False

    def get_object_tags(self, key: str) -> Dict[str, str]:
        """Get tags for an S3 object.

        Args:
            key: Object key

        Returns:
            Dictionary of tag key-value pairs
        """
        try:
            response = self.s3_client.get_object_tagging(
                Bucket=self.bucket_name,
                Key=key
            )
            tags = {tag['Key']: tag['Value'] for tag in response.get('TagSet', [])}
            return tags
        except ClientError as e:
            logger.error(f"Error getting object tags: {e}")
            return {}
