# S3 Lifecycle Policy Basics

## What are S3 Lifecycle Policies?

S3 Lifecycle policies are rules that automatically manage your objects throughout their lifetime. They help you:
- Reduce storage costs by transitioning objects to cheaper storage classes
- Maintain compliance by automatically deleting old data
- Automate data management without manual intervention

## Key Concepts

### 1. Lifecycle Rules
A lifecycle rule consists of:
- **Rule ID**: A unique identifier for the rule
- **Status**: Enabled or Disabled
- **Scope**: Which objects the rule applies to (prefix, tags)
- **Actions**: What happens to the objects (transition or expiration)

### 2. Transitions
Move objects between storage classes based on age:
- **STANDARD** → **STANDARD_IA** (after 30 days)
- **STANDARD_IA** → **GLACIER** (after 90 days)
- **GLACIER** → **DEEP_ARCHIVE** (after 180 days)

### 3. Expirations
Permanently delete objects after a specified time:
- Delete objects after 365 days (1 year retention)
- Clean up incomplete multipart uploads
- Delete expired object delete markers

## Example Lifecycle Policy

```json
{
  "Rules": [
    {
      "Id": "OneYearRetention",
      "Status": "Enabled",
      "Prefix": "logs/",
      "Transitions": [
        {
          "Days": 90,
          "StorageClass": "GLACIER"
        }
      ],
      "Expiration": {
        "Days": 365
      }
    }
  ]
}
```

## Compliance Use Case

For log retention compliance:
1. **Store** logs in S3 STANDARD for quick access (0-30 days)
2. **Transition** to STANDARD_IA for infrequent access (30-90 days)
3. **Archive** to GLACIER for long-term storage (90-365 days)
4. **Delete** after 365 days to meet compliance requirements

## Best Practices

1. **Test First**: Apply policies to a test bucket before production
2. **Use Prefixes**: Target specific directories with prefix filters
3. **Monitor Costs**: Track storage class distribution and costs
4. **Version Control**: Keep lifecycle policies in version control
5. **Document**: Clearly document retention requirements

## Next Steps

- Review AWS S3 storage classes and pricing
- Understand your organization's compliance requirements
- Learn how to create and apply lifecycle policies
- Move to [02-aws-setup.md](02-aws-setup.md)
