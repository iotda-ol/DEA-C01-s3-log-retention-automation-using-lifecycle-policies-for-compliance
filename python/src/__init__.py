"""
S3 Log Retention Automation Package
"""

__version__ = "1.0.0"
__author__ = "S3 Log Retention Team"
__license__ = "MIT"

from .s3_ops import S3Client
from .policy_validator import PolicyValidator
from .compliance_reporter import ComplianceReporter

__all__ = [
    'S3Client',
    'PolicyValidator',
    'ComplianceReporter',
]
