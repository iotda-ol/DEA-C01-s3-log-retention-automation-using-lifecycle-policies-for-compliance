#!/usr/bin/env python3
"""
Basic example: Apply lifecycle policy to a bucket
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'python' / 'src'))

from lifecycle_management.manager import LifecycleManager


def main():
    # Initialize lifecycle manager
    lifecycle_mgr = LifecycleManager(region='us-east-1')
    
    # Bucket name
    bucket_name = input("Enter bucket name: ")
    
    # Create compliance rule (1 year retention with transitions)
    rule = lifecycle_mgr.create_compliance_rule(
        retention_days=365,
        enable_glacier=True,
        glacier_days=90,
        enable_ia=True,
        ia_days=30
    )
    
    print(f"\nApplying lifecycle policy to {bucket_name}...")
    
    # Apply the policy
    success = lifecycle_mgr.set_lifecycle_policy(bucket_name, [rule])
    
    if success:
        print("✓ Policy applied successfully!")
        print("\nPolicy details:")
        print("  • Retention: 365 days")
        print("  • Transition to IA: 30 days")
        print("  • Transition to Glacier: 90 days")
    else:
        print("✗ Failed to apply policy")


if __name__ == '__main__':
    main()
