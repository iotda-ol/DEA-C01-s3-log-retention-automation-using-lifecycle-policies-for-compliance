"""
Report Generator
Generate compliance and usage reports for S3 log retention
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging
from tabulate import tabulate

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generates various reports for S3 log management"""
    
    def __init__(self, s3_ops, cloudwatch_client=None):
        """
        Initialize report generator
        
        Args:
            s3_ops: S3Operations instance
            cloudwatch_client: Optional CloudWatch client for metrics
        """
        self.s3_ops = s3_ops
        self.cloudwatch = cloudwatch_client
    
    def generate_storage_report(
        self, bucket_name: str, prefixes: List[str] = None
    ) -> Dict[str, Any]:
        """
        Generate storage usage report
        
        Args:
            bucket_name: S3 bucket name
            prefixes: List of prefixes to analyze
            
        Returns:
            Report data dict
        """
        if prefixes is None:
            prefixes = ['']
        
        report = {
            "bucket": bucket_name,
            "timestamp": datetime.now().isoformat(),
            "storage_by_prefix": {},
            "total_size_bytes": 0,
            "total_objects": 0
        }
        
        for prefix in prefixes:
            objects = self.s3_ops.list_objects(bucket_name, prefix)
            size = sum(obj.get('Size', 0) for obj in objects)
            
            report["storage_by_prefix"][prefix or "root"] = {
                "size_bytes": size,
                "object_count": len(objects)
            }
            report["total_size_bytes"] += size
            report["total_objects"] += len(objects)
        
        logger.info(f"Generated storage report for {bucket_name}")
        return report
    
    def generate_lifecycle_report(
        self, bucket_name: str
    ) -> Dict[str, Any]:
        """
        Generate lifecycle policy report
        
        Args:
            bucket_name: S3 bucket name
            
        Returns:
            Report data dict
        """
        rules = self.s3_ops.get_lifecycle_policy(bucket_name)
        
        report = {
            "bucket": bucket_name,
            "timestamp": datetime.now().isoformat(),
            "has_lifecycle_policy": rules is not None,
            "rule_count": len(rules) if rules else 0,
            "rules": []
        }
        
        if rules:
            for rule in rules:
                rule_info = {
                    "id": rule.get('ID'),
                    "status": rule.get('Status'),
                    "prefix": rule.get('Filter', {}).get('Prefix', ''),
                    "expiration_days": rule.get('Expiration', {}).get('Days'),
                    "transitions": []
                }
                
                for transition in rule.get('Transitions', []):
                    rule_info["transitions"].append({
                        "days": transition.get('Days'),
                        "storage_class": transition.get('StorageClass')
                    })
                
                report["rules"].append(rule_info)
        
        logger.info(f"Generated lifecycle report for {bucket_name}")
        return report
    
    def generate_age_distribution_report(
        self, bucket_name: str, prefix: str = ""
    ) -> Dict[str, Any]:
        """
        Generate object age distribution report
        
        Args:
            bucket_name: S3 bucket name
            prefix: Object key prefix filter
            
        Returns:
            Report data dict
        """
        objects = self.s3_ops.list_objects(bucket_name, prefix)
        now = datetime.now()
        
        age_buckets = {
            "0-7d": 0,
            "8-30d": 0,
            "31-90d": 0,
            "91-180d": 0,
            "181-365d": 0,
            "365d+": 0
        }
        
        for obj in objects:
            last_modified = obj.get('LastModified')
            if last_modified:
                age_days = (now - last_modified.replace(tzinfo=None)).days
                
                if age_days <= 7:
                    age_buckets["0-7d"] += 1
                elif age_days <= 30:
                    age_buckets["8-30d"] += 1
                elif age_days <= 90:
                    age_buckets["31-90d"] += 1
                elif age_days <= 180:
                    age_buckets["91-180d"] += 1
                elif age_days <= 365:
                    age_buckets["181-365d"] += 1
                else:
                    age_buckets["365d+"] += 1
        
        report = {
            "bucket": bucket_name,
            "prefix": prefix,
            "timestamp": datetime.now().isoformat(),
            "total_objects": len(objects),
            "age_distribution": age_buckets
        }
        
        logger.info(f"Generated age distribution report for {bucket_name}")
        return report
    
    def format_report_text(self, report: Dict[str, Any], report_type: str) -> str:
        """
        Format report as text
        
        Args:
            report: Report data dict
            report_type: Type of report
            
        Returns:
            Formatted report text
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"{report_type.upper()} REPORT")
        lines.append("=" * 70)
        lines.append(f"Bucket: {report.get('bucket', 'N/A')}")
        lines.append(f"Generated: {report.get('timestamp', 'N/A')}")
        lines.append("")
        
        if report_type == "storage":
            lines.append(f"Total Objects: {report['total_objects']:,}")
            lines.append(f"Total Size: {self._format_bytes(report['total_size_bytes'])}")
            lines.append("")
            lines.append("Storage by Prefix:")
            
            table_data = []
            for prefix, data in report['storage_by_prefix'].items():
                table_data.append([
                    prefix,
                    f"{data['object_count']:,}",
                    self._format_bytes(data['size_bytes'])
                ])
            
            lines.append(tabulate(
                table_data,
                headers=['Prefix', 'Objects', 'Size'],
                tablefmt='grid'
            ))
        
        elif report_type == "lifecycle":
            lines.append(f"Has Lifecycle Policy: {report['has_lifecycle_policy']}")
            lines.append(f"Rule Count: {report['rule_count']}")
            lines.append("")
            
            if report['rules']:
                for rule in report['rules']:
                    lines.append(f"Rule: {rule['id']}")
                    lines.append(f"  Status: {rule['status']}")
                    lines.append(f"  Prefix: {rule['prefix'] or '(all)'}")
                    if rule['expiration_days']:
                        lines.append(f"  Expiration: {rule['expiration_days']} days")
                    if rule['transitions']:
                        lines.append("  Transitions:")
                        for t in rule['transitions']:
                            lines.append(f"    {t['days']} days → {t['storage_class']}")
                    lines.append("")
        
        elif report_type == "age_distribution":
            lines.append(f"Total Objects: {report['total_objects']:,}")
            lines.append("")
            lines.append("Age Distribution:")
            
            table_data = [
                [age_range, count]
                for age_range, count in report['age_distribution'].items()
            ]
            
            lines.append(tabulate(
                table_data,
                headers=['Age Range', 'Count'],
                tablefmt='grid'
            ))
        
        lines.append("=" * 70)
        return "\n".join(lines)
    
    @staticmethod
    def _format_bytes(size_bytes: int) -> str:
        """Format bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
