#!/usr/bin/env python3
"""Advanced example: Managing multiple environments."""

from s3_log_retention import LifecyclePolicyManager
import yaml

# Load configuration
with open('configs/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

def create_environment_policies(env_name: str, bucket_name: str):
    """Create policies for an environment."""
    print(f"\nConfiguring {env_name} environment...")
    
    manager = LifecyclePolicyManager(bucket_name)
    
    # Get retention policies from config
    policies = config['retention']['policies']
    
    for log_type, policy in policies.items():
        print(f"  Creating policy for {log_type}...")
        
        success = manager.create_retention_policy(
            rule_id=f"{env_name}-{log_type}",
            prefix=f"logs/{env_name}/{log_type}/",
            expiration_days=policy['retention_days'],
            transitions=policy.get('transitions', [])
        )
        
        if success:
            print(f"    ✓ {log_type} policy created")
        else:
            print(f"    ✗ {log_type} policy failed")

def main():
    """Main function."""
    environments = {
        'dev': 'dev-log-bucket',
        'staging': 'staging-log-bucket',
        'prod': 'prod-log-bucket'
    }
    
    for env, bucket in environments.items():
        create_environment_policies(env, bucket)

if __name__ == '__main__':
    main()
