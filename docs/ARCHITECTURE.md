# Architecture Documentation

## System Overview

The S3 Log Retention Automation solution provides an automated, compliant, and cost-effective way to manage log data in Amazon S3. The architecture follows DEA-C01 best practices and implements Infrastructure as Code using Terraform and Python.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Application Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Servers    │  │ Applications │  │   Services   │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                 │                  │                   │
│         └─────────────────┴──────────────────┘                   │
│                           │                                      │
│                      Log Events                                  │
└───────────────────────────┼──────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Storage Layer (S3)                         │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                     S3 Bucket                              │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │  │
│  │  │ Standard │→ │Standard-IA│→ │ Glacier  │→ │  Delete  │  │  │
│  │  │  (0-30d) │  │ (30-90d)  │  │(90-365d) │  │ (365d+)  │  │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │  │
│  │                                                            │  │
│  │  Features:                                                 │  │
│  │  • Encryption (AES256/KMS)                                 │  │
│  │  • Versioning                                              │  │
│  │  • Lifecycle Policies                                      │  │
│  │  • Public Access Block                                     │  │
│  └───────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Automation Layer                             │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │  Lifecycle  │  │   Lambda     │  │  EventBridge │           │
│  │   Policies  │  │  Functions   │  │    Rules     │           │
│  └─────────────┘  └──────────────┘  └──────────────┘           │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Monitoring Layer                              │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │ CloudWatch  │  │  Dashboards  │  │    Alarms    │           │
│  │   Metrics   │  │              │  │     SNS      │           │
│  └─────────────┘  └──────────────┘  └──────────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. S3 Bucket Module

**Purpose**: Creates and configures S3 buckets for log storage

**Features**:
- Server-side encryption (AES256 or KMS)
- Versioning for data protection
- Public access blocking
- Bucket ownership controls
- Optional access logging
- S3 Inventory for tracking

**Configuration**: `terraform/modules/s3_bucket/`

### 2. Lifecycle Policy Module

**Purpose**: Manages automated data retention and transitions

**Features**:
- Configurable retention periods
- Multi-tier storage transitions
- Noncurrent version management
- Incomplete multipart upload cleanup
- Support for multiple rule sets

**Configuration**: `terraform/modules/lifecycle_policy/`

**Typical Lifecycle**:
```
Day 0:   STANDARD
Day 30:  → STANDARD_IA
Day 90:  → GLACIER
Day 365: → DELETE (compliance)
```

### 3. IAM Module

**Purpose**: Manages access control and permissions

**Features**:
- Lambda execution roles
- EventBridge invoke permissions
- S3 inventory roles
- Cross-account access patterns
- MFA requirements

**Configuration**: `terraform/modules/iam/`

### 4. Monitoring Module

**Purpose**: Provides observability and alerting

**Features**:
- CloudWatch metrics
- Custom dashboards
- Configurable alarms
- SNS notifications
- Log groups

**Configuration**: `terraform/modules/monitoring/`

## Python Components

### 1. S3 Operations (`python/src/s3_ops/`)

**Purpose**: High-level S3 client interface

**Capabilities**:
- List and inspect buckets
- Get lifecycle configurations
- Calculate bucket sizes
- Upload/download objects
- Manage tags
- Retry logic with exponential backoff

### 2. Policy Validator (`python/src/policy_validator/`)

**Purpose**: Validate compliance with retention policies

**Capabilities**:
- Lifecycle policy validation
- Bucket policy security checks
- Compliance reporting
- Minimum retention enforcement
- Storage class validation

### 3. Compliance Reporter (`python/src/compliance_reporter/`)

**Purpose**: Generate compliance reports

**Capabilities**:
- Single and multi-bucket reports
- Text and JSON output formats
- Expiring objects tracking
- Statistics collection
- Compliance scoring

### 4. CLI Tool (`python/src/cli/`)

**Purpose**: Command-line interface for management

**Commands**:
- `list-buckets`: List all S3 buckets
- `bucket-info`: Get bucket details
- `validate-policy`: Check policy compliance
- `compliance-report`: Generate reports
- `expiring-objects`: Find objects nearing expiration

## Data Flow

### 1. Log Ingestion

```
Application → S3 Bucket → Lifecycle Policy Applied
```

### 2. Lifecycle Management

```
S3 Lifecycle Engine → Check Age → Apply Transitions → Delete if Expired
```

### 3. Compliance Monitoring

```
Python CLI/Lambda → Fetch Config → Validate → Generate Report → Alert
```

## Security Architecture

### Defense in Depth

1. **Network Security**:
   - VPC endpoints for private access
   - Public access blocking

2. **Encryption**:
   - At-rest: AES256 or KMS
   - In-transit: TLS 1.2+

3. **Access Control**:
   - IAM policies (least privilege)
   - Bucket policies
   - ACLs disabled (BucketOwnerEnforced)

4. **Monitoring**:
   - CloudWatch alarms
   - Access logging
   - CloudTrail events

## Compliance Features

### DEA-C01 Alignment

1. **Data Retention**: 365-day minimum retention
2. **Cost Optimization**: Automated tier transitions
3. **Security**: Encryption and access controls
4. **Automation**: Infrastructure as Code
5. **Monitoring**: Continuous compliance validation

### Audit Trail

- S3 access logs
- CloudTrail events
- Lifecycle action logs
- Compliance reports

## Scalability

### Horizontal Scaling

- Multiple buckets per environment
- Multi-region support
- Cross-account patterns

### Performance

- S3 automatic scaling
- Optimized API calls
- Batch operations
- Pagination support

## Disaster Recovery

### Backup Strategy

- Versioning enabled
- Cross-region replication (optional)
- Lifecycle policy preservation

### Recovery

- Point-in-time recovery via versions
- Automated restoration scripts
- RTO: < 1 hour
- RPO: Near-zero with versioning

## Cost Optimization

### Storage Tiering

| Tier | Days | Cost | Retrieval |
|------|------|------|-----------|
| STANDARD | 0-30 | $$$ | Instant |
| STANDARD_IA | 30-90 | $$ | Fast |
| GLACIER | 90-365 | $ | Hours |

### Cost Savings

- Automated transitions: ~70% savings
- Lifecycle deletions: Prevents unbounded growth
- Inventory optimization: Identifies savings opportunities

## Best Practices

### Terraform Modules

1. Use variables for flexibility
2. Output important values
3. Include validation rules
4. Document with comments
5. Version modules

### Python Code

1. Use type hints
2. Implement retry logic
3. Log appropriately
4. Handle errors gracefully
5. Write unit tests

### Operations

1. Test in non-prod first
2. Monitor after deployment
3. Regular compliance checks
4. Review and optimize costs
5. Update documentation

## Future Enhancements

- Lambda-based automated processing
- Machine learning for log analysis
- Multi-account organization support
- Advanced cost forecasting
- Automated remediation
