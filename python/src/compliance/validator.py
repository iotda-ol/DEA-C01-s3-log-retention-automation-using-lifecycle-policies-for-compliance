"""
Compliance Validation Module
Validates S3 configurations against compliance requirements
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class ComplianceRequirement:
    """Compliance requirement definition"""
    name: str
    description: str
    required: bool = True


class ComplianceValidator:
    """Validator for S3 compliance requirements"""

    def __init__(self, required_retention_days: int = 365):
        """
        Initialize compliance validator

        Args:
            required_retention_days: Minimum retention period in days
        """
        self.required_retention_days = required_retention_days
        logger.info(f"Compliance validator initialized with {required_retention_days} days retention")

    def validate_lifecycle_policy(self, policy: Optional[Dict]) -> Tuple[bool, List[str]]:
        """
        Validate lifecycle policy meets compliance requirements

        Args:
            policy: Lifecycle policy configuration

        Returns:
            Tuple of (is_compliant, list of issues)
        """
        issues = []

        if not policy or 'Rules' not in policy:
            issues.append("No lifecycle policy configured")
            return False, issues

        rules = policy.get('Rules', [])

        if not rules:
            issues.append("Lifecycle policy has no rules")
            return False, issues

        # Check for expiration rule
        has_expiration = False
        max_expiration = 0

        for rule in rules:
            if rule.get('Status') == 'Enabled':
                if 'Expiration' in rule:
                    has_expiration = True
                    days = rule['Expiration'].get('Days', 0)
                    max_expiration = max(max_expiration, days)

        if not has_expiration:
            issues.append("No expiration rule found")

        if max_expiration < self.required_retention_days:
            issues.append(
                f"Retention period ({max_expiration} days) is less than "
                f"required ({self.required_retention_days} days)"
            )

        is_compliant = len(issues) == 0
        logger.info(f"Policy validation: {'PASS' if is_compliant else 'FAIL'}")

        return is_compliant, issues

    def validate_encryption(self, encryption_config: Optional[Dict]) -> Tuple[bool, List[str]]:
        """
        Validate bucket encryption configuration

        Args:
            encryption_config: Bucket encryption configuration

        Returns:
            Tuple of (is_compliant, list of issues)
        """
        issues = []

        if not encryption_config:
            issues.append("Encryption not enabled")
            return False, issues

        rules = encryption_config.get('Rules', [])

        if not rules:
            issues.append("No encryption rules configured")
            return False, issues

        # Check for SSE
        has_sse = False
        for rule in rules:
            sse_config = rule.get('ApplyServerSideEncryptionByDefault', {})
            if sse_config.get('SSEAlgorithm'):
                has_sse = True
                break

        if not has_sse:
            issues.append("Server-side encryption not configured")

        is_compliant = len(issues) == 0
        logger.info(f"Encryption validation: {'PASS' if is_compliant else 'FAIL'}")

        return is_compliant, issues

    def validate_versioning(self, versioning_config: Optional[Dict]) -> Tuple[bool, List[str]]:
        """
        Validate bucket versioning configuration

        Args:
            versioning_config: Bucket versioning configuration

        Returns:
            Tuple of (is_compliant, list of issues)
        """
        issues = []

        if not versioning_config:
            issues.append("Versioning configuration not found")
            return False, issues

        status = versioning_config.get('Status', 'Disabled')

        if status != 'Enabled':
            issues.append(f"Versioning is {status}, should be Enabled")

        is_compliant = len(issues) == 0
        logger.info(f"Versioning validation: {'PASS' if is_compliant else 'FAIL'}")

        return is_compliant, issues

    def validate_public_access_block(self, public_access_config: Optional[Dict]) -> Tuple[bool, List[str]]:
        """
        Validate public access block configuration

        Args:
            public_access_config: Public access block configuration

        Returns:
            Tuple of (is_compliant, list of issues)
        """
        issues = []

        if not public_access_config:
            issues.append("Public access block not configured")
            return False, issues

        required_blocks = {
            'BlockPublicAcls': True,
            'IgnorePublicAcls': True,
            'BlockPublicPolicy': True,
            'RestrictPublicBuckets': True
        }

        for key, required_value in required_blocks.items():
            actual_value = public_access_config.get(key, False)
            if actual_value != required_value:
                issues.append(f"{key} should be {required_value}, is {actual_value}")

        is_compliant = len(issues) == 0
        logger.info(f"Public access block validation: {'PASS' if is_compliant else 'FAIL'}")

        return is_compliant, issues

    def validate_bucket(self, bucket_name: str, s3_client) -> Dict:
        """
        Perform comprehensive bucket compliance validation

        Args:
            bucket_name: Name of the bucket to validate
            s3_client: Boto3 S3 client

        Returns:
            Validation results dictionary
        """
        logger.info(f"Validating bucket: {bucket_name}")

        results = {
            'bucket': bucket_name,
            'compliant': True,
            'checks': {}
        }

        # Check lifecycle policy
        try:
            lifecycle = s3_client.get_bucket_lifecycle_configuration(Bucket=bucket_name)
        except:
            lifecycle = None

        is_compliant, issues = self.validate_lifecycle_policy(lifecycle)
        results['checks']['lifecycle'] = {
            'compliant': is_compliant,
            'issues': issues
        }
        if not is_compliant:
            results['compliant'] = False

        # Check encryption
        try:
            encryption = s3_client.get_bucket_encryption(Bucket=bucket_name)
        except:
            encryption = None

        is_compliant, issues = self.validate_encryption(encryption)
        results['checks']['encryption'] = {
            'compliant': is_compliant,
            'issues': issues
        }
        if not is_compliant:
            results['compliant'] = False

        # Check versioning
        try:
            versioning = s3_client.get_bucket_versioning(Bucket=bucket_name)
        except:
            versioning = None

        is_compliant, issues = self.validate_versioning(versioning)
        results['checks']['versioning'] = {
            'compliant': is_compliant,
            'issues': issues
        }
        if not is_compliant:
            results['compliant'] = False

        # Check public access block
        try:
            public_access = s3_client.get_public_access_block(Bucket=bucket_name)
            public_access = public_access.get('PublicAccessBlockConfiguration', {})
        except:
            public_access = None

        is_compliant, issues = self.validate_public_access_block(public_access)
        results['checks']['public_access'] = {
            'compliant': is_compliant,
            'issues': issues
        }
        if not is_compliant:
            results['compliant'] = False

        logger.info(f"Bucket {bucket_name} compliance: {'PASS' if results['compliant'] else 'FAIL'}")

        return results

    def get_requirements(self) -> List[ComplianceRequirement]:
        """
        Get list of compliance requirements

        Returns:
            List of compliance requirements
        """
        return [
            ComplianceRequirement(
                name="Lifecycle Policy",
                description=f"Objects must be deleted after {self.required_retention_days} days",
                required=True
            ),
            ComplianceRequirement(
                name="Encryption at Rest",
                description="Server-side encryption must be enabled",
                required=True
            ),
            ComplianceRequirement(
                name="Versioning",
                description="Bucket versioning should be enabled",
                required=True
            ),
            ComplianceRequirement(
                name="Public Access Block",
                description="All public access must be blocked",
                required=True
            ),
            ComplianceRequirement(
                name="Access Logging",
                description="Access logging should be enabled for audit",
                required=False
            )
        ]
