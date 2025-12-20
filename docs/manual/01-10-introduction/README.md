# Steps 1-10: Introduction and Prerequisites (Novice Level)

## Step 1: Understanding DEA-C01 Log Retention Requirements

**Objective**: Learn what DEA-C01 compliance requires for log retention.

**What is DEA-C01?**
DEA-C01 (AWS Certified Data Engineer - Associate) emphasizes best practices for data engineering, including:
- Automated log retention policies
- Cost-effective storage management
- Compliance with retention requirements
- Minimal operational overhead

**Key Requirements**:
- Logs must be retained for **365 days** (1 year)
- Automatic deletion after retention period
- Secure storage with encryption
- Audit trail of all log operations
- Cost optimization through storage class transitions

**Why S3 Lifecycle Policies?**
- Automatic management (set it and forget it)
- No manual intervention required
- Cost savings through storage class transitions
- Built-in compliance features
- Scalable to billions of objects

---

## Step 2: Understanding S3 Basics

**What is Amazon S3?**
Amazon Simple Storage Service (S3) is an object storage service offering:
- Unlimited storage capacity
- 99.999999999% (11 nines) durability
- Multiple storage classes for cost optimization
- Integrated lifecycle management
- Encryption and security features

**Key S3 Concepts**:
- **Bucket**: Container for objects (like a folder)
- **Object**: Individual file stored in S3
- **Key**: Unique identifier for an object
- **Storage Class**: Determines access speed and cost
- **Versioning**: Keep multiple versions of objects

**S3 Storage Classes** (from fastest/most expensive to slowest/cheapest):
1. **STANDARD**: Frequent access, low latency
2. **STANDARD_IA**: Infrequent access, lower cost
3. **GLACIER**: Archive, retrieval in minutes to hours
4. **DEEP_ARCHIVE**: Long-term archive, retrieval in 12 hours

---

## Step 3: Understanding Lifecycle Policies

**What are Lifecycle Policies?**
Automated rules that manage objects throughout their lifecycle:
- **Transition Actions**: Move objects to cheaper storage classes
- **Expiration Actions**: Delete objects after specified time
- **Versioning Actions**: Manage previous versions

**Example Lifecycle Timeline**:
```
Day 0:    Object created → STANDARD storage
Day 30:   Transition to STANDARD_IA (save 50% on storage)
Day 90:   Transition to GLACIER (save 80% on storage)
Day 180:  Transition to DEEP_ARCHIVE (save 90% on storage)
Day 365:  Object expires and is deleted (compliance requirement)
```

**Benefits**:
- **Cost Savings**: Up to 90% storage cost reduction
- **Automation**: No manual intervention
- **Compliance**: Guaranteed retention and deletion
- **Scalability**: Works for millions of objects

---

## Step 4: Prerequisites - AWS Account Setup

**Required Resources**:
1. **AWS Account**: Free tier available at aws.amazon.com
2. **IAM User**: With appropriate permissions
3. **Access Keys**: For programmatic access
4. **AWS CLI**: Command-line interface (optional but recommended)

**Steps to Create IAM User**:
1. Log into AWS Console
2. Navigate to IAM (Identity and Access Management)
3. Click "Users" → "Add user"
4. Username: `log-retention-admin`
5. Access type: Programmatic access ✓, AWS Console access ✓
6. Attach policies:
   - `AmazonS3FullAccess`
   - `CloudWatchFullAccess`
   - `IAMReadOnlyAccess`
7. Download credentials CSV
8. **IMPORTANT**: Store credentials securely!

**Security Best Practices**:
- Never commit credentials to version control
- Use IAM roles when possible
- Enable MFA (Multi-Factor Authentication)
- Rotate access keys regularly
- Follow principle of least privilege

---

## Step 5: Installing Required Tools

**Required Software**:

**1. Python 3.8+**
```bash
# Check Python version
python3 --version

# Install Python (if needed)
# macOS: brew install python3
# Ubuntu: sudo apt install python3 python3-pip
# Windows: Download from python.org
```

**2. Terraform**
```bash
# Check Terraform version
terraform version

# Install Terraform
# macOS: brew install terraform
# Ubuntu: wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
# Windows: Download from terraform.io
```

