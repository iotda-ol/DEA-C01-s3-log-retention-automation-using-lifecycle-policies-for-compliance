"""
Unit tests for PolicyValidator
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from policy_validator.validator import PolicyValidator


@pytest.fixture
def validator():
    """Create PolicyValidator instance"""
    return PolicyValidator(min_retention_days=365)


@pytest.fixture
def valid_policy():
    """Valid lifecycle policy"""
    return {
        'Rules': [
            {
                'ID': 'test-rule',
                'Status': 'Enabled',
                'Expiration': {'Days': 365},
                'Transitions': [
                    {'Days': 30, 'StorageClass': 'STANDARD_IA'},
                    {'Days': 90, 'StorageClass': 'GLACIER'}
                ]
            }
        ]
    }


@pytest.fixture
def invalid_policy_short_retention():
    """Invalid policy with too short retention"""
    return {
        'Rules': [
            {
                'ID': 'test-rule',
                'Status': 'Enabled',
                'Expiration': {'Days': 180}
            }
        ]
    }


def test_validate_valid_policy(validator, valid_policy):
    """Test validation of valid policy"""
    result = validator.validate_lifecycle_policy(valid_policy)

    assert result['valid'] is True
    assert result['compliant'] is True
    assert len(result['issues']) == 0


def test_validate_no_policy(validator):
    """Test validation when no policy exists"""
    result = validator.validate_lifecycle_policy(None)

    assert result['valid'] is False
    assert result['compliant'] is False
    assert 'No lifecycle policy configured' in result['issues']


def test_validate_short_retention(validator, invalid_policy_short_retention):
    """Test validation of policy with insufficient retention"""
    result = validator.validate_lifecycle_policy(invalid_policy_short_retention)

    assert result['valid'] is False
    assert result['compliant'] is False
    assert any('less than required minimum' in issue for issue in result['issues'])


def test_validate_disabled_rule(validator):
    """Test validation of disabled rule"""
    policy = {
        'Rules': [
            {
                'ID': 'test-rule',
                'Status': 'Disabled',
                'Expiration': {'Days': 365}
            }
        ]
    }

    result = validator.validate_lifecycle_policy(policy)

    assert result['compliant'] is False
    assert any('not enabled' in warning for warning in result['warnings'])


def test_validate_invalid_storage_class(validator):
    """Test validation with invalid storage class"""
    policy = {
        'Rules': [
            {
                'ID': 'test-rule',
                'Status': 'Enabled',
                'Expiration': {'Days': 365},
                'Transitions': [
                    {'Days': 30, 'StorageClass': 'INVALID_CLASS'}
                ]
            }
        ]
    }

    result = validator.validate_lifecycle_policy(policy)

    assert result['valid'] is False
    assert any('Invalid storage class' in issue for issue in result['issues'])


def test_validate_transition_order(validator):
    """Test validation of transition day ordering"""
    policy = {
        'Rules': [
            {
                'ID': 'test-rule',
                'Status': 'Enabled',
                'Expiration': {'Days': 365},
                'Transitions': [
                    {'Days': 90, 'StorageClass': 'GLACIER'},
                    {'Days': 30, 'StorageClass': 'STANDARD_IA'}  # Out of order
                ]
            }
        ]
    }

    result = validator.validate_lifecycle_policy(policy)

    assert result['valid'] is False
    assert any('must be greater than previous' in issue for issue in result['issues'])


def test_validate_bucket_policy_public_access(validator):
    """Test bucket policy validation with public access"""
    policy = {
        'Statement': [
            {
                'Effect': 'Allow',
                'Principal': '*',
                'Action': 's3:GetObject'
            }
        ]
    }

    result = validator.validate_bucket_policy(policy)

    assert result['valid'] is False
    assert any('public access' in issue for issue in result['issues'])


def test_validate_bucket_policy_secure_transport(validator):
    """Test bucket policy validation for secure transport"""
    policy = {
        'Statement': [
            {
                'Effect': 'Allow',
                'Principal': {'AWS': 'arn:aws:iam::123456789012:root'},
                'Action': 's3:GetObject'
            }
        ]
    }

    result = validator.validate_bucket_policy(policy)

    assert any('secure transport' in warning for warning in result['warnings'])


def test_generate_compliance_report(validator, valid_policy):
    """Test compliance report generation"""
    report = validator.generate_compliance_report(
        bucket_name='test-bucket',
        lifecycle_policy=valid_policy,
        bucket_policy=None
    )

    assert report['bucket_name'] == 'test-bucket'
    assert report['overall_compliant'] is True
    assert 'timestamp' in report
    assert report['min_retention_days'] == 365
