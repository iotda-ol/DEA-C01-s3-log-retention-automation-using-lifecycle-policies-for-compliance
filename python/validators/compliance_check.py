#!/usr/bin/env python3
"""
Compliance Checker
Validates S3 bucket configuration against DEA-C01 requirements
"""

import click
import logging
import sys
from pathlib import Path
from datetime import datetime
from tabulate import tabulate

sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.aws_client import AWSClientManager
from lib.s3_operations import S3Operations

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ComplianceChecker:
    """DEA-C01 compliance checker for S3 buckets"""
    
    def __init__(self, aws_client):
        self.aws = aws_client
        self.s3 = aws_client.get_s3_client()
        self.s3_ops = S3Operations(self.s3)
        
    def check_versioning(self, bucket_name: str) -> tuple[bool, str]:
        """Check if versioning is enabled"""
        try:
            response = self.s3.get_bucket_versioning(Bucket=bucket_name)
            status = response.get('Status', 'Disabled')
            if status == 'Enabled':
                return True, "Versioning enabled"
            return False, f"Versioning {status.lower()}"
        except Exception as e:
            return False, f"Error checking versioning: {e}"
    
    def check_encryption(self, bucket_name: str) -> tuple[bool, str]:
        """Check if encryption is enabled"""
        try:
            response = self.s3.get_bucket_encryption(Bucket=bucket_name)
            rules = response.get('ServerSideEncryptionConfiguration', {}).get('Rules', [])
            if rules:
                algo = rules[0]['ApplyServerSideEncryptionByDefault']['SSEAlgorithm']
                return True, f"Encryption enabled ({algo})"
            return False, "Encryption not configured"
        except self.s3.exceptions.ServerSideEncryptionConfigurationNotFoundError:
            return False, "Encryption not configured"
        except Exception as e:
            return False, f"Error checking encryption: {e}"
    
    def check_public_access(self, bucket_name: str) -> tuple[bool, str]:
        """Check if public access is blocked"""
        try:
            response = self.s3.get_public_access_block(Bucket=bucket_name)
            config = response.get('PublicAccessBlockConfiguration', {})
            
            all_blocked = all([
                config.get('BlockPublicAcls', False),
                config.get('BlockPublicPolicy', False),
                config.get('IgnorePublicAcls', False),
                config.get('RestrictPublicBuckets', False)
            ])
            
            if all_blocked:
                return True, "Public access fully blocked"
            return False, "Public access not fully blocked"
        except Exception as e:
            return False, f"Error checking public access: {e}"
    
    def check_lifecycle_policy(self, bucket_name: str) -> tuple[bool, str]:
        """Check if lifecycle policy exists with 365-day retention"""
        rules = self.s3_ops.get_lifecycle_policy(bucket_name)
        
        if not rules:
            return False, "No lifecycle policy configured"
        
        # Check for retention rule
        compliant_rules = []
        for rule in rules:
            if rule.get('Status') == 'Enabled':
                expiration = rule.get('Expiration', {})
                days = expiration.get('Days', 0)
                
                # DEA-C01 requires max 365 days retention
                if 1 <= days <= 365:
                    compliant_rules.append(f"{rule['ID']} ({days}d)")
        
        if compliant_rules:
            return True, f"Compliant rules: {', '.join(compliant_rules)}"
        return False, "No compliant retention rules found"
    
    def check_logging(self, bucket_name: str) -> tuple[bool, str]:
        """Check if access logging is enabled"""
        try:
            response = self.s3.get_bucket_logging(Bucket=bucket_name)
            logging_config = response.get('LoggingEnabled', {})
            
            if logging_config:
                target = logging_config.get('TargetBucket', 'unknown')
                return True, f"Logging to {target}"
            return False, "Access logging not enabled"
        except Exception as e:
            return False, f"Error checking logging: {e}"
    
    def run_all_checks(self, bucket_name: str) -> dict:
        """Run all compliance checks"""
        logger.info(f"Running compliance checks for {bucket_name}")
        
        checks = {
            "Versioning": self.check_versioning(bucket_name),
            "Encryption": self.check_encryption(bucket_name),
            "Public Access Block": self.check_public_access(bucket_name),
            "Lifecycle Policy": self.check_lifecycle_policy(bucket_name),
            "Access Logging": self.check_logging(bucket_name),
        }
        
        return checks


@click.group()
@click.option('--region', default='us-east-1', help='AWS region')
@click.option('--profile', default=None, help='AWS profile name')
@click.pass_context
def cli(ctx, region, profile):
    """DEA-C01 Compliance Checker for S3 Buckets"""
    ctx.ensure_object(dict)
    ctx.obj['aws'] = AWSClientManager(region_name=region, profile_name=profile)
    ctx.obj['checker'] = ComplianceChecker(ctx.obj['aws'])


@cli.command()
@click.argument('bucket_name')
@click.option('--format', type=click.Choice(['table', 'json']), default='table')
@click.pass_context
def check(ctx, bucket_name, format):
    """Run compliance checks on a bucket"""
    checker = ctx.obj['checker']
    
    click.echo(f"\n{'='*60}")
    click.echo(f"DEA-C01 Compliance Check: {bucket_name}")
    click.echo(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    click.echo(f"{'='*60}\n")
    
    checks = checker.run_all_checks(bucket_name)
    
    # Prepare results
    results = []
    all_passed = True
    
    for check_name, (passed, message) in checks.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        results.append([check_name, status, message])
        if not passed:
            all_passed = False
    
    if format == 'table':
        click.echo(tabulate(
            results,
            headers=['Check', 'Status', 'Details'],
            tablefmt='grid'
        ))
    else:
        import json
        output = {
            "bucket": bucket_name,
            "timestamp": datetime.now().isoformat(),
            "checks": {
                name: {"passed": passed, "message": msg}
                for name, (passed, msg) in checks.items()
            },
            "overall_compliance": all_passed
        }
        click.echo(json.dumps(output, indent=2))
    
    click.echo(f"\n{'='*60}")
    if all_passed:
        click.echo("✓ OVERALL STATUS: COMPLIANT")
        click.echo(f"{'='*60}\n")
        sys.exit(0)
    else:
        click.echo("✗ OVERALL STATUS: NON-COMPLIANT")
        click.echo(f"{'='*60}\n")
        sys.exit(1)


@cli.command()
@click.option('--prefix', default='', help='Bucket name prefix filter')
@click.pass_context
def check_all(ctx, prefix):
    """Run compliance checks on all buckets"""
    aws = ctx.obj['aws']
    checker = ctx.obj['checker']
    
    # List all buckets
    s3 = aws.get_s3_client()
    response = s3.list_buckets()
    buckets = [b['Name'] for b in response.get('Buckets', [])
               if b['Name'].startswith(prefix)]
    
    if not buckets:
        click.echo("No buckets found")
        return
    
    click.echo(f"Checking {len(buckets)} bucket(s)...\n")
    
    summary = []
    for bucket_name in buckets:
        checks = checker.run_all_checks(bucket_name)
        passed_count = sum(1 for passed, _ in checks.values() if passed)
        total_count = len(checks)
        compliance = "COMPLIANT" if passed_count == total_count else "NON-COMPLIANT"
        
        summary.append([
            bucket_name,
            f"{passed_count}/{total_count}",
            compliance
        ])
    
    click.echo(tabulate(
        summary,
        headers=['Bucket', 'Checks Passed', 'Status'],
        tablefmt='grid'
    ))


if __name__ == '__main__':
    cli(obj={})
