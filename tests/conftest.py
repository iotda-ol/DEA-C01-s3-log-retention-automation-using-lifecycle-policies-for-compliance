"""Pytest configuration and fixtures."""

import pytest
from moto import mock_s3, mock_cloudwatch, mock_sns
import boto3


@pytest.fixture
def aws_credentials(monkeypatch):
    """Mock AWS credentials."""
    monkeypatch.setenv('AWS_ACCESS_KEY_ID', 'testing')
    monkeypatch.setenv('AWS_SECRET_ACCESS_KEY', 'testing')
    monkeypatch.setenv('AWS_SECURITY_TOKEN', 'testing')
    monkeypatch.setenv('AWS_SESSION_TOKEN', 'testing')
    monkeypatch.setenv('AWS_DEFAULT_REGION', 'us-east-1')


@pytest.fixture
def s3_client(aws_credentials):
    """Create a mocked S3 client."""
    with mock_s3():
        yield boto3.client('s3', region_name='us-east-1')


@pytest.fixture
def test_bucket(s3_client):
    """Create a test S3 bucket."""
    bucket_name = 'test-log-bucket'
    s3_client.create_bucket(Bucket=bucket_name)
    return bucket_name


@pytest.fixture
def cloudwatch_client(aws_credentials):
    """Create a mocked CloudWatch client."""
    with mock_cloudwatch():
        yield boto3.client('cloudwatch', region_name='us-east-1')


@pytest.fixture
def sns_client(aws_credentials):
    """Create a mocked SNS client."""
    with mock_sns():
        yield boto3.client('sns', region_name='us-east-1')
