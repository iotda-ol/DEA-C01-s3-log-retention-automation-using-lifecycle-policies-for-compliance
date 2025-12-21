"""
Unit tests for S3Client
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from botocore.exceptions import ClientError
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from s3_ops.client import S3Client


@pytest.fixture
def s3_client():
    """Create S3Client instance for testing"""
    with patch('boto3.Session'):
        return S3Client()


@pytest.fixture
def mock_s3_response():
    """Mock S3 API responses"""
    return {
        'Buckets': [
            {'Name': 'test-bucket-1', 'CreationDate': '2024-01-01T00:00:00Z'},
            {'Name': 'test-bucket-2', 'CreationDate': '2024-01-02T00:00:00Z'}
        ]
    }


def test_list_buckets_success(s3_client, mock_s3_response):
    """Test successful bucket listing"""
    s3_client.s3_client.list_buckets = Mock(return_value=mock_s3_response)

    buckets = s3_client.list_buckets()

    assert len(buckets) == 2
    assert buckets[0]['name'] == 'test-bucket-1'
    assert buckets[1]['name'] == 'test-bucket-2'


def test_list_buckets_empty(s3_client):
    """Test bucket listing with no buckets"""
    s3_client.s3_client.list_buckets = Mock(return_value={'Buckets': []})

    buckets = s3_client.list_buckets()

    assert len(buckets) == 0


def test_list_buckets_error(s3_client):
    """Test bucket listing with error"""
    s3_client.s3_client.list_buckets = Mock(
        side_effect=ClientError(
            {'Error': {'Code': 'AccessDenied', 'Message': 'Access Denied'}},
            'ListBuckets'
        )
    )

    with pytest.raises(ClientError):
        s3_client.list_buckets()


def test_get_bucket_location_us_east_1(s3_client):
    """Test getting bucket location for us-east-1"""
    s3_client.s3_client.get_bucket_location = Mock(
        return_value={'LocationConstraint': None}
    )

    location = s3_client.get_bucket_location('test-bucket')

    assert location == 'us-east-1'


def test_get_bucket_location_other_region(s3_client):
    """Test getting bucket location for other regions"""
    s3_client.s3_client.get_bucket_location = Mock(
        return_value={'LocationConstraint': 'us-west-2'}
    )

    location = s3_client.get_bucket_location('test-bucket')

    assert location == 'us-west-2'


def test_get_lifecycle_configuration_exists(s3_client):
    """Test getting lifecycle configuration when it exists"""
    mock_config = {
        'Rules': [
            {
                'ID': 'test-rule',
                'Status': 'Enabled',
                'Expiration': {'Days': 365}
            }
        ]
    }
    s3_client.s3_client.get_bucket_lifecycle_configuration = Mock(
        return_value=mock_config
    )

    config = s3_client.get_lifecycle_configuration('test-bucket')

    assert config is not None
    assert len(config['Rules']) == 1


def test_get_lifecycle_configuration_not_exists(s3_client):
    """Test getting lifecycle configuration when it doesn't exist"""
    s3_client.s3_client.get_bucket_lifecycle_configuration = Mock(
        side_effect=ClientError(
            {'Error': {'Code': 'NoSuchLifecycleConfiguration'}},
            'GetBucketLifecycleConfiguration'
        )
    )

    config = s3_client.get_lifecycle_configuration('test-bucket')

    assert config is None


def test_get_bucket_size(s3_client):
    """Test calculating bucket size"""
    mock_paginator = Mock()
    mock_page_iterator = [
        {
            'Contents': [
                {'Key': 'file1.log', 'Size': 1024},
                {'Key': 'file2.log', 'Size': 2048}
            ]
        }
    ]
    mock_paginator.paginate.return_value = mock_page_iterator

    s3_client.s3_client.get_paginator = Mock(return_value=mock_paginator)

    result = s3_client.get_bucket_size('test-bucket')

    assert result['total_size_bytes'] == 3072
    assert result['object_count'] == 2


def test_get_bucket_tags_with_tags(s3_client):
    """Test getting bucket tags when tags exist"""
    mock_response = {
        'TagSet': [
            {'Key': 'Environment', 'Value': 'production'},
            {'Key': 'Project', 'Value': 'LogRetention'}
        ]
    }
    s3_client.s3_client.get_bucket_tagging = Mock(return_value=mock_response)

    tags = s3_client.get_bucket_tags('test-bucket')

    assert len(tags) == 2
    assert tags['Environment'] == 'production'
    assert tags['Project'] == 'LogRetention'


def test_get_bucket_tags_no_tags(s3_client):
    """Test getting bucket tags when no tags exist"""
    s3_client.s3_client.get_bucket_tagging = Mock(
        side_effect=ClientError(
            {'Error': {'Code': 'NoSuchTagSet'}},
            'GetBucketTagging'
        )
    )

    tags = s3_client.get_bucket_tags('test-bucket')

    assert len(tags) == 0
