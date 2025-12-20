"""
Setup configuration for S3 Log Retention Automation
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="s3-log-retention",
    version="1.0.0",
    author="S3 Log Retention Team",
    author_email="",
    description="Automated S3 log retention with lifecycle policies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iotda-ol/DEA-C01-s3-log-retention-automation-using-lifecycle-policies-for-compliance",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Logging",
        "Topic :: System :: Archiving",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "boto3>=1.34.0",
        "botocore>=1.34.0",
        "click>=8.1.0",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0.1",
        "python-dateutil>=2.8.2",
        "colorlog>=6.8.0",
        "tenacity>=8.2.3",
        "tabulate>=0.9.0",
        "tqdm>=4.66.0",
        "jsonschema>=4.20.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.12.0",
            "moto>=4.2.0",
            "black>=23.12.0",
            "flake8>=6.1.0",
            "pylint>=3.0.0",
            "mypy>=1.7.0",
            "types-PyYAML>=6.0.12",
            "types-python-dateutil>=2.8.19",
        ],
        "async": [
            "aioboto3>=12.3.0",
            "aiofiles>=23.2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "s3-log-retention=cli.main:cli",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
