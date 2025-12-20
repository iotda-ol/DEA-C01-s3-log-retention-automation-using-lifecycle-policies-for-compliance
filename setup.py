"""Setup configuration for S3 Log Retention Automation."""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="s3-log-retention",
    version="1.0.0",
    author="DEA-C01 Team",
    author_email="team@example.com",
    description="Automated S3 log retention using lifecycle policies for compliance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iotda-ol/DEA-C01-s3-log-retention-automation-using-lifecycle-policies-for-compliance",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: System :: Logging",
        "Topic :: System :: Archiving",
    ],
    python_requires=">=3.9",
    install_requires=[
        "boto3>=1.34.0",
        "click>=8.1.7",
        "pyyaml>=6.0.1",
        "python-dotenv>=1.0.0",
        "pydantic>=2.5.0",
        "structlog>=23.2.0",
        "python-dateutil>=2.8.2",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.12.0",
            "moto>=4.2.0",
            "black>=23.12.0",
            "pylint>=3.0.0",
            "mypy>=1.7.0",
            "isort>=5.13.0",
        ],
        "async": [
            "aioboto3>=12.3.0",
            "aiofiles>=23.2.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "s3-log-retention=cli.main:cli",
        ],
    },
)
