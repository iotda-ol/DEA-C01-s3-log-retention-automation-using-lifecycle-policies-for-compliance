#!/usr/bin/env python3
"""Test lifecycle policies by uploading sample logs."""

import boto3
import sys
from datetime import datetime, timedelta
import time


def upload_test_logs(bucket_name: str, count: int = 10):
    """Upload test log files to S3."""
    s3_client = boto3.client('s3')

    for i in range(count):
        key = f"logs/test/sample-{i}.log"
        content = f"Test log entry {i} - {datetime.now()}"

        s3_client.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=content.encode('utf-8'),
            Metadata={'test': 'true'}
        )
        print(f"Uploaded: {key}")

    print(f"\n✓ Successfully uploaded {count} test log files")


def check_lifecycle_application(bucket_name: str):
    """Check if lifecycle policies are configured."""
    s3_client = boto3.client('s3')

    try:
        response = s3_client.get_bucket_lifecycle_configuration(Bucket=bucket_name)
        rules = response.get('Rules', [])

        print(f"\nLifecycle Rules: {len(rules)}")
        for rule in rules:
            print(f"\nRule: {rule['ID']}")
            print(f"  Status: {rule['Status']}")
            if 'Expiration' in rule:
                print(f"  Expiration: {rule['Expiration'].get('Days')} days")
            if 'Transitions' in rule:
                print(f"  Transitions:")
                for trans in rule['Transitions']:
                    print(f"    - {trans['Days']} days → {trans['StorageClass']}")

    except Exception as e:
        print(f"Error checking lifecycle: {e}")


def main():
    """Main test function."""
    if len(sys.argv) < 2:
        print("Usage: python test_lifecycle.py <bucket-name> [count]")
        sys.exit(1)

    bucket_name = sys.argv[1]
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 10

    print(f"Testing lifecycle policies for bucket: {bucket_name}")
    
    check_lifecycle_application(bucket_name)
    upload_test_logs(bucket_name, count)

    print("\nNote: Lifecycle transitions occur asynchronously.")
    print("Check back after the configured transition periods.")


if __name__ == '__main__':
    main()
