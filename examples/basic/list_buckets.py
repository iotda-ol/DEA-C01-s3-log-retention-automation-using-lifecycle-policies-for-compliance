#!/usr/bin/env python3
"""
Basic example: List all S3 buckets
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'python' / 'src'))

from s3_operations.client import S3Operations


def main():
    # Initialize S3 client
    s3_ops = S3Operations(region='us-east-1')
    
    # List all buckets
    print("Listing all S3 buckets...\n")
    buckets = s3_ops.list_buckets()
    
    for bucket in buckets:
        print(f"  • {bucket['Name']}")
        print(f"    Created: {bucket['CreationDate']}")
        print()
    
    print(f"Total buckets: {len(buckets)}")


if __name__ == '__main__':
    main()
