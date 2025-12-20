#!/usr/bin/env python3
"""Basic example of using S3 log retention automation."""

from s3_log_retention import S3LogManager, LifecyclePolicyManager

# Configuration
BUCKET_NAME = 'my-log-bucket'
REGION = 'us-east-1'

def main():
    """Main example function."""
    # Initialize managers
    s3_manager = S3LogManager(BUCKET_NAME, REGION)
    lifecycle_manager = LifecyclePolicyManager(BUCKET_NAME, REGION)

    # Create a basic retention policy
    print("Creating retention policy...")
    success = lifecycle_manager.create_retention_policy(
        rule_id='basic-retention',
        prefix='logs/',
        expiration_days=365,
        transitions=[
            {'Days': 30, 'StorageClass': 'STANDARD_IA'},
            {'Days': 90, 'StorageClass': 'GLACIER'}
        ]
    )

    if success:
        print("✓ Retention policy created successfully")
    else:
        print("✗ Failed to create retention policy")
        return

    # List existing logs
    print("\nListing logs...")
    logs = s3_manager.list_logs(prefix='logs/')
    print(f"Found {len(logs)} log files")

    # Validate the policy
    print("\nValidating policy...")
    validation = lifecycle_manager.validate_policy()
    print(f"Policy is {'valid' if validation['valid'] else 'invalid'}")


if __name__ == '__main__':
    main()
