"""
CLI Module
Command-line interface for S3 log retention automation
"""

import sys
import logging
import click
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from s3_ops import S3Client
from policy_validator import PolicyValidator
from compliance_reporter import ComplianceReporter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@click.group()
@click.option('--region', default=None, help='AWS region')
@click.option('--profile', default=None, help='AWS profile')
@click.option('--verbose', is_flag=True, help='Enable verbose logging')
@click.pass_context
def cli(ctx, region, profile, verbose):
    """S3 Log Retention Automation CLI"""
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    ctx.ensure_object(dict)
    ctx.obj['s3_client'] = S3Client(region_name=region, profile_name=profile)
    ctx.obj['policy_validator'] = PolicyValidator()
    ctx.obj['compliance_reporter'] = ComplianceReporter(
        ctx.obj['s3_client'],
        ctx.obj['policy_validator']
    )


@cli.command()
@click.pass_context
def list_buckets(ctx):
    """List all S3 buckets"""
    s3_client = ctx.obj['s3_client']

    try:
        buckets = s3_client.list_buckets()

        click.echo("\nS3 Buckets:")
        click.echo("-" * 80)

        for bucket in buckets:
            click.echo(f"  {bucket['name']:50} Created: {bucket['creation_date']}")

        click.echo(f"\nTotal: {len(buckets)} buckets")

    except Exception as e:
        logger.error(f"Error listing buckets: {e}")
        sys.exit(1)


@cli.command()
@click.argument('bucket_name')
@click.pass_context
def bucket_info(ctx, bucket_name):
    """Get information about a specific bucket"""
    s3_client = ctx.obj['s3_client']

    try:
        click.echo(f"\nBucket Information: {bucket_name}")
        click.echo("=" * 80)

        # Get location
        location = s3_client.get_bucket_location(bucket_name)
        click.echo(f"Region: {location}")

        # Get size
        stats = s3_client.get_bucket_size(bucket_name)
        click.echo(f"Size: {stats['total_size_gb']} GB")
        click.echo(f"Objects: {stats['object_count']}")

        # Get tags
        tags = s3_client.get_bucket_tags(bucket_name)
        if tags:
            click.echo("\nTags:")
            for key, value in tags.items():
                click.echo(f"  {key}: {value}")

        # Get lifecycle configuration
        lifecycle = s3_client.get_lifecycle_configuration(bucket_name)
        if lifecycle:
            click.echo(f"\nLifecycle Rules: {len(lifecycle.get('Rules', []))}")
        else:
            click.echo("\nLifecycle Configuration: Not configured")

    except Exception as e:
        logger.error(f"Error getting bucket info: {e}")
        sys.exit(1)


@cli.command()
@click.argument('bucket_name')
@click.pass_context
def validate_policy(ctx, bucket_name):
    """Validate lifecycle policy for a bucket"""
    s3_client = ctx.obj['s3_client']
    policy_validator = ctx.obj['policy_validator']

    try:
        click.echo(f"\nValidating lifecycle policy for: {bucket_name}")
        click.echo("=" * 80)

        lifecycle = s3_client.get_lifecycle_configuration(bucket_name)

        if not lifecycle:
            click.echo("❌ No lifecycle policy configured", err=True)
            sys.exit(1)

        result = policy_validator.validate_lifecycle_policy(lifecycle)

        click.echo(f"Valid: {'✓' if result['valid'] else '✗'}")
        click.echo(f"Compliant: {'✓' if result['compliant'] else '✗'}")
        click.echo(f"Rules: {result['rules_count']}")

        if result['issues']:
            click.echo("\nIssues:")
            for issue in result['issues']:
                click.echo(f"  ❌ {issue}")

        if result['warnings']:
            click.echo("\nWarnings:")
            for warning in result['warnings']:
                click.echo(f"  ⚠️  {warning}")

        if result['valid'] and result['compliant']:
            click.echo("\n✓ Policy is valid and compliant")
        else:
            sys.exit(1)

    except Exception as e:
        logger.error(f"Error validating policy: {e}")
        sys.exit(1)


@cli.command()
@click.argument('bucket_name')
@click.option('--format', type=click.Choice(['text', 'json']), default='text', help='Output format')
@click.option('--output', type=click.Path(), help='Output file path')
@click.pass_context
def compliance_report(ctx, bucket_name, format, output):
    """Generate compliance report for a bucket"""
    compliance_reporter = ctx.obj['compliance_reporter']

    try:
        report = compliance_reporter.generate_bucket_report(bucket_name)

        if format == 'json':
            output_text = json.dumps(report, indent=2, default=str)
        else:
            output_text = compliance_reporter.format_report_text(report)

        if output:
            with open(output, 'w') as f:
                f.write(output_text)
            click.echo(f"Report saved to {output}")
        else:
            click.echo(output_text)

    except Exception as e:
        logger.error(f"Error generating compliance report: {e}")
        sys.exit(1)


@cli.command()
@click.option('--format', type=click.Choice(['text', 'json']), default='text', help='Output format')
@click.option('--output', type=click.Path(), help='Output file path')
@click.pass_context
def compliance_report_all(ctx, format, output):
    """Generate compliance report for all buckets"""
    s3_client = ctx.obj['s3_client']
    compliance_reporter = ctx.obj['compliance_reporter']

    try:
        buckets = s3_client.list_buckets()
        bucket_names = [b['name'] for b in buckets]

        click.echo(f"Generating compliance report for {len(bucket_names)} buckets...")

        report = compliance_reporter.generate_multi_bucket_report(bucket_names)

        if format == 'json':
            output_text = json.dumps(report, indent=2, default=str)
        else:
            output_text = compliance_reporter.format_report_text(report)

        if output:
            with open(output, 'w') as f:
                f.write(output_text)
            click.echo(f"Report saved to {output}")
        else:
            click.echo(output_text)

    except Exception as e:
        logger.error(f"Error generating compliance report: {e}")
        sys.exit(1)


@cli.command()
@click.argument('bucket_name')
@click.option('--days', default=30, help='Days threshold for expiration warning')
@click.pass_context
def expiring_objects(ctx, bucket_name, days):
    """List objects that will expire soon"""
    compliance_reporter = ctx.obj['compliance_reporter']

    try:
        objects = compliance_reporter.get_expiring_objects(bucket_name, days)

        click.echo(f"\nObjects expiring within {days} days in {bucket_name}:")
        click.echo("=" * 80)

        if not objects:
            click.echo("No objects expiring soon")
            return

        for obj in objects:
            click.echo(
                f"  {obj['key']:60} "
                f"Expires in: {obj['days_until_expiration']} days"
            )

        click.echo(f"\nTotal: {len(objects)} objects")

    except Exception as e:
        logger.error(f"Error listing expiring objects: {e}")
        sys.exit(1)


if __name__ == '__main__':
    cli(obj={})