**3. AWS CLI**
```bash
# Install AWS CLI
# macOS: brew install awscli
# Ubuntu: sudo apt install awscli
# Windows: Download MSI installer from AWS

# Configure AWS CLI
aws configure
# Enter:
# - AWS Access Key ID
# - AWS Secret Access Key
# - Default region (e.g., us-east-1)
# - Default output format (json)
```

**4. Git**
```bash
# Check Git version
git --version

# Install Git
# macOS: brew install git
# Ubuntu: sudo apt install git
# Windows: Download from git-scm.com
```

---

## Step 6: Setting Up Your Development Environment

**1. Create Project Directory**:
```bash
mkdir -p ~/projects/s3-log-retention
cd ~/projects/s3-log-retention
```

**2. Clone Repository**:
```bash
git clone https://github.com/iotda-ol/DEA-C01-s3-log-retention-automation-using-lifecycle-policies-for-compliance.git
cd DEA-C01-s3-log-retention-automation-using-lifecycle-policies-for-compliance
```

**3. Set Up Python Environment**:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
cd python
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

**4. Verify Installation**:
```bash
# Test Python imports
python -c "import boto3; print('boto3:', boto3.__version__)"

# Test Terraform
terraform version

# Test AWS CLI
aws s3 ls
```

---

## Step 7: Understanding the Project Structure

**Directory Organization**:
```
DEA-C01-s3-log-retention-automation/
├── terraform/                    # Infrastructure as Code
│   ├── modules/                  # Reusable Terraform modules
│   │   ├── s3-bucket/           # S3 bucket creation
│   │   ├── lifecycle-policy/    # Lifecycle policy management
│   │   ├── iam/                 # IAM roles and policies
│   │   └── logging/             # CloudWatch/CloudTrail setup
│   ├── environments/            # Environment-specific configs
│   │   ├── dev/
│   │   ├── staging/
│   │   └── prod/
│   └── main.tf                  # Root configuration
├── python/                      # Python automation
│   ├── lib/                     # Core libraries (reusable)
│   │   ├── aws_client.py       # AWS client management
│   │   ├── s3_operations.py    # S3 operations
│   │   ├── lifecycle_policy.py # Policy templates
│   │   └── config_manager.py   # Configuration handling
│   ├── scripts/                 # Executable scripts
│   ├── validators/              # Compliance validation
│   ├── reporting/               # Report generation
│   └── monitoring/              # Monitoring tools
├── docs/                        # Documentation
│   └── manual/                  # This step-by-step guide
├── tests/                       # Automated tests
├── examples/                    # Usage examples
├── templates/                   # Configuration templates
└── scripts/                     # Utility scripts
```

**Key Design Principles**:
- **Modularity**: Reusable components
- **Separation of Concerns**: Each module has one responsibility
- **DRY (Don't Repeat Yourself)**: Shared code in libraries
- **Environment Isolation**: Dev/Staging/Prod separation
- **Infrastructure as Code**: Everything version controlled

---

## Step 8: Understanding AWS Credentials and Profiles

**AWS Credentials Hierarchy** (checked in this order):
1. Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)
2. AWS credentials file (`~/.aws/credentials`)
3. AWS config file (`~/.aws/config`)
4. IAM instance profile (for EC2 instances)
5. Container credentials (for ECS)

**Setting Up Multiple Profiles**:

**~/.aws/credentials**:
```ini
[default]
aws_access_key_id = YOUR_DEFAULT_KEY
aws_secret_access_key = YOUR_DEFAULT_SECRET

[log-retention-dev]
aws_access_key_id = YOUR_DEV_KEY
aws_secret_access_key = YOUR_DEV_SECRET

[log-retention-prod]
aws_access_key_id = YOUR_PROD_KEY
aws_secret_access_key = YOUR_PROD_SECRET
```

**~/.aws/config**:
```ini
[default]
region = us-east-1
output = json

[profile log-retention-dev]
region = us-east-1
output = json

[profile log-retention-prod]
region = us-west-2
output = json
```

