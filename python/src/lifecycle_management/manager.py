"""
Lifecycle Management Module
Handles S3 lifecycle policy operations
"""

import boto3
from typing import Dict, List, Optional
from botocore.exceptions import ClientError
import logging
import json

logger = logging.getLogger(__name__)


class LifecycleManager:
    """Manager for S3 lifecycle policies"""

    def __init__(self, s3_client=None, region: str = 'us-east-1'):
        """
        Initialize lifecycle manager

        Args:
            s3_client: Boto3 S3 client (creates new if None)
            region: AWS region
        """
        self.s3 = s3_client or boto3.client('s3', region_name=region)
        self.region = region
        logger.info("Lifecycle manager initialized")

    def get_lifecycle_policy(self, bucket: str) -> Optional[Dict]:
        """
        Get lifecycle configuration for a bucket

        Args:
            bucket: Bucket name

        Returns:
            Lifecycle configuration dict or None if not configured
        """
        try:
            response = self.s3.get_bucket_lifecycle_configuration(Bucket=bucket)
            logger.info(f"Retrieved lifecycle policy for {bucket}")
            return response
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchLifecycleConfiguration':
                logger.info(f"No lifecycle policy found for {bucket}")
                return None
            logger.error(f"Error getting lifecycle policy: {e}")
            raise

    def set_lifecycle_policy(self, bucket: str, rules: List[Dict]) -> bool:
        """
        Set lifecycle configuration for a bucket

        Args:
            bucket: Bucket name
            rules: List of lifecycle rules

        Returns:
            True if successful
        """
        try:
            self.s3.put_bucket_lifecycle_configuration(
                Bucket=bucket,
                LifecycleConfiguration={'Rules': rules}
            )
            logger.info(f"Set lifecycle policy for {bucket}")
            return True
        except ClientError as e:
            logger.error(f"Error setting lifecycle policy: {e}")
            raise

    def delete_lifecycle_policy(self, bucket: str) -> bool:
        """
        Delete lifecycle configuration from a bucket

        Args:
            bucket: Bucket name

        Returns:
            True if successful
        """
        try:
            self.s3.delete_bucket_lifecycle(Bucket=bucket)
            logger.info(f"Deleted lifecycle policy from {bucket}")
            return True
        except ClientError as e:
            logger.error(f"Error deleting lifecycle policy: {e}")
            raise

    def create_retention_rule(self, rule_id: str, retention_days: int,
                             prefix: str = '', status: str = 'Enabled') -> Dict:
        """
        Create a simple retention rule

        Args:
            rule_id: Unique rule identifier
            retention_days: Days to retain objects
            prefix: Object key prefix filter
            status: Rule status (Enabled/Disabled)

        Returns:
            Lifecycle rule dictionary
        """
        rule = {
            'ID': rule_id,
            'Status': status,
            'Expiration': {
                'Days': retention_days
            }
        }

        if prefix:
            rule['Prefix'] = prefix

        logger.info(f"Created retention rule: {rule_id}")
        return rule

    def create_transition_rule(self, rule_id: str, transitions: List[Dict],
                              expiration_days: Optional[int] = None,
                              prefix: str = '', status: str = 'Enabled') -> Dict:
        """
        Create a rule with storage class transitions

        Args:
            rule_id: Unique rule identifier
            transitions: List of transition configurations
            expiration_days: Optional expiration in days
            prefix: Object key prefix filter
            status: Rule status

        Returns:
            Lifecycle rule dictionary
        """
        rule = {
            'ID': rule_id,
            'Status': status,
            'Transitions': transitions
        }

        if prefix:
            rule['Prefix'] = prefix

        if expiration_days:
            rule['Expiration'] = {'Days': expiration_days}

        logger.info(f"Created transition rule: {rule_id}")
        return rule

    def create_compliance_rule(self, retention_days: int = 365,
                              enable_glacier: bool = True,
                              glacier_days: int = 90,
                              enable_ia: bool = True,
                              ia_days: int = 30) -> Dict:
        """
        Create a compliance-focused lifecycle rule

        Args:
            retention_days: Total retention period
            enable_glacier: Enable Glacier transition
            glacier_days: Days before Glacier transition
            enable_ia: Enable IA transition
            ia_days: Days before IA transition

        Returns:
            Compliance lifecycle rule
        """
        transitions = []

        if enable_ia:
            transitions.append({
                'Days': ia_days,
                'StorageClass': 'STANDARD_IA'
            })

        if enable_glacier:
            transitions.append({
                'Days': glacier_days,
                'StorageClass': 'GLACIER'
            })

        rule = {
            'ID': 'compliance-retention-policy',
            'Status': 'Enabled',
            'Expiration': {
                'Days': retention_days
            }
        }

        if transitions:
            rule['Transitions'] = transitions

        logger.info("Created compliance rule")
        return rule

    def validate_rule(self, rule: Dict) -> bool:
        """
        Validate a lifecycle rule structure

        Args:
            rule: Lifecycle rule dictionary

        Returns:
            True if valid

        Raises:
            ValueError if invalid
        """
        required_fields = ['ID', 'Status']

        for field in required_fields:
            if field not in rule:
                raise ValueError(f"Missing required field: {field}")

        if rule['Status'] not in ['Enabled', 'Disabled']:
            raise ValueError("Status must be Enabled or Disabled")

        # Must have at least one action
        has_action = any(key in rule for key in 
                        ['Expiration', 'Transitions', 'NoncurrentVersionExpiration'])

        if not has_action:
            raise ValueError("Rule must have at least one action")

        logger.info(f"Rule {rule['ID']} is valid")
        return True

    def export_policy(self, bucket: str, file_path: str) -> bool:
        """
        Export lifecycle policy to JSON file

        Args:
            bucket: Bucket name
            file_path: Output file path

        Returns:
            True if successful
        """
        try:
            policy = self.get_lifecycle_policy(bucket)
            if policy:
                with open(file_path, 'w') as f:
                    json.dump(policy, f, indent=2)
                logger.info(f"Exported policy to {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error exporting policy: {e}")
            raise

    def import_policy(self, bucket: str, file_path: str) -> bool:
        """
        Import lifecycle policy from JSON file

        Args:
            bucket: Bucket name
            file_path: Input file path

        Returns:
            True if successful
        """
        try:
            with open(file_path, 'r') as f:
                policy = json.load(f)

            rules = policy.get('Rules', [])
            return self.set_lifecycle_policy(bucket, rules)
        except Exception as e:
            logger.error(f"Error importing policy: {e}")
            raise
