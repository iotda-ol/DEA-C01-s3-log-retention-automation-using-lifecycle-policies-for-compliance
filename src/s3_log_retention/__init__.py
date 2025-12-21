"""S3 Log Retention automation package.

This package provides utilities for managing S3 log retention using
lifecycle policies for compliance purposes.
"""

__version__ = "1.0.0"
__author__ = "DEA-C01 Team"

from .lifecycle import LifecyclePolicyManager
from .s3_utils import S3LogManager

__all__ = [
    "LifecyclePolicyManager",
    "S3LogManager",
]
