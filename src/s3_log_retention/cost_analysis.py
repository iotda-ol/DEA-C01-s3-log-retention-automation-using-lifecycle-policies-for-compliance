"""Cost analysis utilities for S3 log retention."""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class CostAnalyzer:
    """Analyze costs for S3 log retention."""

    # Storage costs per GB-month (approximate)
    STORAGE_COSTS = {
        'STANDARD': 0.023,
        'STANDARD_IA': 0.0125,
        'INTELLIGENT_TIERING': 0.023,
        'GLACIER': 0.004,
        'DEEP_ARCHIVE': 0.00099,
    }

    def __init__(self, bucket_name: str, region: Optional[str] = None):
        """Initialize cost analyzer.

        Args:
            bucket_name: Name of the S3 bucket
            region: AWS region
        """
        self.bucket_name = bucket_name
        self.region = region or 'us-east-1'
        self.s3_client = boto3.client('s3', region_name=self.region)
        self.cloudwatch_client = boto3.client('cloudwatch', region_name=self.region)

    def calculate_storage_cost(self, size_bytes: int, storage_class: str) -> float:
        """Calculate monthly storage cost.

        Args:
            size_bytes: Size in bytes
            storage_class: S3 storage class

        Returns:
            Estimated monthly cost in USD
        """
        size_gb = size_bytes / (1024 ** 3)
        cost_per_gb = self.STORAGE_COSTS.get(storage_class, 0.023)
        return size_gb * cost_per_gb

    def analyze_bucket_costs(self) -> Dict[str, float]:
        """Analyze total bucket costs by storage class.

        Returns:
            Dictionary of storage class to estimated monthly cost
        """
        costs = {}
        total_cost = 0.0

        try:
            paginator = self.s3_client.get_paginator('list_objects_v2')
            storage_stats = {}

            for page in paginator.paginate(Bucket=self.bucket_name):
                for obj in page.get('Contents', []):
                    storage_class = obj.get('StorageClass', 'STANDARD')
                    size = obj.get('Size', 0)

                    if storage_class not in storage_stats:
                        storage_stats[storage_class] = 0
                    storage_stats[storage_class] += size

            for storage_class, total_bytes in storage_stats.items():
                cost = self.calculate_storage_cost(total_bytes, storage_class)
                costs[storage_class] = cost
                total_cost += cost

            costs['TOTAL'] = total_cost
            logger.info(f"Estimated monthly cost: ${total_cost:.2f}")
            return costs

        except ClientError as e:
            logger.error(f"Error analyzing costs: {e}")
            raise

    def estimate_savings(self, transition_days: int, target_class: str) -> Dict:
        """Estimate potential savings from lifecycle transition.

        Args:
            transition_days: Days before transition
            target_class: Target storage class

        Returns:
            Dictionary with savings estimate
        """
        result = {
            'current_cost': 0.0,
            'projected_cost': 0.0,
            'monthly_savings': 0.0,
            'annual_savings': 0.0
        }

        try:
            # Simplified calculation - in reality would need more detailed analysis
            current_costs = self.analyze_bucket_costs()
            current_standard = current_costs.get('STANDARD', 0.0)

            # Estimate how much would transition
            transition_ratio = min(1.0, transition_days / 365.0)
            transitionable_cost = current_standard * transition_ratio

            target_cost_ratio = self.STORAGE_COSTS.get(target_class, 0.023) / 0.023
            new_cost = transitionable_cost * target_cost_ratio

            result['current_cost'] = current_costs.get('TOTAL', 0.0)
            result['projected_cost'] = result['current_cost'] - transitionable_cost + new_cost
            result['monthly_savings'] = result['current_cost'] - result['projected_cost']
            result['annual_savings'] = result['monthly_savings'] * 12

            logger.info(f"Estimated annual savings: ${result['annual_savings']:.2f}")
            return result

        except ClientError as e:
            logger.error(f"Error estimating savings: {e}")
            return result
