"""
Policy Validator Module
Validates S3 lifecycle policies for compliance
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class PolicyValidator:
    """Validates S3 lifecycle policies against compliance requirements"""

    def __init__(self, min_retention_days: int = 365):
        """
        Initialize policy validator

        Args:
            min_retention_days: Minimum retention period required for compliance
        """
        self.min_retention_days = min_retention_days
        logger.info(f"Initialized PolicyValidator with min retention: {min_retention_days} days")

    def validate_lifecycle_policy(self, policy: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate lifecycle policy configuration

        Args:
            policy: Lifecycle policy configuration from S3

        Returns:
            Validation result with status and issues
        """
        issues = []
        warnings = []

        if not policy:
            return {
                'valid': False,
                'issues': ['No lifecycle policy configured'],
                'warnings': [],
                'compliant': False
            }

        rules = policy.get('Rules', [])
        if not rules:
            issues.append('No lifecycle rules defined')

        for rule in rules:
            rule_id = rule.get('ID', 'Unknown')
            rule_issues = self._validate_rule(rule)
            issues.extend([f"Rule '{rule_id}': {issue}" for issue in rule_issues])

            # Check for warnings
            if rule.get('Status') != 'Enabled':
                warnings.append(f"Rule '{rule_id}' is not enabled")

        # Check compliance
        compliant = self._check_compliance(rules)

        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings,
            'compliant': compliant,
            'rules_count': len(rules)
        }

    def _validate_rule(self, rule: Dict[str, Any]) -> List[str]:
        """
        Validate individual lifecycle rule

        Args:
            rule: Lifecycle rule configuration

        Returns:
            List of validation issues
        """
        issues = []

        # Check if rule has ID
        if 'ID' not in rule:
            issues.append('Rule missing ID')

        # Check if rule has status
        if 'Status' not in rule:
            issues.append('Rule missing Status')

        # Validate expiration configuration
        if 'Expiration' in rule:
            expiration = rule['Expiration']
            if 'Days' in expiration:
                days = expiration['Days']
                if days < self.min_retention_days:
                    issues.append(
                        f'Expiration period ({days} days) is less than '
                        f'required minimum ({self.min_retention_days} days)'
                    )
            elif 'Date' not in expiration:
                issues.append('Expiration missing both Days and Date')

        # Validate transitions
        if 'Transitions' in rule:
            transition_issues = self._validate_transitions(rule['Transitions'])
            issues.extend(transition_issues)

        # Check noncurrent version expiration
        if 'NoncurrentVersionExpiration' in rule:
            nc_exp = rule['NoncurrentVersionExpiration']
            if 'NoncurrentDays' in nc_exp:
                nc_days = nc_exp['NoncurrentDays']
                if nc_days > self.min_retention_days:
                    issues.append(
                        f'Noncurrent version expiration ({nc_days} days) exceeds '
                        f'maximum allowed ({self.min_retention_days} days)'
                    )

        return issues

    def _validate_transitions(self, transitions: List[Dict[str, Any]]) -> List[str]:
        """
        Validate lifecycle transitions

        Args:
            transitions: List of transition configurations

        Returns:
            List of validation issues
        """
        issues = []
        valid_storage_classes = [
            'STANDARD_IA',
            'INTELLIGENT_TIERING',
            'ONEZONE_IA',
            'GLACIER',
            'GLACIER_IR',
            'DEEP_ARCHIVE'
        ]

        previous_days = 0
        for idx, transition in enumerate(transitions):
            # Validate storage class
            storage_class = transition.get('StorageClass')
            if storage_class not in valid_storage_classes:
                issues.append(f'Invalid storage class: {storage_class}')

            # Validate transition days
            if 'Days' in transition:
                days = transition['Days']
                if days <= previous_days:
                    issues.append(
                        f'Transition {idx + 1} days ({days}) must be greater than '
                        f'previous transition ({previous_days})'
                    )
                previous_days = days

                # Check minimum transition periods
                if storage_class in ['STANDARD_IA', 'INTELLIGENT_TIERING']:
                    if days < 30:
                        issues.append(
                            f'Transition to {storage_class} requires minimum 30 days'
                        )
                elif storage_class == 'GLACIER':
                    if days < 90:
                        issues.append(
                            f'Recommended minimum for {storage_class} is 90 days'
                        )

        return issues

    def _check_compliance(self, rules: List[Dict[str, Any]]) -> bool:
        """
        Check if lifecycle policy meets compliance requirements

        Args:
            rules: List of lifecycle rules

        Returns:
            True if compliant, False otherwise
        """
        # Check if at least one enabled rule has proper expiration
        for rule in rules:
            if rule.get('Status') != 'Enabled':
                continue

            if 'Expiration' in rule:
                expiration = rule['Expiration']
                if 'Days' in expiration:
                    days = expiration['Days']
                    if days >= self.min_retention_days:
                        return True

        return False

    def validate_bucket_policy(self, bucket_policy: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate S3 bucket policy for security best practices

        Args:
            bucket_policy: S3 bucket policy document

        Returns:
            Validation result
        """
        issues = []
        warnings = []

        if not bucket_policy:
            warnings.append('No bucket policy configured')
            return {
                'valid': True,
                'issues': [],
                'warnings': warnings
            }

        statements = bucket_policy.get('Statement', [])

        for statement in statements:
            # Check for overly permissive policies
            if statement.get('Principal') == '*':
                if statement.get('Effect') == 'Allow':
                    issues.append('Policy allows public access with Principal: *')

            # Check for secure transport
            condition = statement.get('Condition', {})
            if not any('SecureTransport' in str(c) for c in condition.values()):
                warnings.append('Policy does not enforce secure transport (SSL/TLS)')

        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings
        }

    def generate_compliance_report(
        self,
        bucket_name: str,
        lifecycle_policy: Optional[Dict[str, Any]],
        bucket_policy: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate comprehensive compliance report

        Args:
            bucket_name: Name of the S3 bucket
            lifecycle_policy: Lifecycle policy configuration
            bucket_policy: Bucket policy configuration

        Returns:
            Compliance report
        """
        lifecycle_validation = self.validate_lifecycle_policy(lifecycle_policy or {})
        policy_validation = self.validate_bucket_policy(bucket_policy or {})

        overall_compliant = (
            lifecycle_validation['compliant'] and
            policy_validation['valid']
        )

        return {
            'bucket_name': bucket_name,
            'timestamp': datetime.utcnow().isoformat(),
            'overall_compliant': overall_compliant,
            'lifecycle_policy': lifecycle_validation,
            'bucket_policy': policy_validation,
            'min_retention_days': self.min_retention_days
        }
