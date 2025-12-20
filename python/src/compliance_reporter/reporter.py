"""
Compliance Reporter Module
Generates compliance reports for S3 log retention
"""

import logging
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from tabulate import tabulate

logger = logging.getLogger(__name__)


class ComplianceReporter:
    """Generates compliance reports for S3 buckets"""

    def __init__(self, s3_client, policy_validator):
        """
        Initialize compliance reporter

        Args:
            s3_client: S3Client instance
            policy_validator: PolicyValidator instance
        """
        self.s3_client = s3_client
        self.policy_validator = policy_validator
        logger.info("Initialized ComplianceReporter")

    def generate_bucket_report(self, bucket_name: str) -> Dict[str, Any]:
        """
        Generate compliance report for a single bucket

        Args:
            bucket_name: Name of the S3 bucket

        Returns:
            Compliance report dictionary
        """
        logger.info(f"Generating compliance report for {bucket_name}")

        # Get lifecycle configuration
        lifecycle_config = self.s3_client.get_lifecycle_configuration(bucket_name)

        # Get bucket size and object count
        bucket_stats = self.s3_client.get_bucket_size(bucket_name)

        # Get bucket tags
        tags = self.s3_client.get_bucket_tags(bucket_name)

        # Validate lifecycle policy
        validation_result = self.policy_validator.validate_lifecycle_policy(
            lifecycle_config or {}
        )

        report = {
            'bucket_name': bucket_name,
            'timestamp': datetime.utcnow().isoformat(),
            'statistics': bucket_stats,
            'tags': tags,
            'lifecycle_policy': {
                'configured': lifecycle_config is not None,
                'validation': validation_result
            },
            'compliant': validation_result['compliant']
        }

        return report

    def generate_multi_bucket_report(self, bucket_names: List[str]) -> Dict[str, Any]:
        """
        Generate compliance report for multiple buckets

        Args:
            bucket_names: List of bucket names

        Returns:
            Multi-bucket compliance report
        """
        logger.info(f"Generating compliance report for {len(bucket_names)} buckets")

        bucket_reports = []
        compliant_count = 0
        non_compliant_count = 0

        for bucket_name in bucket_names:
            try:
                report = self.generate_bucket_report(bucket_name)
                bucket_reports.append(report)

                if report['compliant']:
                    compliant_count += 1
                else:
                    non_compliant_count += 1

            except Exception as e:
                logger.error(f"Error generating report for {bucket_name}: {e}")
                bucket_reports.append({
                    'bucket_name': bucket_name,
                    'error': str(e),
                    'compliant': False
                })
                non_compliant_count += 1

        summary = {
            'total_buckets': len(bucket_names),
            'compliant_buckets': compliant_count,
            'non_compliant_buckets': non_compliant_count,
            'compliance_rate': round(
                (compliant_count / len(bucket_names) * 100) if bucket_names else 0,
                2
            )
        }

        return {
            'timestamp': datetime.utcnow().isoformat(),
            'summary': summary,
            'buckets': bucket_reports
        }

    def format_report_text(self, report: Dict[str, Any]) -> str:
        """
        Format compliance report as human-readable text

        Args:
            report: Compliance report dictionary

        Returns:
            Formatted text report
        """
        lines = []
        lines.append("=" * 80)
        lines.append("S3 Log Retention Compliance Report")
        lines.append("=" * 80)
        lines.append(f"Generated: {report['timestamp']}")
        lines.append("")

        if 'summary' in report:
            # Multi-bucket report
            summary = report['summary']
            lines.append("Summary:")
            lines.append(f"  Total Buckets: {summary['total_buckets']}")
            lines.append(f"  Compliant: {summary['compliant_buckets']}")
            lines.append(f"  Non-Compliant: {summary['non_compliant_buckets']}")
            lines.append(f"  Compliance Rate: {summary['compliance_rate']}%")
            lines.append("")

            # Table of buckets
            table_data = []
            for bucket in report['buckets']:
                if 'error' in bucket:
                    table_data.append([
                        bucket['bucket_name'],
                        'ERROR',
                        '-',
                        '-',
                        bucket['error']
                    ])
                else:
                    table_data.append([
                        bucket['bucket_name'],
                        'Yes' if bucket['compliant'] else 'No',
                        bucket['statistics']['total_size_gb'],
                        bucket['statistics']['object_count'],
                        ''
                    ])

            lines.append(tabulate(
                table_data,
                headers=['Bucket', 'Compliant', 'Size (GB)', 'Objects', 'Notes'],
                tablefmt='grid'
            ))
        else:
            # Single bucket report
            lines.append(f"Bucket: {report['bucket_name']}")
            lines.append(f"Compliant: {'Yes' if report['compliant'] else 'No'}")
            lines.append("")

            lines.append("Statistics:")
            stats = report['statistics']
            lines.append(f"  Size: {stats['total_size_gb']} GB ({stats['total_size_bytes']} bytes)")
            lines.append(f"  Objects: {stats['object_count']}")
            lines.append("")

            lines.append("Lifecycle Policy:")
            lifecycle = report['lifecycle_policy']
            lines.append(f"  Configured: {'Yes' if lifecycle['configured'] else 'No'}")

            if lifecycle['configured']:
                validation = lifecycle['validation']
                lines.append(f"  Valid: {'Yes' if validation['valid'] else 'No'}")
                lines.append(f"  Rules Count: {validation['rules_count']}")

                if validation['issues']:
                    lines.append("")
                    lines.append("  Issues:")
                    for issue in validation['issues']:
                        lines.append(f"    - {issue}")

                if validation['warnings']:
                    lines.append("")
                    lines.append("  Warnings:")
                    for warning in validation['warnings']:
                        lines.append(f"    - {warning}")

        lines.append("")
        lines.append("=" * 80)
        return "\n".join(lines)

    def export_report_json(self, report: Dict[str, Any], file_path: str):
        """
        Export compliance report to JSON file

        Args:
            report: Compliance report dictionary
            file_path: Path to output JSON file
        """
        try:
            with open(file_path, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            logger.info(f"Exported compliance report to {file_path}")
        except Exception as e:
            logger.error(f"Error exporting report to {file_path}: {e}")
            raise

    def get_expiring_objects(
        self,
        bucket_name: str,
        days_threshold: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Get objects that will expire within the threshold

        Args:
            bucket_name: Name of the S3 bucket
            days_threshold: Number of days to look ahead

        Returns:
            List of objects that will expire soon
        """
        logger.info(
            f"Finding objects expiring within {days_threshold} days in {bucket_name}"
        )

        lifecycle_config = self.s3_client.get_lifecycle_configuration(bucket_name)
        if not lifecycle_config:
            logger.warning(f"No lifecycle configuration for {bucket_name}")
            return []

        expiring_objects = []
        threshold_date = datetime.utcnow() + timedelta(days=days_threshold)

        # Get all objects
        objects = self.s3_client.list_objects(bucket_name, max_keys=10000)

        for rule in lifecycle_config.get('Rules', []):
            if rule.get('Status') != 'Enabled':
                continue

            if 'Expiration' not in rule:
                continue

            expiration = rule['Expiration']
            if 'Days' in expiration:
                expiration_days = expiration['Days']

                for obj in objects:
                    obj_age_days = (datetime.utcnow() - obj['last_modified'].replace(tzinfo=None)).days
                    days_until_expiration = expiration_days - obj_age_days

                    if 0 < days_until_expiration <= days_threshold:
                        expiring_objects.append({
                            'key': obj['key'],
                            'size': obj['size'],
                            'last_modified': obj['last_modified'],
                            'days_until_expiration': days_until_expiration,
                            'rule_id': rule.get('ID', 'Unknown')
                        })

        logger.info(f"Found {len(expiring_objects)} objects expiring soon")
        return expiring_objects
