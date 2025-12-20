from setuptools import setup, find_packages

setup(
    name="s3-log-retention",
    version="1.0.0",
    description="S3 Log Retention Automation for DEA-C01 Compliance",
    author="Platform Engineering",
    packages=find_packages(),
    install_requires=[
        "boto3>=1.34.0",
        "click>=8.1.7",
        "pyyaml>=6.0",
        "python-dateutil>=2.8.2",
        "tabulate>=0.9.0",
    ],
    entry_points={
        "console_scripts": [
            "s3-log-manager=scripts.manage_logs:cli",
            "s3-compliance-check=scripts.compliance_check:cli",
            "s3-lifecycle-apply=scripts.apply_lifecycle:cli",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
