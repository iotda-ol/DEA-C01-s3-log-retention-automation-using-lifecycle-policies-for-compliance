"""Command-line interface for S3 log retention management."""

import sys
import click
from s3_log_retention import LifecyclePolicyManager, S3LogManager
from s3_log_retention.logger import setup_logging, get_logger


@click.group()
@click.option('--log-level', default='INFO', help='Logging level')
@click.option('--json-logs', is_flag=True, help='Output logs in JSON format')
@click.pass_context
def cli(ctx, log_level, json_logs):
    """S3 Log Retention Management CLI."""
    setup_logging(level=log_level, json_logs=json_logs)
    ctx.ensure_object(dict)
    ctx.obj['logger'] = get_logger(__name__)


@cli.command()
@click.option('--bucket', required=True, help='S3 bucket name')
@click.option('--prefix', default='', help='Object prefix to filter')
@click.option('--region', help='AWS region')
@click.pass_context
def list_logs(ctx, bucket, prefix, region):
    """List log files in S3 bucket."""
    logger = ctx.obj['logger']
    logger.info("Listing logs", bucket=bucket, prefix=prefix)

    manager = S3LogManager(bucket, region)
    logs = manager.list_logs(prefix=prefix)

    for log in logs:
        click.echo(f"{log['Key']}\t{log['Size']}\t{log['LastModified']}")

    logger.info(f"Found {len(logs)} log files")


@cli.command()
@click.option('--bucket', required=True, help='S3 bucket name')
@click.option('--rule-id', required=True, help='Lifecycle rule ID')
@click.option('--prefix', default='', help='Object prefix')
@click.option('--retention-days', type=int, required=True, help='Days to retain logs')
@click.option('--archive-days', type=int, default=30, help='Days before archiving')
@click.option('--region', help='AWS region')
@click.pass_context
def create_policy(ctx, bucket, rule_id, prefix, retention_days, archive_days, region):
    """Create a lifecycle retention policy."""
    logger = ctx.obj['logger']
    logger.info("Creating lifecycle policy", bucket=bucket, rule_id=rule_id)

    manager = LifecyclePolicyManager(bucket, region)

    transitions = []
    if archive_days < retention_days:
        transitions.append({'Days': archive_days, 'StorageClass': 'STANDARD_IA'})

    if retention_days > 90:
        transitions.append({'Days': 90, 'StorageClass': 'GLACIER'})

    success = manager.create_retention_policy(
        rule_id=rule_id,
        prefix=prefix,
        expiration_days=retention_days,
        transitions=transitions if transitions else None
    )

    if success:
        click.echo(f"✓ Successfully created lifecycle policy: {rule_id}")
        logger.info("Policy created successfully")
    else:
        click.echo(f"✗ Failed to create lifecycle policy", err=True)
        logger.error("Policy creation failed")
        sys.exit(1)


@cli.command()
@click.option('--bucket', required=True, help='S3 bucket name')
@click.option('--region', help='AWS region')
@click.pass_context
def list_policies(ctx, bucket, region):
    """List all lifecycle policies for a bucket."""
    logger = ctx.obj['logger']
    logger.info("Listing lifecycle policies", bucket=bucket)

    manager = LifecyclePolicyManager(bucket, region)
    rules = manager.get_lifecycle_rules()

    if not rules:
        click.echo("No lifecycle policies found")
        return

    for rule in rules:
        click.echo(f"\nRule ID: {rule['ID']}")
        click.echo(f"  Status: {rule['Status']}")
        click.echo(f"  Prefix: {rule.get('Filter', {}).get('Prefix', 'N/A')}")

        if 'Expiration' in rule:
            click.echo(f"  Expiration: {rule['Expiration'].get('Days', 'N/A')} days")

        if 'Transitions' in rule:
            click.echo("  Transitions:")
            for trans in rule['Transitions']:
                click.echo(f"    - {trans['Days']} days → {trans['StorageClass']}")


@cli.command()
@click.option('--bucket', required=True, help='S3 bucket name')
@click.option('--region', help='AWS region')
@click.pass_context
def validate_policy(ctx, bucket, region):
    """Validate lifecycle policy configuration."""
    logger = ctx.obj['logger']
    logger.info("Validating lifecycle policy", bucket=bucket)

    manager = LifecyclePolicyManager(bucket, region)
    result = manager.validate_policy()

    click.echo(f"\nValidation Result: {'✓ VALID' if result['valid'] else '✗ INVALID'}")
    click.echo(f"Rule Count: {result['rule_count']}")

    if result['errors']:
        click.echo("\nErrors:")
        for error in result['errors']:
            click.echo(f"  ✗ {error}")

    if result['warnings']:
        click.echo("\nWarnings:")
        for warning in result['warnings']:
            click.echo(f"  ⚠ {warning}")

    if not result['valid']:
        sys.exit(1)


if __name__ == '__main__':
    cli(obj={})
