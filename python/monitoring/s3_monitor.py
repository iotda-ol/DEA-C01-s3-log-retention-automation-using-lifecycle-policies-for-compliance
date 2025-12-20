"""
Monitoring Module
CloudWatch monitoring for S3 log retention
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class S3Monitor:
    """Monitor S3 bucket metrics using CloudWatch"""
    
    def __init__(self, cloudwatch_client, s3_client):
        """
        Initialize S3 monitor
        
        Args:
            cloudwatch_client: Boto3 CloudWatch client
            s3_client: Boto3 S3 client
        """
        self.cloudwatch = cloudwatch_client
        self.s3 = s3_client
    
    def get_bucket_metrics(
        self,
        bucket_name: str,
        metric_name: str,
        start_time: datetime = None,
        end_time: datetime = None,
        period: int = 86400
    ) -> List[Dict]:
        """
        Get CloudWatch metrics for S3 bucket
        
        Args:
            bucket_name: S3 bucket name
            metric_name: Metric name (BucketSizeBytes, NumberOfObjects, etc.)
            start_time: Start time for metrics
            end_time: End time for metrics
            period: Period in seconds
            
        Returns:
            List of metric data points
        """
        if end_time is None:
            end_time = datetime.now()
        if start_time is None:
            start_time = end_time - timedelta(days=7)
        
        try:
            response = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/S3',
                MetricName=metric_name,
                Dimensions=[
                    {'Name': 'BucketName', 'Value': bucket_name},
                    {'Name': 'StorageType', 'Value': 'StandardStorage'}
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=period,
                Statistics=['Average', 'Sum']
            )
            
            datapoints = response.get('Datapoints', [])
            logger.info(f"Retrieved {len(datapoints)} data points for {metric_name}")
            return sorted(datapoints, key=lambda x: x['Timestamp'])
        except Exception as e:
            logger.error(f"Failed to get metrics for {bucket_name}: {e}")
            return []
    
    def get_storage_size(self, bucket_name: str, days: int = 7) -> List[Dict]:
        """
        Get bucket storage size metrics
        
        Args:
            bucket_name: S3 bucket name
            days: Number of days to retrieve
            
        Returns:
            List of storage size data points
        """
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)
        
        return self.get_bucket_metrics(
            bucket_name,
            'BucketSizeBytes',
            start_time,
            end_time
        )
    
    def get_object_count(self, bucket_name: str, days: int = 7) -> List[Dict]:
        """
        Get bucket object count metrics
        
        Args:
            bucket_name: S3 bucket name
            days: Number of days to retrieve
            
        Returns:
            List of object count data points
        """
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)
        
        return self.get_bucket_metrics(
            bucket_name,
            'NumberOfObjects',
            start_time,
            end_time
        )
    
    def check_storage_quota(
        self,
        bucket_name: str,
        quota_bytes: int
    ) -> tuple[bool, int, str]:
        """
        Check if bucket exceeds storage quota
        
        Args:
            bucket_name: S3 bucket name
            quota_bytes: Quota in bytes
            
        Returns:
            Tuple of (exceeds_quota, current_size, message)
        """
        metrics = self.get_storage_size(bucket_name, days=1)
        
        if not metrics:
            return False, 0, "No metrics available"
        
        current_size = int(metrics[-1].get('Average', 0))
        exceeds = current_size > quota_bytes
        
        message = f"Current: {self._format_bytes(current_size)}, " \
                  f"Quota: {self._format_bytes(quota_bytes)}"
        
        if exceeds:
            message += " - QUOTA EXCEEDED"
            logger.warning(f"Storage quota exceeded for {bucket_name}")
        
        return exceeds, current_size, message
    
    def get_lifecycle_transition_metrics(
        self,
        bucket_name: str,
        days: int = 30
    ) -> Dict[str, int]:
        """
        Estimate objects in different storage classes
        
        Args:
            bucket_name: S3 bucket name
            days: Number of days to analyze
            
        Returns:
            Dict of storage class counts
        """
        # This is an estimation based on lifecycle rules
        # Actual implementation would query all objects
        storage_classes = {
            'STANDARD': 0,
            'STANDARD_IA': 0,
            'GLACIER': 0,
            'DEEP_ARCHIVE': 0
        }
        
        try:
            paginator = self.s3.get_paginator('list_objects_v2')
            pages = paginator.paginate(Bucket=bucket_name)
            
            for page in pages:
                for obj in page.get('Contents', []):
                    storage_class = obj.get('StorageClass', 'STANDARD')
                    if storage_class in storage_classes:
                        storage_classes[storage_class] += 1
            
            logger.info(f"Retrieved storage class distribution for {bucket_name}")
        except Exception as e:
            logger.error(f"Failed to get storage class distribution: {e}")
        
        return storage_classes
    
    def create_alarm(
        self,
        alarm_name: str,
        bucket_name: str,
        metric_name: str,
        threshold: float,
        comparison_operator: str = 'GreaterThanThreshold',
        evaluation_periods: int = 2,
        alarm_actions: Optional[List[str]] = None
    ) -> bool:
        """
        Create CloudWatch alarm for S3 bucket
        
        Args:
            alarm_name: Name of the alarm
            bucket_name: S3 bucket name
            metric_name: Metric to monitor
            threshold: Alarm threshold
            comparison_operator: Comparison operator
            evaluation_periods: Number of evaluation periods
            alarm_actions: List of action ARNs
            
        Returns:
            True if successful
        """
        try:
            self.cloudwatch.put_metric_alarm(
                AlarmName=alarm_name,
                ComparisonOperator=comparison_operator,
                EvaluationPeriods=evaluation_periods,
                MetricName=metric_name,
                Namespace='AWS/S3',
                Period=86400,
                Statistic='Average',
                Threshold=threshold,
                ActionsEnabled=True,
                AlarmActions=alarm_actions or [],
                AlarmDescription=f'Monitor {metric_name} for {bucket_name}',
                Dimensions=[
                    {'Name': 'BucketName', 'Value': bucket_name},
                    {'Name': 'StorageType', 'Value': 'StandardStorage'}
                ]
            )
            
            logger.info(f"Created alarm: {alarm_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to create alarm {alarm_name}: {e}")
            return False
    
    @staticmethod
    def _format_bytes(size_bytes: int) -> str:
        """Format bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