**Using Profiles**:
```bash
# AWS CLI
aws s3 ls --profile log-retention-dev

# Python (boto3)
session = boto3.Session(profile_name='log-retention-dev')

# Terraform
export AWS_PROFILE=log-retention-dev
terraform plan
```

---

## Step 9: Basic AWS S3 Operations (Hands-On)

**Create Your First Bucket**:
```bash
# Set variables
BUCKET_NAME="my-first-log-bucket-$(date +%s)"
REGION="us-east-1"

# Create bucket
aws s3 mb s3://$BUCKET_NAME --region $REGION

# Verify creation
aws s3 ls | grep $BUCKET_NAME
```

**Upload a Test Log File**:
```bash
# Create test log file
echo "$(date): Test log entry" > test.log

# Upload to S3
aws s3 cp test.log s3://$BUCKET_NAME/logs/test.log

# List bucket contents
aws s3 ls s3://$BUCKET_NAME/logs/

# Download file
aws s3 cp s3://$BUCKET_NAME/logs/test.log downloaded.log

# Verify content
cat downloaded.log
```

**Enable Versioning**:
```bash
# Enable versioning
aws s3api put-bucket-versioning \
    --bucket $BUCKET_NAME \
    --versioning-configuration Status=Enabled

# Verify versioning
aws s3api get-bucket-versioning --bucket $BUCKET_NAME
```

**Clean Up**:
```bash
# Delete object
aws s3 rm s3://$BUCKET_NAME/logs/test.log

# Delete bucket
aws s3 rb s3://$BUCKET_NAME --force
```

---

## Step 10: Understanding Costs and Cost Optimization

**S3 Pricing Components**:
1. **Storage**: Per GB per month
2. **Requests**: Per 1,000 requests (PUT, GET, etc.)
3. **Data Transfer**: Outbound data transfer
4. **Management**: Inventory, analytics, object tags

**Storage Class Pricing** (approximate, us-east-1):
- **STANDARD**: $0.023 per GB/month
- **STANDARD_IA**: $0.0125 per GB/month (46% cheaper)
- **GLACIER**: $0.004 per GB/month (83% cheaper)
- **DEEP_ARCHIVE**: $0.00099 per GB/month (96% cheaper)

**Example Cost Calculation** (100 GB logs for 1 year):

**Without Lifecycle Policy** (all in STANDARD):
```
100 GB × $0.023/GB × 12 months = $276/year
```

**With DEA-C01 Lifecycle Policy**:
```
STANDARD (0-30 days):    100 GB × $0.023 × 1 month  = $2.30
STANDARD_IA (30-90 days): 100 GB × $0.0125 × 2 months = $2.50
GLACIER (90-180 days):   100 GB × $0.004 × 3 months  = $1.20
DEEP_ARCHIVE (180-365):  100 GB × $0.00099 × 6 months = $0.59
Total = $6.59/year (98% savings!)
```

**Cost Optimization Tips**:
1. Use lifecycle policies for automatic transitions
2. Delete old logs per compliance requirements
3. Enable compression for log files
4. Use appropriate storage classes
5. Monitor storage metrics with CloudWatch
6. Clean up incomplete multipart uploads
7. Use S3 Inventory for visibility

---

## Summary of Steps 1-10

**What You've Learned**:
✅ DEA-C01 compliance requirements
✅ S3 fundamentals and storage classes
✅ Lifecycle policies and their benefits
✅ AWS account and IAM setup
✅ Required tools installation
✅ Development environment configuration
✅ Project structure and organization
✅ AWS credentials and profiles
✅ Basic S3 operations
✅ Cost optimization strategies

**Next Steps** (Steps 11-20):
- AWS account configuration
- Setting up billing alerts
- IAM best practices
- VPC and networking basics
- CloudTrail setup for auditing

**Checklist Before Moving Forward**:
- [ ] AWS account created and verified
- [ ] IAM user with proper permissions created
- [ ] AWS CLI installed and configured
- [ ] Python 3.8+ installed
- [ ] Terraform installed
- [ ] Repository cloned
- [ ] Virtual environment set up
- [ ] Dependencies installed
- [ ] Can list S3 buckets with AWS CLI
- [ ] Understanding of cost implications
