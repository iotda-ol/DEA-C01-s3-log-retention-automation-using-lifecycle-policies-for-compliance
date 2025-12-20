"""
Sample test file for S3 operations
"""

import pytest
from moto import mock_s3
import boto3
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from s3_operations.client import S3Operations


@mock_s3
def test_list_buckets():
    """Test listing S3 buckets"""
    # Create mock S3 client
    s3_ops = S3Operations(region='us-east-1')
    
    # Create test bucket
    s3_ops.client.create_bucket(Bucket='test-bucket')
    
    # List buckets
    buckets = s3_ops.list_buckets()
    
    # Assert
    assert len(buckets) == 1
    assert buckets[0]['Name'] == 'test-bucket'


@mock_s3
def test_bucket_exists():
    """Test checking if bucket exists"""
    s3_ops = S3Operations(region='us-east-1')
    
    # Create bucket
    s3_ops.client.create_bucket(Bucket='test-bucket')
    
    # Test exists
    assert s3_ops.bucket_exists('test-bucket') is True
    assert s3_ops.bucket_exists('non-existent-bucket') is False


@mock_s3
def test_upload_download_file(tmp_path):
    """Test file upload and download"""
    s3_ops = S3Operations(region='us-east-1')
    
    # Create bucket
    s3_ops.client.create_bucket(Bucket='test-bucket')
    
    # Create test file
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content")
    
    # Upload file
    result = s3_ops.upload_file(str(test_file), 'test-bucket', 'test.txt')
    assert result is True
    
    # Download file
    download_file = tmp_path / "downloaded.txt"
    result = s3_ops.download_file('test-bucket', 'test.txt', str(download_file))
    assert result is True
    assert download_file.read_text() == "test content"
