#!/usr/bin/env python3
"""
S3 Log Retention Automation CLI
Main command-line interface
"""

import click
import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from s3_operations.client import S3Operations
from lifecycle_management.manager import LifecycleManager
from compliance.validator import ComplianceValidator


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@click.group()
@click.option('--region', default='us-east-1', help='AWS region')
@click.option('--profile', default=None, help='AWS profile name')
@click.pass_context
def cli(ctx, region, profile):
    """S3 Log Retention Automation Tool"""
    ctx.ensure_object(dict)
    ctx.obj['region'] = region
    ctx.obj['profile'] = profile
    ctx.obj['s3_ops'] = S3Operations(region=region, profile=profile)
    ctx.obj['lifecycle_mgr'] = LifecycleManager(
        s3_client=ctx.obj['s3_ops'].client,
        region=region
    )
    ctx.obj['validator'] = ComplianceValidator()


@cli.command()
@click.pass_context
def list_buckets(ctx):
    """List all S3 buckets"""
    s3_ops = ctx.obj['s3_ops']
    buckets = s3_ops.list_buckets()
    
    click.echo(f"\nFound {len(buckets)} buckets:\n")
    for bucket in buckets:
        click.echo(f"  - {bucket['Name']} (Created: {bucket['CreationDate']})")


@cli.command()
@click.argument('bucket')
@click.pass_context
def check_policy(ctx, bucket):
    """Check lifecycle policy for a bucket"""
    lifecycle_mgr = ctx.obj['lifecycle_mgr']
    
    policy = lifecycle_mgr.get_lifecycle_policy(bucket)
    
    if policy:
        click.echo(f"\nLifecycle policy for {bucket}:")
        rules = policy.get('Rules', [])
        for rule in rules:
            click.echo(f"\n  Rule: {rule.get('ID')}")
            click.echo(f"  Status: {rule.get('Status')}")
            if 'Expiration' in rule:
                click.echo(f"  Expiration: {rule['Expiration'].get('Days')} days")
            if 'Transitions' in rule:
                for transition in rule['Transitions']:
                    click.echo(f"  Transition: {transition['Days']} days -> {transition['StorageClass']}")
    else:
        click.echo(f"\nNo lifecycle policy found for {bucket}")


@cli.command()
@click.argument('bucket')
@click.option('--retention-days', default=365, help='Retention period in days')
@click.option('--enable-glacier/--no-glacier', default=True, help='Enable Glacier transition')
@click.option('--glacier-days', default=90, help='Days before Glacier transition')
@click.option('--enable-ia/--no-ia', default=True, help='Enable IA transition')
@click.option('--ia-days', default=30, help='Days before IA transition')
@click.pass_context
def apply_policy(ctx, bucket, retention_days, enable_glacier, glacier_days, enable_ia, ia_days):
    """Apply lifecycle policy to a bucket"""
    lifecycle_mgr = ctx.obj['lifecycle_mgr']
    
    rule = lifecycle_mgr.create_compliance_rule(
        retention_days=retention_days,
        enable_glacier=enable_glacier,
        glacier_days=glacier_days,
        enable_ia=enable_ia,
        ia_days=ia_days
    )
    
    success = lifecycle_mgr.set_lifecycle_policy(bucket, [rule])
    
    if success:
        click.echo(f"\n✓ Successfully applied lifecycle policy to {bucket}")
        click.echo(f"  Retention: {retention_days} days")
        if enable_ia:
            click.echo(f"  IA transition: {ia_days} days")
        if enable_glacier:
            click.echo(f"  Glacier transition: {glacier_days} days")
    else:
        click.echo(f"\n✗ Failed to apply policy to {bucket}", err=True)


@cli.command()
@click.argument('bucket')
@click.pass_context
def validate(ctx, bucket):
    """Validate bucket compliance"""
    validator = ctx.obj['validator']
    s3_client = ctx.obj['s3_ops'].client
    
    click.echo(f"\nValidating compliance for: {bucket}\n")
    
    results = validator.validate_bucket(bucket, s3_client)
    
    for check_name, check_result in results['checks'].items():
        status = "✓ PASS" if check_result['compliant'] else "✗ FAIL"
        click.echo(f"{status} - {check_name.replace('_', ' ').title()}")
        
        if not check_result['compliant']:
            for issue in check_result['issues']:
                click.echo(f"    • {issue}")
    
    click.echo(f"\nOverall Status: {'✓ COMPLIANT' if results['compliant'] else '✗ NON-COMPLIANT'}")


@cli.command()
@click.option('--retention-days', default=365, help='Required retention days')
@click.pass_context
def scan_all(ctx, retention_days):
    """Scan all buckets for compliance"""
    s3_ops = ctx.obj['s3_ops']
    validator = ComplianceValidator(required_retention_days=retention_days)
    
    buckets = s3_ops.list_buckets()
    
    click.echo(f"\nScanning {len(buckets)} buckets for compliance...\n")
    
    compliant_count = 0
    non_compliant_count = 0
    
    for bucket in buckets:
        bucket_name = bucket['Name']
        results = validator.validate_bucket(bucket_name, s3_ops.client)
        
        if results['compliant']:
            click.echo(f"✓ {bucket_name}")
            compliant_count += 1
        else:
            click.echo(f"✗ {bucket_name}")
            non_compliant_count += 1
            for check_name, check_result in results['checks'].items():
                if not check_result['compliant']:
                    for issue in check_result['issues']:
                        click.echo(f"    • {issue}")
    
    click.echo(f"\nSummary:")
    click.echo(f"  Compliant: {compliant_count}")
    click.echo(f"  Non-compliant: {non_compliant_count}")
    click.echo(f"  Total: {len(buckets)}")


@cli.command()
@click.argument('bucket')
@click.argument('file_path')
@click.pass_context
def export_policy(ctx, bucket, file_path):
    """Export lifecycle policy to JSON file"""
    lifecycle_mgr = ctx.obj['lifecycle_mgr']
    
    success = lifecycle_mgr.export_policy(bucket, file_path)
    
    if success:
        click.echo(f"\n✓ Exported policy to {file_path}")
    else:
        click.echo(f"\n✗ No policy to export from {bucket}", err=True)


@cli.command()
@click.argument('bucket')
@click.argument('file_path')
@click.pass_context
def import_policy(ctx, bucket, file_path):
    """Import lifecycle policy from JSON file"""
    lifecycle_mgr = ctx.obj['lifecycle_mgr']
    
    success = lifecycle_mgr.import_policy(bucket, file_path)
    
    if success:
        click.echo(f"\n✓ Imported policy to {bucket}")
    else:
        click.echo(f"\n✗ Failed to import policy", err=True)


if __name__ == '__main__':
    cli(obj={})
