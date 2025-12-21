"""Validation utilities for log files and policies."""

import re
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class LogValidator:
    """Validate log files and metadata."""

    @staticmethod
    def validate_log_key(key: str) -> bool:
        """Validate S3 object key format.

        Args:
            key: S3 object key

        Returns:
            True if valid, False otherwise
        """
        # Check for valid characters
        if not re.match(r'^[a-zA-Z0-9!_.*\'()/\-]+$', key):
            logger.warning(f"Invalid characters in key: {key}")
            return False

        # Check length
        if len(key) > 1024:
            logger.warning(f"Key too long: {len(key)} chars")
            return False

        return True

    @staticmethod
    def validate_log_format(content: bytes, format_type: str = 'json') -> bool:
        """Validate log file format.

        Args:
            content: Log file content
            format_type: Expected format (json, csv, txt)

        Returns:
            True if valid, False otherwise
        """
        if format_type == 'json':
            try:
                import json
                json.loads(content.decode('utf-8'))
                return True
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                logger.error(f"Invalid JSON: {e}")
                return False

        elif format_type == 'csv':
            try:
                import csv
                import io
                reader = csv.reader(io.StringIO(content.decode('utf-8')))
                list(reader)
                return True
            except (csv.Error, UnicodeDecodeError) as e:
                logger.error(f"Invalid CSV: {e}")
                return False

        return True

    @staticmethod
    def validate_retention_policy(policy: Dict) -> Dict[str, any]:
        """Validate lifecycle retention policy.

        Args:
            policy: Lifecycle policy dictionary

        Returns:
            Validation result dictionary
        """
        result = {
            'valid': True,
            'errors': [],
            'warnings': []
        }

        # Check required fields
        if 'Rules' not in policy:
            result['errors'].append("Missing 'Rules' field")
            result['valid'] = False
            return result

        for idx, rule in enumerate(policy['Rules']):
            rule_id = rule.get('ID', f'rule-{idx}')

            # Check rule status
            if 'Status' not in rule:
                result['errors'].append(f"Rule {rule_id}: Missing Status")
                result['valid'] = False

            # Validate transitions
            if 'Transitions' in rule:
                prev_days = 0
                for trans in rule['Transitions']:
                    days = trans.get('Days', 0)

                    if days <= prev_days:
                        result['errors'].append(
                            f"Rule {rule_id}: Transitions not in ascending order"
                        )
                        result['valid'] = False

                    if days < 30 and trans.get('StorageClass') == 'STANDARD_IA':
                        result['warnings'].append(
                            f"Rule {rule_id}: STANDARD_IA requires 30+ days"
                        )

                    prev_days = days

            # Check expiration
            if 'Expiration' in rule:
                exp_days = rule['Expiration'].get('Days', 0)
                if exp_days < 1:
                    result['errors'].append(
                        f"Rule {rule_id}: Invalid expiration days"
                    )
                    result['valid'] = False

        return result

    @staticmethod
    def validate_bucket_name(name: str) -> bool:
        """Validate S3 bucket name.

        Args:
            name: Bucket name

        Returns:
            True if valid, False otherwise
        """
        # Length check
        if len(name) < 3 or len(name) > 63:
            logger.error(f"Invalid bucket name length: {len(name)}")
            return False

        # Format check
        if not re.match(r'^[a-z0-9][a-z0-9\-]*[a-z0-9]$', name):
            logger.error(f"Invalid bucket name format: {name}")
            return False

        # IP address check
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', name):
            logger.error("Bucket name cannot be formatted as IP address")
            return False

        return True

    @staticmethod
    def validate_tags(tags: Dict[str, str]) -> bool:
        """Validate resource tags.

        Args:
            tags: Dictionary of tags

        Returns:
            True if valid, False otherwise
        """
        for key, value in tags.items():
            # Check key length
            if len(key) > 128:
                logger.error(f"Tag key too long: {key}")
                return False

            # Check value length
            if len(value) > 256:
                logger.error(f"Tag value too long for key {key}")
                return False

            # Check for aws: prefix (reserved)
            if key.lower().startswith('aws:'):
                logger.error(f"Tag key cannot start with 'aws:': {key}")
                return False

        return True
