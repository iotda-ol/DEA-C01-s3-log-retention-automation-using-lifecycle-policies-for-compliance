#!/usr/bin/env python3
"""
Basic example: Validate bucket compliance
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'python' / 'src'))

import boto3
from compliance.validator import ComplianceValidator


def main():
    # Initialize validator
    validator = ComplianceValidator(required_retention_days=365)
    s3_client = boto3.client('s3', region_name='us-east-1')
    
    # Bucket name
    bucket_name = input("Enter bucket name: ")
    
    print(f"\nValidating compliance for: {bucket_name}\n")
    
    # Validate bucket
    results = validator.validate_bucket(bucket_name, s3_client)
    
    # Display results
    for check_name, check_result in results['checks'].items():
        status = "✓ PASS" if check_result['compliant'] else "✗ FAIL"
        print(f"{status} - {check_name.replace('_', ' ').title()}")
        
        if not check_result['compliant']:
            for issue in check_result['issues']:
                print(f"    • {issue}")
    
    print(f"\nOverall: {'✓ COMPLIANT' if results['compliant'] else '✗ NON-COMPLIANT'}")


if __name__ == '__main__':
    main()
