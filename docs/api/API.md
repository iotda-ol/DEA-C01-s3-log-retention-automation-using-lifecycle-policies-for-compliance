# API Documentation

## Python Modules

### S3Operations Module

**Location**: `python/src/s3_operations/client.py`

#### Class: S3Operations

Main S3 client wrapper providing common operations.

```python
from s3_operations.client import S3Operations
```

##### Methods

**`__init__(region: str = 'us-east-1', profile: Optional[str] = None)`**

Initialize S3 operations client.

- **Parameters**:
  - `region` (str): AWS region. Default: 'us-east-1'
  - `profile` (Optional[str]): AWS profile name. Default: None

**`list_buckets() -> List[Dict]`**

List all S3 buckets in the account.

- **Returns**: List of bucket dictionaries
- **Raises**: `ClientError` on AWS API errors

**`bucket_exists(bucket_name: str) -> bool`**

Check if a bucket exists and is accessible.

- **Parameters**:
  - `bucket_name` (str): Name of the bucket
- **Returns**: True if bucket exists, False otherwise

**`create_bucket(bucket_name: str, region: Optional[str] = None) -> bool`**

Create a new S3 bucket.

- **Parameters**:
  - `bucket_name` (str): Name of the bucket to create
  - `region` (Optional[str]): AWS region. Default: client region
- **Returns**: True if successful
- **Raises**: `ClientError` on creation failure

**`upload_file(file_path: str, bucket: str, key: str, extra_args: Optional[Dict] = None) -> bool`**

Upload a file to S3.

- **Parameters**:
  - `file_path` (str): Local file path
  - `bucket` (str): Target bucket name
  - `key` (str): Object key in S3
  - `extra_args` (Optional[Dict]): Additional upload arguments
- **Returns**: True if successful
- **Raises**: `ClientError` on upload failure

**`download_file(bucket: str, key: str, file_path: str) -> bool`**

Download a file from S3.

- **Parameters**:
  - `bucket` (str): Source bucket name
  - `key` (str): Object key in S3
  - `file_path` (str): Local file path to save
- **Returns**: True if successful
- **Raises**: `ClientError` on download failure

**`list_objects(bucket: str, prefix: str = '', max_keys: int = 1000) -> List[Dict]`**

List objects in a bucket.

- **Parameters**:
  - `bucket` (str): Bucket name
  - `prefix` (str): Object key prefix filter. Default: ''
  - `max_keys` (int): Maximum number of keys to return. Default: 1000
- **Returns**: List of object dictionaries
- **Raises**: `ClientError` on listing failure

### LifecycleManager Module

**Location**: `python/src/lifecycle_management/manager.py`

#### Class: LifecycleManager

Manager for S3 lifecycle policies.

```python
from lifecycle_management.manager import LifecycleManager
```

##### Methods

**`__init__(s3_client=None, region: str = 'us-east-1')`**

Initialize lifecycle manager.

- **Parameters**:
  - `s3_client`: Boto3 S3 client. Creates new if None
  - `region` (str): AWS region. Default: 'us-east-1'

**`get_lifecycle_policy(bucket: str) -> Optional[Dict]`**

Get lifecycle configuration for a bucket.

- **Parameters**:
  - `bucket` (str): Bucket name
- **Returns**: Lifecycle configuration dict or None if not configured
- **Raises**: `ClientError` on API errors

**`set_lifecycle_policy(bucket: str, rules: List[Dict]) -> bool`**

Set lifecycle configuration for a bucket.

- **Parameters**:
  - `bucket` (str): Bucket name
  - `rules` (List[Dict]): List of lifecycle rules
- **Returns**: True if successful
- **Raises**: `ClientError` on policy application failure

**`delete_lifecycle_policy(bucket: str) -> bool`**

Delete lifecycle configuration from a bucket.

- **Parameters**:
  - `bucket` (str): Bucket name
- **Returns**: True if successful
- **Raises**: `ClientError` on deletion failure

**`create_retention_rule(rule_id: str, retention_days: int, prefix: str = '', status: str = 'Enabled') -> Dict`**

Create a simple retention rule.

- **Parameters**:
  - `rule_id` (str): Unique rule identifier
  - `retention_days` (int): Days to retain objects
  - `prefix` (str): Object key prefix filter. Default: ''
  - `status` (str): Rule status. Default: 'Enabled'
- **Returns**: Lifecycle rule dictionary

**`create_compliance_rule(retention_days: int = 365, enable_glacier: bool = True, glacier_days: int = 90, enable_ia: bool = True, ia_days: int = 30) -> Dict`**

Create a compliance-focused lifecycle rule.

- **Parameters**:
  - `retention_days` (int): Total retention period. Default: 365
  - `enable_glacier` (bool): Enable Glacier transition. Default: True
  - `glacier_days` (int): Days before Glacier transition. Default: 90
  - `enable_ia` (bool): Enable IA transition. Default: True
  - `ia_days` (int): Days before IA transition. Default: 30
- **Returns**: Compliance lifecycle rule

**`validate_rule(rule: Dict) -> bool`**

Validate a lifecycle rule structure.

- **Parameters**:
  - `rule` (Dict): Lifecycle rule dictionary
