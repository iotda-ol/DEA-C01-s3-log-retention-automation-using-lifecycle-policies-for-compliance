# AWS Account Setup Guide

## Prerequisites

Before you begin, you'll need:
- A valid email address
- A credit card (for AWS billing)
- A phone number (for verification)

## Step 1: Create AWS Account

1. Go to [aws.amazon.com](https://aws.amazon.com)
2. Click "Create an AWS Account"
3. Enter your email and account name
4. Follow the registration process
5. Verify your email address

## Step 2: Secure Your Root Account

### Enable Multi-Factor Authentication (MFA)

1. Sign in to AWS Console
2. Click on your account name → Security Credentials
3. Scroll to "Multi-factor authentication (MFA)"
4. Click "Activate MFA"
5. Choose "Virtual MFA device"
6. Scan the QR code with Google Authenticator or similar app
7. Enter two consecutive MFA codes
8. Click "Assign MFA"

**Why MFA?** Protects your account even if password is compromised.

## Step 3: Create IAM Admin User

**Never use root account for daily tasks!**

1. Navigate to IAM Console
2. Click "Users" → "Add user"
3. Set username (e.g., `admin`)
4. Check "Programmatic access" and "AWS Management Console access"
5. Set a strong password
6. Click "Next: Permissions"
7. Click "Attach existing policies directly"
8. Select "AdministratorAccess"
9. Click "Next: Tags" → "Next: Review" → "Create user"
10. **Save** the Access Key ID and Secret Access Key

## Step 4: Enable MFA for IAM User

Repeat MFA setup process for your IAM admin user.

## Step 5: Configure AWS Billing Alerts

1. Go to Billing Dashboard
2. Click "Budgets"
3. Click "Create budget"
4. Select "Cost budget"
5. Set budget amount (e.g., $10)
6. Configure email alerts at 80% and 100%
7. Create budget

## Step 6: Verify Account Limits

Check your account limits:
```bash
aws service-quotas list-service-quotas \
  --service-code s3 \
  --query 'Quotas[*].[QuotaName,Value]'
```

## Step 7: Set Up AWS CLI Profiles

Create a named profile for easier management:

```bash
# Configure default profile
aws configure --profile dev

# Set environment variable to use profile
export AWS_PROFILE=dev
```

## Security Checklist

- [ ] Root account MFA enabled
- [ ] IAM admin user created
- [ ] IAM user MFA enabled
- [ ] Access keys saved securely
- [ ] Billing alerts configured
- [ ] Password policy configured
- [ ] CloudTrail enabled
- [ ] AWS Config enabled (optional)

## Common Issues

### Issue: Can't receive verification code
**Solution**: Check spam folder, ensure phone number is correct

### Issue: Credit card not accepted
**Solution**: Try a different card, contact AWS support

### Issue: Account under review
**Solution**: Wait 24 hours, check email for updates

## Next Steps

- Configure AWS CLI on your local machine
- Create your first S3 bucket
- Review IAM best practices
- Move to [03-python-setup.md](03-python-setup.md)
