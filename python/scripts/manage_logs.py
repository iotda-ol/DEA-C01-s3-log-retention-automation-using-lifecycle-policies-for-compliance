#!/usr/bin/env python3
"""
S3 Log Manager CLI
Command-line interface for managing S3 log buckets
"""

import click
import logging
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.aws_client import AWSClientManager
from lib.s3_operations import S3Operations
from lib.lifecycle_policy import LifecyclePolicyManager
from lib.config_manager import ConfigManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@click.group()
@click.option('--region', default='us-east-1', help='AWS region')
@click.option('--profile', default=None, help='AWS profile name')
@click.option('--config', default=None, help='Configuration file path')
@click.pass_context
def cli(ctx, region, profile, config):
    """S3 Log Manager - Manage S3 log buckets and lifecycle policies"""
    ctx.ensure_object(dict)
    
    # Initialize configuration
    if config:
        ctx.obj['config'] = ConfigManager(config)
    else:
        ctx.obj['config'] = ConfigManager()
    
    # Initialize AWS client
    ctx.obj['aws'] = AWSClientManager(region_name=region, profile_name=profile)
    ctx.obj['s3_ops'] = S3Operations(ctx.obj['aws'].get_s3_client())


@cli.command()
@click.argument('bucket_name')
@click.option('--region', default='us-east-1', help='AWS region')
@click.pass_context
def create_bucket(ctx, bucket_name, region):
    """Create a new S3 bucket for logs"""
    s3_ops = ctx.obj['s3_ops']
    
    if s3_ops.bucket_exists(bucket_name):
        click.echo(f"Bucket {bucket_name} already exists")
        return
    
    click.echo(f"Creating bucket: {bucket_name}")
    if s3_ops.create_bucket(bucket_name, region):
        click.echo(f"✓ Successfully created bucket: {bucket_name}")
        
        # Enable versioning
        if s3_ops.enable_versioning(bucket_name):
            click.echo(f"✓ Enabled versioning on {bucket_name}")
    else:
        click.echo(f"✗ Failed to create bucket: {bucket_name}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('bucket_name')
@click.option('--template', type=click.Choice(['dea-c01', 'cost-optimized', 'custom']), 
              default='dea-c01', help='Lifecycle policy template')
@click.option('--retention-days', type=int, default=365, help='Retention period in days')
@click.option('--prefix', default='', help='Object key prefix filter')
@click.pass_context
def apply_lifecycle(ctx, bucket_name, template, retention_days, prefix):
    """Apply lifecycle policy to bucket"""
    s3_ops = ctx.obj['s3_ops']
    
    if not s3_ops.bucket_exists(bucket_name):
        click.echo(f"Bucket {bucket_name} does not exist", err=True)
        sys.exit(1)
    
    # Get policy from template
    if template == 'custom':
        rule = LifecyclePolicyManager.create_retention_rule(
            rule_id=f"custom-retention-{retention_days}d",
            expiration_days=retention_days,
            prefix=prefix
        )
    else:
        rule = LifecyclePolicyManager.get_template(template, prefix=prefix)
    
    # Validate rule
    is_valid, error = LifecyclePolicyManager.validate_rule(rule)
    if not is_valid:
        click.echo(f"Invalid lifecycle rule: {error}", err=True)
        sys.exit(1)
    
    click.echo(f"Applying lifecycle policy to {bucket_name}")
    if s3_ops.put_lifecycle_policy(bucket_name, [rule]):
        click.echo(f"✓ Successfully applied lifecycle policy")
        click.echo(f"  Template: {template}")
        click.echo(f"  Retention: {retention_days} days")
    else:
        click.echo(f"✗ Failed to apply lifecycle policy", err=True)
        sys.exit(1)


@cli.command()
@click.argument('bucket_name')
@click.pass_context
def show_lifecycle(ctx, bucket_name):
    """Show current lifecycle policy for bucket"""
    s3_ops = ctx.obj['s3_ops']
    
    rules = s3_ops.get_lifecycle_policy(bucket_name)
    if rules:
        click.echo(f"Lifecycle policies for {bucket_name}:")
        for rule in rules:
            click.echo(f"\n  Rule ID: {rule.get('ID')}")
            click.echo(f"  Status: {rule.get('Status')}")
            if 'Expiration' in rule:
                click.echo(f"  Expiration: {rule['Expiration'].get('Days', 'N/A')} days")
            if 'Transitions' in rule:
                click.echo(f"  Transitions:")
                for transition in rule['Transitions']:
                    click.echo(f"    - {transition['Days']} days → {transition['StorageClass']}")
    else:
        click.echo(f"No lifecycle policy found for {bucket_name}")


@cli.command()
@click.argument('bucket_name')
@click.option('--prefix', default='', help='Object key prefix filter')
@click.pass_context
def list_objects(ctx, bucket_name, prefix):
    """List objects in bucket"""
    s3_ops = ctx.obj['s3_ops']
    
    click.echo(f"Listing objects in {bucket_name} (prefix: '{prefix}')")
    objects = s3_ops.list_objects(bucket_name, prefix)
    
    if objects:
        click.echo(f"\nFound {len(objects)} objects:")
        for obj in objects[:20]:  # Show first 20
            click.echo(f"  {obj['Key']} ({obj['Size']} bytes, {obj['LastModified']})")
        
        if len(objects) > 20:
            click.echo(f"  ... and {len(objects) - 20} more")
    else:
        click.echo("No objects found")


@cli.command()
@click.argument('bucket_name')
@click.option('--prefix', default='', help='Object key prefix filter')
@click.pass_context
def bucket_size(ctx, bucket_name, prefix):
    """Calculate total size of bucket"""
    s3_ops = ctx.obj['s3_ops']
    
    click.echo(f"Calculating size for {bucket_name} (prefix: '{prefix}')")
    size_bytes = s3_ops.get_bucket_size(bucket_name, prefix)
    
    # Convert to human readable format
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            click.echo(f"Total size: {size_bytes:.2f} {unit}")
            break
        size_bytes /= 1024.0


@cli.command()
@click.argument('bucket_name')
@click.option('--days', type=int, required=True, help='Delete objects older than this many days')
@click.option('--prefix', default='', help='Object key prefix filter')
@click.option('--dry-run/--no-dry-run', default=True, help='Dry run (no actual deletion)')
@click.pass_context
def cleanup_old(ctx, bucket_name, days, prefix, dry_run):
    """Delete objects older than specified days"""
    s3_ops = ctx.obj['s3_ops']
    
    if dry_run:
        click.echo(f"DRY RUN: Would delete objects older than {days} days from {bucket_name}")
    else:
        click.echo(f"WARNING: Deleting objects older than {days} days from {bucket_name}")
        if not click.confirm('Are you sure you want to continue?'):
            click.echo("Cancelled")
            return
    
    count = s3_ops.delete_old_objects(bucket_name, days, prefix, dry_run)
    
    if dry_run:
        click.echo(f"Would delete {count} objects")
    else:
        click.echo(f"Deleted {count} objects")


if __name__ == '__main__':
    cli(obj={})
