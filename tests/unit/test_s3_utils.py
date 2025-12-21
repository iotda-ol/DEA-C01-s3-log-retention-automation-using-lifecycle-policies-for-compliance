"""Unit tests for S3 utilities."""

import pytest
from s3_log_retention.s3_utils import S3LogManager


class TestS3LogManager:
    """Test S3LogManager class."""

    def test_init(self, test_bucket):
        """Test initialization."""
        manager = S3LogManager(test_bucket)
        assert manager.bucket_name == test_bucket

    def test_list_logs_empty(self, test_bucket, s3_client):
        """Test listing logs in empty bucket."""
        manager = S3LogManager(test_bucket)
        logs = manager.list_logs()
        assert len(logs) == 0

    def test_list_logs_with_objects(self, test_bucket, s3_client):
        """Test listing logs with objects."""
        # Upload test objects
        s3_client.put_object(
            Bucket=test_bucket,
            Key='logs/test1.log',
            Body=b'test content'
        )
        s3_client.put_object(
            Bucket=test_bucket,
            Key='logs/test2.log',
            Body=b'test content'
        )

        manager = S3LogManager(test_bucket)
        logs = manager.list_logs(prefix='logs/')
        assert len(logs) == 2

    def test_get_log_metadata(self, test_bucket, s3_client):
        """Test getting object metadata."""
        key = 'test.log'
        s3_client.put_object(
            Bucket=test_bucket,
            Key=key,
            Body=b'test content',
            Metadata={'source': 'test'}
        )

        manager = S3LogManager(test_bucket)
        metadata = manager.get_log_metadata(key)
        assert 'ContentLength' in metadata

    def test_tag_object(self, test_bucket, s3_client):
        """Test tagging objects."""
        key = 'test.log'
        s3_client.put_object(Bucket=test_bucket, Key=key, Body=b'test')

        manager = S3LogManager(test_bucket)
        tags = {'Environment': 'test', 'Type': 'log'}
        result = manager.tag_object(key, tags)
        assert result is True

        retrieved_tags = manager.get_object_tags(key)
        assert retrieved_tags == tags
