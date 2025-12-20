# Architecture Documentation

## System Overview

This project implements an automated S3 log retention system that meets DEA-C01 compliance requirements through Infrastructure as Code (Terraform) and Python automation.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Application Layer                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Web Apps │  │ Services │  │ Lambda   │  │   EC2    │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
└───────┼─────────────┼─────────────┼─────────────┼──────────┘
        │             │             │             │
        └─────────────┴─────────────┴─────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────────┐
        │         IAM Roles & Policies              │
        │  ┌─────────────┐  ┌─────────────┐        │
        │  │ Log Writer  │  │ Log Reader  │        │
        │  └─────────────┘  └─────────────┘        │
        └───────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      S3 Bucket                               │
│  ┌────────────────────────────────────────────────────┐     │
│  │ Lifecycle Policy (DEA-C01 Compliant)               │     │
│  │  • Day 0-30:    STANDARD                           │     │
│  │  • Day 30-90:   STANDARD_IA  (50% cheaper)         │     │
│  │  • Day 90-180:  GLACIER      (83% cheaper)         │     │
│  │  • Day 180-365: DEEP_ARCHIVE (96% cheaper)         │     │
│  │  • Day 365+:    DELETED      (compliance)          │     │
│  └────────────────────────────────────────────────────┘     │
│                                                               │
│  Features:                                                    │
│  • Server-side encryption (AES256 or KMS)                    │
│  • Versioning enabled                                        │
│  • Public access blocked                                     │
│  • Access logging                                            │
└─────────────────────────────────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
    ┌───────────────────┐   ┌───────────────────┐
    │   CloudWatch      │   │   CloudTrail      │
    │   • Metrics       │   │   • API Audit     │
    │   • Alarms        │   │   • Compliance    │
    │   • Dashboards    │   │   • Security      │
    └─────────┬─────────┘   └───────────────────┘
              │
              ▼
    ┌───────────────────┐
    │   SNS Topics      │
    │   • Email Alerts  │
    │   • Slack/PagerDuty│
    └───────────────────┘
```

## Component Architecture

### 1. Terraform Modules (Infrastructure Layer)

**Module Structure**:
```
terraform/modules/
├── s3-bucket/          # S3 bucket creation with security
├── lifecycle-policy/   # Lifecycle policy management
├── iam/               # IAM roles and policies
└── logging/           # CloudWatch & CloudTrail setup
```

**Design Principles**:
- **Modularity**: Each module is self-contained and reusable
- **Composability**: Modules can be combined for complex scenarios
- **Configuration**: Environment-specific variables
- **State Management**: Remote state in S3 with locking

### 2. Python Library (Automation Layer)

**Library Structure**:
```
python/lib/
├── aws_client.py       # AWS client management (singleton pattern)
├── s3_operations.py    # S3 operations (CRUD, lifecycle)
├── lifecycle_policy.py # Policy templates and validation
└── config_manager.py   # Configuration handling
```

**Design Patterns**:
- **Factory Pattern**: AWS client creation
- **Template Method**: Lifecycle policy generation
- **Strategy Pattern**: Different compliance templates
- **Singleton**: AWS session management

### 3. Automation Scripts

**Script Architecture**:
```
python/
├── scripts/        # CLI tools (Click-based)
├── validators/     # Compliance checking
├── reporting/      # Report generation
└── monitoring/     # Metrics and alerting
```

## Data Flow

### Log Ingestion Flow
```
1. Application generates logs
2. Logs sent to S3 via SDK/CLI
3. S3 accepts with IAM validation
4. Object stored in STANDARD class
5. Metadata tagged with timestamp
6. CloudTrail records API call
7. CloudWatch metrics updated
```

### Lifecycle Transition Flow
```
1. Daily lifecycle evaluation runs
2. Objects matched against rules
3. Age calculated from creation date
4. Transition action determined
5. Object moved to target storage class
6. CloudWatch event emitted
7. Metric updated
```

### Compliance Validation Flow
```
1. Scheduled Lambda/Script runs
2. Fetch bucket configuration
3. Validate against DEA-C01 requirements:
   ✓ Versioning enabled
   ✓ Encryption enabled
   ✓ Public access blocked
   ✓ Lifecycle policy exists
   ✓ 365-day retention enforced
