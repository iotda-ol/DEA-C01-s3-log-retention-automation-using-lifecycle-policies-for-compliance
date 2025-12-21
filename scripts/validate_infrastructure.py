#!/usr/bin/env python3
"""Validate deployed infrastructure."""

import boto3
import sys
from typing import Dict, List


def validate_bucket(bucket_name: str) -> Dict[str, bool]:
    """Validate S3 bucket configuration."""
    s3_client = boto3.client('s3')
    results = {}

    try:
        # Check bucket exists
        s3_client.head_bucket(Bucket=bucket_name)
        results['bucket_exists'] = True

        # Check versioning
        versioning = s3_client.get_bucket_versioning(Bucket=bucket_name)
        results['versioning_enabled'] = versioning.get('Status') == 'Enabled'

        # Check encryption
        try:
            encryption = s3_client.get_bucket_encryption(Bucket=bucket_name)
            results['encryption_enabled'] = True
        except:
            results['encryption_enabled'] = False

        # Check lifecycle policy
        try:
            lifecycle = s3_client.get_bucket_lifecycle_configuration(Bucket=bucket_name)
            results['lifecycle_configured'] = len(lifecycle.get('Rules', [])) > 0
        except:
            results['lifecycle_configured'] = False

    except Exception as e:
        print(f"Error validating bucket: {e}")
        results['bucket_exists'] = False

    return results


def main():
    """Main validation function."""
    if len(sys.argv) < 2:
        print("Usage: python validate_infrastructure.py <bucket-name>")
        sys.exit(1)

    bucket_name = sys.argv[1]
    print(f"Validating infrastructure for bucket: {bucket_name}")

    results = validate_bucket(bucket_name)

    print("\nValidation Results:")
    print("-" * 50)
    for check, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{check:30s}: {status}")

    all_passed = all(results.values())
    print("-" * 50)
    print(f"\nOverall: {'✓ ALL CHECKS PASSED' if all_passed else '✗ SOME CHECKS FAILED'}")

    sys.exit(0 if all_passed else 1)


if __name__ == '__main__':
    main()
