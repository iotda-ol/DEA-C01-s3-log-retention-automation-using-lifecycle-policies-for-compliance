# Development Environment Setup

This guide walks you through setting up your development environment for S3 log retention automation.

## Prerequisites

### Operating System

The project works on:
- macOS 10.15+
- Ubuntu 20.04+
- Windows 10+ (with WSL2 recommended)

### Required Software

1. **AWS CLI** (version 2.x)
2. **Terraform** (version 1.0+)
3. **Python** (version 3.9+)
4. **Git** (version 2.x)

## Installation Steps

### 1. Install AWS CLI

**macOS:**
```bash
brew install awscli
```

**Linux:**
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

**Windows:**
Download from: https://aws.amazon.com/cli/

Verify installation:
```bash
aws --version
```

### 2. Install Terraform

**macOS:**
```bash
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
```

**Linux:**
```bash
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform
```

**Windows:**
Download from: https://www.terraform.io/downloads

Verify installation:
```bash
terraform --version
```

### 3. Install Python

**macOS:**
```bash
brew install python@3.11
```

**Linux:**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

**Windows:**
Download from: https://www.python.org/downloads/

Verify installation:
```bash
python3 --version
pip3 --version
```

### 4. Install Git

**macOS:**
```bash
brew install git
```

**Linux:**
```bash
sudo apt install git
```

**Windows:**
Download from: https://git-scm.com/download/win

Verify installation:
```bash
git --version
```

## Project Setup

### 1. Clone Repository

```bash
git clone https://github.com/iotda-ol/DEA-C01-s3-log-retention-automation-using-lifecycle-policies-for-compliance.git
cd DEA-C01-s3-log-retention-automation-using-lifecycle-policies-for-compliance
```

### 2. Create Python Virtual Environment

```bash
python3 -m venv venv
```

Activate the environment:

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```powershell
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Install the Package

```bash
pip install -e .
```

### 5. Configure AWS Credentials

```bash
aws configure
```

Enter your:
- AWS Access Key ID
- AWS Secret Access Key
- Default region (e.g., us-east-1)
- Default output format (json)

## IDE Setup

### Visual Studio Code

Recommended extensions:
- Python (Microsoft)
- Pylance
- HashiCorp Terraform
- YAML
- GitLens

Settings (`.vscode/settings.json`):
```json
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "python.testing.pytestEnabled": true,
  "terraform.format.enable": true
}
```

### PyCharm

1. Open project directory
2. Configure Python interpreter to use `venv`
3. Enable Terraform plugin
4. Set pytest as test runner

## Verify Setup

Run all verification checks:

```bash
# Check Python
python --version

# Check AWS CLI
aws --version

# Check Terraform
terraform --version

# Check project installation
s3-log-retention --help

# Run tests
pytest tests/unit/ -v
```

## Common Issues

### Python not found

Make sure Python is in your PATH. On Windows, check "Add Python to PATH" during installation.

### AWS credentials not configured

Run `aws configure` and ensure credentials are valid:
```bash
aws sts get-caller-identity
```

### Terraform provider download issues

Check internet connection and proxy settings:
```bash
export HTTP_PROXY=http://proxy:port
export HTTPS_PROXY=http://proxy:port
```

### Virtual environment issues

Delete and recreate:
```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Next Steps

1. Read [Step-by-Step Guide](../STEP_BY_STEP_GUIDE.md)
2. Review [Architecture Overview](../architecture/overview.md)
3. Try [Basic Examples](../../examples/basic/)
4. Deploy [Development Environment](../../terraform/environments/dev.tfvars)
