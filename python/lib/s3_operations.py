"""
S3 Operations Module
Reusable S3 operations for log management
"""

from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger(__name__)


class S3Operations:
    """Handles S3 operations for log management"""

    def __init__(self, s3_client):
        """
        Initialize S3 operations
        
        Args:
            s3_client: Boto3 S3 client
        """
        self.s3 = s3_client

    def create_bucket(self, bucket_name: str, region: str = "us-east-1") -> bool:
        """
        Create S3 bucket
        
        Args:
            bucket_name: Name of the bucket
            region: AWS region
            
        Returns:
            True if successful
        """
        try:
            if region == "us-east-1":
                self.s3.create_bucket(Bucket=bucket_name)
            else:
                self.s3.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={"LocationConstraint": region}
                )
            logger.info(f"Created bucket: {bucket_name}")
            return True
        except ClientError as e:
            logger.error(f"Failed to create bucket {bucket_name}: {e}")
            return False

    def bucket_exists(self, bucket_name: str) -> bool:
        """
        Check if bucket exists
        
        Args:
            bucket_name: Name of the bucket
            
        Returns:
            True if bucket exists
        """
        try:
            self.s3.head_bucket(Bucket=bucket_name)
            return True
        except ClientError:
            return False

    def enable_versioning(self, bucket_name: str) -> bool:
        """
        Enable versioning on bucket
        
        Args:
            bucket_name: Name of the bucket
            
        Returns:
            True if successful
        """
        try:
            self.s3.put_bucket_versioning(
                Bucket=bucket_name,
                VersioningConfiguration={"Status": "Enabled"}
            )
            logger.info(f"Enabled versioning on {bucket_name}")
            return True
        except ClientError as e:
            logger.error(f"Failed to enable versioning on {bucket_name}: {e}")
            return False

    def put_lifecycle_policy(self, bucket_name: str, rules: List[Dict]) -> bool:
        """
        Apply lifecycle policy to bucket
        
        Args:
            bucket_name: Name of the bucket
            rules: List of lifecycle rules
            
        Returns:
            True if successful
        """
        try:
            self.s3.put_bucket_lifecycle_configuration(
                Bucket=bucket_name,
                LifecycleConfiguration={"Rules": rules}
            )
            logger.info(f"Applied lifecycle policy to {bucket_name}")
            return True
        except ClientError as e:
            logger.error(f"Failed to apply lifecycle policy to {bucket_name}: {e}")
            return False

    def get_lifecycle_policy(self, bucket_name: str) -> Optional[Dict]:
        """
        Get current lifecycle policy
        
        Args:
            bucket_name: Name of the bucket
            
        Returns:
            Lifecycle configuration dict or None
        """
        try:
            response = self.s3.get_bucket_lifecycle_configuration(Bucket=bucket_name)
            return response.get("Rules", [])
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchLifecycleConfiguration":
                logger.info(f"No lifecycle policy found for {bucket_name}")
                return None
            logger.error(f"Failed to get lifecycle policy for {bucket_name}: {e}")
            return None

    def list_objects(
        self, bucket_name: str, prefix: str = "", max_keys: int = 1000
    ) -> List[Dict]:
        """
        List objects in bucket
        
        Args:
            bucket_name: Name of the bucket
            prefix: Object key prefix filter
            max_keys: Maximum number of keys to return
            
        Returns:
            List of object metadata dicts
        """
        objects = []
        try:
            paginator = self.s3.get_paginator("list_objects_v2")
            pages = paginator.paginate(
                Bucket=bucket_name,
                Prefix=prefix,
                PaginationConfig={"MaxItems": max_keys}
            )
            
            for page in pages:
                objects.extend(page.get("Contents", []))
                
            logger.info(f"Listed {len(objects)} objects from {bucket_name}")
            return objects
        except ClientError as e:
            logger.error(f"Failed to list objects in {bucket_name}: {e}")
            return []

    def get_bucket_size(self, bucket_name: str, prefix: str = "") -> int:
        """
        Calculate total size of bucket or prefix
        
        Args:
            bucket_name: Name of the bucket
            prefix: Object key prefix filter
            
        Returns:
            Total size in bytes
        """
        total_size = 0
        try:
            paginator = self.s3.get_paginator("list_objects_v2")
            pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)
            
            for page in pages:
                for obj in page.get("Contents", []):
                    total_size += obj.get("Size", 0)
                    
            logger.info(f"Bucket {bucket_name} size: {total_size} bytes")
            return total_size
        except ClientError as e:
            logger.error(f"Failed to calculate bucket size for {bucket_name}: {e}")
            return 0

    def delete_old_objects(
        self, bucket_name: str, days: int, prefix: str = "", dry_run: bool = True
    ) -> int:
        """
        Delete objects older than specified days
        
        Args:
            bucket_name: Name of the bucket
            days: Delete objects older than this many days
            prefix: Object key prefix filter
            dry_run: If True, only report what would be deleted
            
        Returns:
            Number of objects deleted (or would be deleted in dry run)
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        deleted_count = 0
        
        try:
            objects = self.list_objects(bucket_name, prefix)
            
            for obj in objects:
                last_modified = obj.get("LastModified")
                if last_modified and last_modified.replace(tzinfo=None) < cutoff_date:
                    if not dry_run:
                        self.s3.delete_object(Bucket=bucket_name, Key=obj["Key"])
                        logger.debug(f"Deleted {obj['Key']}")
                    else:
                        logger.debug(f"Would delete {obj['Key']}")
                    deleted_count += 1
                    
            action = "Would delete" if dry_run else "Deleted"
            logger.info(f"{action} {deleted_count} objects from {bucket_name}")
            return deleted_count
        except ClientError as e:
            logger.error(f"Failed to delete old objects from {bucket_name}: {e}")
            return 0

    def upload_file(
        self, file_path: str, bucket_name: str, object_key: str, metadata: Optional[Dict] = None
    ) -> bool:
        """
        Upload file to S3
        
        Args:
            file_path: Local file path
            bucket_name: Name of the bucket
            object_key: S3 object key
            metadata: Optional metadata dict
            
        Returns:
            True if successful
        """
        try:
            extra_args = {}
            if metadata:
                extra_args["Metadata"] = metadata
                
            self.s3.upload_file(file_path, bucket_name, object_key, ExtraArgs=extra_args)
            logger.info(f"Uploaded {file_path} to s3://{bucket_name}/{object_key}")
            return True
        except ClientError as e:
            logger.error(f"Failed to upload {file_path}: {e}")
            return False
