# Architecture Overview

## System Architecture

This S3 log retention automation solution follows a modular, cloud-native architecture designed for scalability, security, and compliance.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     AWS Cloud Environment                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌───────────────┐         ┌───────────────┐                │
│  │               │         │               │                │
│  │  Application  │────────▶│  Log Bucket   │                │
│  │   Services    │         │   (S3)        │                │
│  │               │         │               │                │
│  └───────────────┘         └───────┬───────┘                │
│                                    │                         │
│                            ┌───────▼────────┐                │
│                            │   Lifecycle    │                │
│                            │    Policy      │                │
│                            └───────┬────────┘                │
│                                    │                         │
│              ┌─────────────────────┼─────────────────┐       │
│              │                     │                 │       │
│         ┌────▼─────┐      ┌────────▼──────┐  ┌──────▼─────┐ │
│         │ Standard │      │  Glacier      │  │   Delete   │ │
│         │ (0-30d)  │      │  (90-365d)    │  │  (>365d)   │ │
│         └──────────┘      └───────────────┘  └────────────┘ │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐   │
│  │            Monitoring & Compliance                    │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐     │   │
│  │  │ CloudWatch │  │AWS Config  │  │CloudTrail  │     │   │
│  │  └────────────┘  └────────────┘  └────────────┘     │   │
│  └───────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. Storage Layer (S3)

- **Primary Bucket**: Stores application logs
- **Access Logs Bucket**: Stores S3 access logs for audit
- **Features**:
  - Server-side encryption (AES256 or KMS)
  - Versioning enabled
  - Public access blocked
  - Cross-region replication (optional)

### 2. Lifecycle Management

- **Transitions**:
  - Day 0-30: STANDARD storage class
  - Day 30-90: STANDARD_IA (Infrequent Access)
  - Day 90-365: GLACIER
  - Day 365+: Automatic deletion

- **Benefits**:
  - Cost optimization
  - Compliance adherence
  - Automated operations

### 3. Access Control (IAM)

```
┌─────────────────────────────────────────┐
│         IAM Role Architecture           │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────────┐    ┌──────────────┐  │
│  │   EC2/ECS    │    │   Lambda     │  │
│  │  Applications│    │  Functions   │  │
│  └──────┬───────┘    └──────┬───────┘  │
│         │                   │          │
│         └────────┬──────────┘          │
│                  │                     │
│           ┌──────▼───────┐             │
│           │  IAM Role    │             │
│           │ (Least       │             │
│           │  Privilege)  │             │
│           └──────┬───────┘             │
│                  │                     │
│           ┌──────▼───────┐             │
│           │  S3 Policy   │             │
│           │  - Read      │             │
│           │  - Write     │             │
│           │  - Lifecycle │             │
│           └──────────────┘             │
└─────────────────────────────────────────┘
```

### 4. Monitoring & Compliance

- **CloudWatch**: Metrics and alarms
- **CloudTrail**: API audit logging
- **AWS Config**: Configuration compliance
- **Custom Validation**: Python-based compliance checks

## Infrastructure as Code

### Terraform Module Structure

```
terraform/
├── modules/              # Reusable components
│   ├── s3-bucket/       # Bucket with best practices
│   ├── lifecycle-policy/# Lifecycle configuration
│   └── iam/             # Access control
└── environments/        # Environment-specific
    ├── dev/
    ├── staging/
    └── prod/
```

### Python Automation

```
python/
├── src/
│   ├── s3_operations/      # S3 client wrapper
│   ├── lifecycle_management/# Policy management
│   └── compliance/         # Validation
└── main.py                # CLI interface
```

## Data Flow

### Log Upload Flow

```
1. Application generates log
2. Log uploaded to S3 (encrypted)
3. S3 event triggers notification
4. Metadata stored for tracking
5. Lifecycle policy applied automatically
```

### Lifecycle Flow

```
Day 0:   Upload → STANDARD storage
Day 30:  Transition → STANDARD_IA
Day 90:  Transition → GLACIER
Day 365: Deletion (compliance)
```

## Security Architecture

### Defense in Depth

1. **Network Level**
   - VPC endpoints for S3 (optional)
   - Private subnet access

2. **Access Control**
   - IAM roles with least privilege
   - Bucket policies
   - SCPs (Service Control Policies)

3. **Encryption**
   - At rest: AES256 or KMS
   - In transit: TLS 1.2+

4. **Monitoring**
   - CloudTrail for all API calls
   - GuardDuty for threat detection
   - Security Hub for compliance

5. **Compliance**
   - Automated validation
   - Regular audits
   - Reporting

## Scalability

### Horizontal Scaling

- Multiple buckets for different log types
- Regional deployment
- Cross-account architecture

### Performance

- S3 Transfer Acceleration (optional)
- Multipart uploads for large files
- Parallel operations

## Disaster Recovery

### Backup Strategy

1. **Cross-Region Replication**
   - Primary: us-east-1
   - DR: us-west-2

2. **Versioning**
   - Protect against accidental deletion
   - Point-in-time recovery

3. **Recovery Procedures**
   - Documented runbooks
   - Tested recovery processes
   - RTO: 4 hours
   - RPO: 15 minutes

## Cost Optimization

### Storage Class Transitions

| Age | Storage Class | Cost (per GB/month) | Use Case |
|-----|---------------|---------------------|----------|
| 0-30d | STANDARD | $0.023 | Active logs |
| 30-90d | STANDARD_IA | $0.0125 | Occasional access |
| 90-365d | GLACIER | $0.004 | Archive |
| 365d+ | Deleted | $0 | Compliance met |

### Estimated Monthly Cost

For 1TB of logs:
- Month 1: $23 (all STANDARD)
- Month 2: $11.50 (50% IA)
- Month 6: $6 (mostly GLACIER)
- Yearly average: ~$10/month

## Integration Points

### AWS Services

- **S3**: Primary storage
- **IAM**: Access control
- **CloudWatch**: Monitoring
- **CloudTrail**: Audit logging
- **AWS Config**: Compliance
- **Lambda**: Event processing (optional)
- **SNS**: Notifications

### Third-Party Tools

- Terraform: Infrastructure deployment
- Python: Automation and validation
- Git: Version control
- CI/CD: Automated deployment

## Best Practices

1. **Modular Design**
   - Reusable Terraform modules
   - Composable Python functions

2. **Infrastructure as Code**
   - All resources in version control
   - Peer review for changes

3. **Security First**
   - Least privilege access
   - Encryption everywhere
   - Regular audits

4. **Automation**
   - Automated policy application
   - Continuous compliance checking
   - Self-healing where possible

5. **Documentation**
   - Architecture diagrams
   - Runbooks
   - API documentation
