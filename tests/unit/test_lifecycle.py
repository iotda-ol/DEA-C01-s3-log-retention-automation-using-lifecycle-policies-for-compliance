"""Unit tests for lifecycle policy management."""

import pytest
from s3_log_retention.lifecycle import LifecyclePolicyManager


class TestLifecyclePolicyManager:
    """Test LifecyclePolicyManager class."""

    def test_init(self, test_bucket):
        """Test initialization."""
        manager = LifecyclePolicyManager(test_bucket)
        assert manager.bucket_name == test_bucket

    def test_create_retention_policy(self, test_bucket, s3_client):
        """Test creating a retention policy."""
        manager = LifecyclePolicyManager(test_bucket)
        
        result = manager.create_retention_policy(
            rule_id='test-rule',
            prefix='logs/',
            expiration_days=365
        )
        assert result is True

        rules = manager.get_lifecycle_rules()
        assert len(rules) == 1
        assert rules[0]['ID'] == 'test-rule'

    def test_create_compliance_policy(self, test_bucket, s3_client):
        """Test creating a compliance policy."""
        manager = LifecyclePolicyManager(test_bucket)
        
        result = manager.create_compliance_policy(
            log_type='audit',
            retention_days=365,
            archive_days=30
        )
        assert result is True

        rules = manager.get_lifecycle_rules()
        assert len(rules) > 0

    def test_delete_lifecycle_rule(self, test_bucket, s3_client):
        """Test deleting a lifecycle rule."""
        manager = LifecyclePolicyManager(test_bucket)
        
        # Create a rule first
        manager.create_retention_policy(
            rule_id='test-rule',
            expiration_days=90
        )

        # Delete it
        result = manager.delete_lifecycle_rule('test-rule')
        assert result is True

        rules = manager.get_lifecycle_rules()
        assert len(rules) == 0

    def test_validate_policy(self, test_bucket, s3_client):
        """Test policy validation."""
        manager = LifecyclePolicyManager(test_bucket)
        
        # Create a valid policy
        manager.create_retention_policy(
            rule_id='test-rule',
            expiration_days=365,
            transitions=[
                {'Days': 30, 'StorageClass': 'STANDARD_IA'},
                {'Days': 90, 'StorageClass': 'GLACIER'}
            ]
        )

        result = manager.validate_policy()
        assert result['valid'] is True
        assert result['rule_count'] == 1