4. Generate compliance report
5. Send notifications if non-compliant
```

## Security Architecture

### Defense in Depth

**Layer 1: Network**
- VPC endpoints for S3 (optional)
- No internet gateway required
- Traffic stays on AWS backbone

**Layer 2: IAM**
- Least privilege access
- Service-specific roles
- MFA for critical operations
- Session policies

**Layer 3: Encryption**
- At-rest: AES256 or KMS
- In-transit: TLS 1.2+
- Bucket keys for cost optimization

**Layer 4: Access Control**
- Public access blocked
- Bucket policies
- Access point policies
- SCPs (in Organizations)

**Layer 5: Monitoring**
- CloudTrail for all API calls
- Access logging
- CloudWatch alarms
- GuardDuty integration

## Scalability Considerations

### Horizontal Scaling
- S3 automatically scales
- No provisioning required
- Handles billions of objects
- Parallel processing support

### Performance Optimization
- Request rate: 5,500 GET/s per prefix
- Partition key strategy for high throughput
- Transfer acceleration (if needed)
- Multipart upload for large files

### Cost Optimization
- Lifecycle transitions reduce storage costs by 96%
- Intelligent-Tiering for unknown access patterns
- S3 Inventory for cost analysis
- Reserved capacity for Glacier (if predictable)

## Disaster Recovery

### Backup Strategy
```
Primary Region (us-east-1)
    ↓ Cross-Region Replication
DR Region (us-west-2)
    ↓ Lifecycle to Glacier
Long-term Archive
```

### RPO/RTO Targets
- **RPO**: Near-zero (replication is continuous)
- **RTO**: < 1 hour (automated failover)

### DR Testing
- Quarterly DR drills
- Automated restore testing
- Runbook validation

## Monitoring & Observability

### Key Metrics
- Bucket size (bytes)
- Object count
- Request rate
- 4xx/5xx errors
- Lifecycle transitions
- Storage class distribution

### Alerting
- Storage quota exceeded
- Lifecycle policy failures
- Encryption disabled
- Public access enabled
- Compliance violations

### Dashboards
- Real-time metrics
- Cost analysis
- Compliance status
- Performance metrics

## Integration Points

### Upstream (Log Producers)
- Application SDKs (boto3, aws-sdk)
- Log shippers (Fluentd, Logstash)
- CloudWatch Logs subscription
- Kinesis Firehose

### Downstream (Log Consumers)
- Athena for querying
- EMR for processing
- Glue for ETL
- QuickSight for visualization
- Third-party SIEM tools

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| IaC | Terraform 1.6+ | Infrastructure provisioning |
| Language | Python 3.8+ | Automation scripts |
| SDK | Boto3 | AWS API interaction |
| CLI | AWS CLI v2 | Manual operations |
| Storage | S3 | Object storage |
| Monitoring | CloudWatch | Metrics & alarms |
| Audit | CloudTrail | API logging |
| Notifications | SNS | Alerting |

## Best Practices

1. **Immutable Infrastructure**: Never modify, always replace
2. **Version Control**: All IaC in Git
3. **Code Review**: Terraform plans reviewed before apply
4. **Testing**: Validate in dev before prod
5. **Documentation**: Keep architecture docs updated
6. **Tagging**: Consistent resource tagging
7. **Monitoring**: Proactive alerting
8. **Security**: Regular security audits
9. **Cost**: Monthly cost reviews
10. **Compliance**: Automated compliance checking

## Future Enhancements

- [ ] Multi-region active-active deployment
- [ ] ML-based anomaly detection
- [ ] Automated cost optimization
- [ ] Self-healing automation
- [ ] Advanced analytics with Athena
- [ ] Integration with data lake
- [ ] Real-time log streaming
- [ ] Compression optimization