- **Returns**: True if valid
- **Raises**: `ValueError` if invalid

### ComplianceValidator Module

**Location**: `python/src/compliance/validator.py`

#### Class: ComplianceValidator

Validator for S3 compliance requirements.

```python
from compliance.validator import ComplianceValidator
```

##### Methods

**`__init__(required_retention_days: int = 365)`**

Initialize compliance validator.

- **Parameters**:
  - `required_retention_days` (int): Minimum retention period in days. Default: 365

**`validate_lifecycle_policy(policy: Optional[Dict]) -> Tuple[bool, List[str]]`**

Validate lifecycle policy meets compliance requirements.

- **Parameters**:
  - `policy` (Optional[Dict]): Lifecycle policy configuration
- **Returns**: Tuple of (is_compliant, list of issues)

**`validate_encryption(encryption_config: Optional[Dict]) -> Tuple[bool, List[str]]`**

Validate bucket encryption configuration.

- **Parameters**:
  - `encryption_config` (Optional[Dict]): Bucket encryption configuration
- **Returns**: Tuple of (is_compliant, list of issues)

**`validate_versioning(versioning_config: Optional[Dict]) -> Tuple[bool, List[str]]`**

Validate bucket versioning configuration.

- **Parameters**:
  - `versioning_config` (Optional[Dict]): Bucket versioning configuration
- **Returns**: Tuple of (is_compliant, list of issues)

**`validate_public_access_block(public_access_config: Optional[Dict]) -> Tuple[bool, List[str]]`**

Validate public access block configuration.

- **Parameters**:
  - `public_access_config` (Optional[Dict]): Public access block configuration
- **Returns**: Tuple of (is_compliant, list of issues)

**`validate_bucket(bucket_name: str, s3_client) -> Dict`**

Perform comprehensive bucket compliance validation.

- **Parameters**:
  - `bucket_name` (str): Name of the bucket to validate
  - `s3_client`: Boto3 S3 client
- **Returns**: Validation results dictionary with structure:
  ```python
  {
      'bucket': str,
      'compliant': bool,
      'checks': {
          'lifecycle': {'compliant': bool, 'issues': List[str]},
          'encryption': {'compliant': bool, 'issues': List[str]},
          'versioning': {'compliant': bool, 'issues': List[str]},
          'public_access': {'compliant': bool, 'issues': List[str]}
      }
  }
  ```

## Terraform Modules

### S3 Bucket Module

**Location**: `terraform/modules/s3-bucket`

#### Resources Created

- `aws_s3_bucket.main` - Main S3 bucket
- `aws_s3_bucket_versioning.main` - Versioning configuration
- `aws_s3_bucket_server_side_encryption_configuration.main` - Encryption
- `aws_s3_bucket_public_access_block.main` - Public access block
- `aws_s3_bucket_logging.main` - Access logging
- `aws_s3_bucket_ownership_controls.main` - Ownership controls

#### Inputs

See `terraform/modules/s3-bucket/variables.tf` for all variables.

Key variables:
- `bucket_name` (string, required): Name of the S3 bucket
- `environment` (string): Environment name
- `enable_versioning` (bool): Enable bucket versioning
- `enable_encryption` (bool): Enable server-side encryption
- `enable_logging` (bool): Enable access logging

#### Outputs

- `bucket_id`: ID of the S3 bucket
- `bucket_arn`: ARN of the S3 bucket
- `bucket_domain_name`: Domain name of the bucket
- `bucket_regional_domain_name`: Regional domain name

### Lifecycle Policy Module

**Location**: `terraform/modules/lifecycle-policy`

#### Resources Created

- `aws_s3_bucket_lifecycle_configuration.main` - Lifecycle configuration

#### Inputs

Key variables:
- `bucket_id` (string, required): S3 bucket ID
- `retention_days` (number): Days to retain objects
- `enable_ia_transition` (bool): Enable IA transition
- `enable_glacier_transition` (bool): Enable Glacier transition

#### Outputs

- `lifecycle_rule_ids`: List of lifecycle rule IDs

### IAM Module

**Location**: `terraform/modules/iam`

#### Resources Created

- `aws_iam_role.main` - IAM role
- `aws_iam_policy.s3_access` - S3 access policy
- `aws_iam_role_policy_attachment.s3_access` - Policy attachment

#### Inputs

Key variables:
- `role_name` (string, required): Name of the IAM role
- `services` (list(string)): AWS services that can assume role
- `bucket_arns` (list(string), required): ARNs of S3 buckets

#### Outputs

- `role_arn`: ARN of the IAM role
- `role_name`: Name of the IAM role
- `policy_arn`: ARN of the IAM policy

## CLI Commands

See `python/main.py` for the CLI implementation.

### Available Commands

- `list-buckets`: List all S3 buckets
- `check-policy BUCKET`: Check lifecycle policy
- `apply-policy BUCKET`: Apply lifecycle policy
- `validate BUCKET`: Validate bucket compliance
- `scan-all`: Scan all buckets for compliance
- `export-policy BUCKET FILE`: Export policy to file
- `import-policy BUCKET FILE`: Import policy from file

### Global Options

- `--region TEXT`: AWS region
- `--profile TEXT`: AWS profile name
- `--help`: Show help message
