"""
AWS Client Manager
Provides reusable AWS service clients with configuration and error handling
"""

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class AWSClientManager:
    """Manages AWS service clients with caching and configuration"""

    def __init__(self, region_name: str = "us-east-1", profile_name: Optional[str] = None):
        """
        Initialize AWS client manager
        
        Args:
            region_name: AWS region name
            profile_name: AWS profile name (optional)
        """
        self.region_name = region_name
        self.profile_name = profile_name
        self._session = None
        self._clients = {}

    @property
    def session(self) -> boto3.Session:
        """Get or create boto3 session"""
        if self._session is None:
            try:
                if self.profile_name:
                    self._session = boto3.Session(
                        profile_name=self.profile_name,
                        region_name=self.region_name
                    )
                else:
                    self._session = boto3.Session(region_name=self.region_name)
                logger.info(f"Created AWS session for region {self.region_name}")
            except NoCredentialsError:
                logger.error("AWS credentials not found")
                raise
        return self._session

    def get_client(self, service_name: str, **kwargs) -> Any:
        """
        Get or create AWS service client with caching
        
        Args:
            service_name: AWS service name (s3, cloudwatch, etc.)
            **kwargs: Additional client configuration
            
        Returns:
            Boto3 client instance
        """
        cache_key = f"{service_name}_{hash(frozenset(kwargs.items()))}"
        
        if cache_key not in self._clients:
            try:
                self._clients[cache_key] = self.session.client(
                    service_name,
                    **kwargs
                )
                logger.debug(f"Created {service_name} client")
            except ClientError as e:
                logger.error(f"Failed to create {service_name} client: {e}")
                raise
                
        return self._clients[cache_key]

    def get_s3_client(self):
        """Get S3 client"""
        return self.get_client("s3")

    def get_cloudwatch_client(self):
        """Get CloudWatch client"""
        return self.get_client("cloudwatch")

    def get_iam_client(self):
        """Get IAM client"""
        return self.get_client("iam")

    def get_cloudtrail_client(self):
        """Get CloudTrail client"""
        return self.get_client("cloudtrail")

    def get_sns_client(self):
        """Get SNS client"""
        return self.get_client("sns")

    def get_sts_client(self):
        """Get STS client"""
        return self.get_client("sts")

    def get_account_id(self) -> str:
        """Get current AWS account ID"""
        try:
            sts = self.get_sts_client()
            return sts.get_caller_identity()["Account"]
        except ClientError as e:
            logger.error(f"Failed to get account ID: {e}")
            raise
