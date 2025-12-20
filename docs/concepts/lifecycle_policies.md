# Lifecycle Policies

S3 Lifecycle policies automate object transitions and deletions.

## Policy Components

### Transitions

Move objects between storage classes:

```json
{
  "Transitions": [
    {
      "Days": 30,
      "StorageClass": "STANDARD_IA"
    },
    {
      "Days": 90,
      "StorageClass": "GLACIER"
    }
  ]
}
```

### Expiration

Delete objects after a period:

```json
{
  "Expiration": {
    "Days": 365
  }
}
```

### Filters

Apply rules to specific objects:

```json
{
  "Filter": {
    "Prefix": "logs/"
  }
}
```

## Storage Classes

| Class | Use Case | Cost | Retrieval |
|-------|----------|------|-----------|
| STANDARD | Active data | High | Instant |
| STANDARD_IA | Infrequent access | Medium | Instant |
| INTELLIGENT_TIERING | Unknown patterns | Variable | Instant |
| GLACIER | Archive | Low | Minutes-hours |
| DEEP_ARCHIVE | Long-term archive | Very low | 12-48 hours |

## Best Practices

1. **Plan transitions carefully**: Consider access patterns
2. **Use prefixes**: Organize objects logically
3. **Test policies**: Use test objects first
4. **Monitor costs**: Track storage class distribution
5. **Validate compliance**: Ensure retention meets requirements

## Example Policy

```python
from s3_log_retention import LifecyclePolicyManager

manager = LifecyclePolicyManager('my-bucket')

manager.create_retention_policy(
    rule_id='log-retention',
    prefix='logs/',
    expiration_days=365,
    transitions=[
        {'Days': 30, 'StorageClass': 'STANDARD_IA'},
        {'Days': 90, 'StorageClass': 'GLACIER'},
        {'Days': 180, 'StorageClass': 'DEEP_ARCHIVE'}
    ]
)
```
