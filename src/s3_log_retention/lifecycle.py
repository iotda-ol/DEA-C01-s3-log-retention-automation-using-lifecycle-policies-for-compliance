"""Lifecycle policy management for S3 buckets."""

import logging
from typing import Dict, List, Optional

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class LifecyclePolicyManager:
    """Manage S3 bucket lifecycle policies."""

    def __init__(self, bucket_name: str, region: Optional[str] = None):
        """Initialize lifecycle policy manager.

        Args:
            bucket_name: Name of the S3 bucket
            region: AWS region (optional)
        """
        self.bucket_name = bucket_name
        self.region = region
        self.s3_client = boto3.client('s3', region_name=region)
        logger.info(f"Initialized LifecyclePolicyManager for bucket: {bucket_name}")

    def create_retention_policy(
        self,
        rule_id: str,
        prefix: str = "",
        expiration_days: int = 365,
        transitions: Optional[List[Dict]] = None
    ) -> bool:
        """Create a lifecycle retention policy.

        Args:
            rule_id: Unique identifier for the rule
            prefix: Object prefix to apply rule to
            expiration_days: Days until objects are deleted
            transitions: List of storage class transitions

        Returns:
            True if successful, False otherwise

        Example:
            transitions = [
                {'Days': 30, 'StorageClass': 'STANDARD_IA'},
                {'Days': 90, 'StorageClass': 'GLACIER'},
            ]
        """
        rule = {
            'ID': rule_id,
            'Status': 'Enabled',
            'Filter': {'Prefix': prefix},
            'Expiration': {'Days': expiration_days}
        }

        if transitions:
            rule['Transitions'] = transitions

        try:
            # Get existing lifecycle configuration
            existing_rules = self.get_lifecycle_rules()

            # Add or update the rule
            rules = [r for r in existing_rules if r.get('ID') != rule_id]
            rules.append(rule)

            # Put the lifecycle configuration
            self.s3_client.put_bucket_lifecycle_configuration(
                Bucket=self.bucket_name,
                LifecycleConfiguration={'Rules': rules}
            )
            logger.info(f"Created/updated lifecycle rule: {rule_id}")
            return True
        except ClientError as e:
            logger.error(f"Error creating lifecycle policy: {e}")
            return False

    def get_lifecycle_rules(self) -> List[Dict]:
        """Get all lifecycle rules for the bucket.

        Returns:
            List of lifecycle rule dictionaries
        """
        try:
            response = self.s3_client.get_bucket_lifecycle_configuration(
                Bucket=self.bucket_name
            )
            rules = response.get('Rules', [])
            logger.info(f"Retrieved {len(rules)} lifecycle rules")
            return rules
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchLifecycleConfiguration':
                logger.info("No lifecycle configuration exists")
                return []
            logger.error(f"Error getting lifecycle configuration: {e}")
            raise

    def delete_lifecycle_rule(self, rule_id: str) -> bool:
        """Delete a specific lifecycle rule.

        Args:
            rule_id: ID of the rule to delete

        Returns:
            True if successful, False otherwise
        """
        try:
            existing_rules = self.get_lifecycle_rules()
            rules = [r for r in existing_rules if r.get('ID') != rule_id]

            if len(rules) == len(existing_rules):
                logger.warning(f"Rule {rule_id} not found")
                return False

            if rules:
                self.s3_client.put_bucket_lifecycle_configuration(
                    Bucket=self.bucket_name,
                    LifecycleConfiguration={'Rules': rules}
                )
            else:
                # Delete entire lifecycle configuration if no rules left
                self.s3_client.delete_bucket_lifecycle(Bucket=self.bucket_name)

            logger.info(f"Deleted lifecycle rule: {rule_id}")
            return True
        except ClientError as e:
            logger.error(f"Error deleting lifecycle rule: {e}")
            return False

    def create_compliance_policy(
        self,
        log_type: str,
        retention_days: int,
        archive_days: int = 30
    ) -> bool:
        """Create a compliance-focused lifecycle policy.

        Args:
            log_type: Type of logs (e.g., 'access', 'application', 'audit')
            retention_days: Days to retain logs before deletion
            archive_days: Days before moving to archive storage

        Returns:
            True if successful, False otherwise
        """
        transitions = []

        # Standard IA after 30 days (or custom archive_days)
        if archive_days < retention_days:
            transitions.append({
                'Days': archive_days,
                'StorageClass': 'STANDARD_IA'
            })

        # Glacier after 90 days if retention allows
        if retention_days > 90:
            glacier_days = max(90, archive_days + 30)
            transitions.append({
                'Days': glacier_days,
                'StorageClass': 'GLACIER'
            })

        # Glacier Deep Archive after 180 days if retention allows
        if retention_days > 180:
            deep_archive_days = max(180, archive_days + 60)
            transitions.append({
                'Days': deep_archive_days,
                'StorageClass': 'DEEP_ARCHIVE'
            })

        rule_id = f"compliance-{log_type}-{retention_days}d"
        prefix = f"logs/{log_type}/"

        return self.create_retention_policy(
            rule_id=rule_id,
            prefix=prefix,
            expiration_days=retention_days,
            transitions=transitions
        )

    def validate_policy(self) -> Dict[str, any]:
        """Validate the current lifecycle policy.

        Returns:
            Dictionary with validation results
        """
        result = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'rule_count': 0
        }

        try:
            rules = self.get_lifecycle_rules()
            result['rule_count'] = len(rules)

            for rule in rules:
                rule_id = rule.get('ID', 'unknown')

                # Check for required fields
                if 'Status' not in rule:
                    result['errors'].append(f"Rule {rule_id} missing Status")
                    result['valid'] = False

                # Validate transitions
                if 'Transitions' in rule:
                    prev_days = 0
                    for transition in rule['Transitions']:
                        days = transition.get('Days', 0)
                        if days <= prev_days:
                            result['errors'].append(
                                f"Rule {rule_id}: Transition days not in ascending order"
                            )
                            result['valid'] = False
                        prev_days = days

                # Warn about missing expiration
                if 'Expiration' not in rule and 'NoncurrentVersionExpiration' not in rule:
                    result['warnings'].append(
                        f"Rule {rule_id}: No expiration configured"
                    )

            logger.info(f"Policy validation complete: {result}")
            return result
        except ClientError as e:
            logger.error(f"Error validating policy: {e}")
            result['valid'] = False
            result['errors'].append(str(e))
            return result
