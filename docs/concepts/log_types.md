# Log Types

Different types of logs have different retention requirements.

## Application Logs

**Purpose**: Track application behavior and errors

**Retention**: Typically 90-180 days

**Storage Transition**:
- 0-30 days: Standard
- 30-90 days: Standard-IA
- 90+ days: Glacier

## Access Logs

**Purpose**: Track access to resources (S3, CloudFront, ALB)

**Retention**: Typically 90-365 days

**Storage Transition**:
- 0-30 days: Standard
- 30-90 days: Standard-IA
- 90-365 days: Glacier

## Audit Logs

**Purpose**: Security and compliance auditing

**Retention**: 1-7 years (compliance dependent)

**Storage Transition**:
- 0-90 days: Standard
- 90-180 days: Standard-IA
- 180-365 days: Glacier
- 365+ days: Deep Archive

## Security Logs

**Purpose**: Security events and incidents

**Retention**: 1-3 years

**Storage Transition**:
- 0-90 days: Standard
- 90-180 days: Standard-IA
- 180+ days: Glacier

## Compliance Requirements

| Framework | Min Retention | Typical Retention |
|-----------|---------------|-------------------|
| GDPR      | As needed     | 1-2 years        |
| SOC 2     | 1 year        | 1-3 years        |
| HIPAA     | 6 years       | 7 years          |
| PCI DSS   | 1 year        | 1-3 years        |
| ISO 27001 | As defined    | 1-3 years        |
