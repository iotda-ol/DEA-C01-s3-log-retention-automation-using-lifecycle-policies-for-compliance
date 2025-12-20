"""
Configuration Manager
Handles configuration loading and validation
"""

import yaml
import json
import os
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class ConfigManager:
    """Manages configuration from files and environment variables"""

    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration manager
        
        Args:
            config_file: Path to configuration file (YAML or JSON)
        """
        self.config = {}
        if config_file:
            self.load_from_file(config_file)
        self.load_from_env()

    def load_from_file(self, file_path: str) -> None:
        """
        Load configuration from file
        
        Args:
            file_path: Path to configuration file
        """
        if not os.path.exists(file_path):
            logger.warning(f"Configuration file not found: {file_path}")
            return

        try:
            with open(file_path, "r") as f:
                if file_path.endswith((".yaml", ".yml")):
                    self.config = yaml.safe_load(f)
                elif file_path.endswith(".json"):
                    self.config = json.load(f)
                else:
                    logger.error(f"Unsupported file format: {file_path}")
                    return
                    
            logger.info(f"Loaded configuration from {file_path}")
        except Exception as e:
            logger.error(f"Failed to load configuration from {file_path}: {e}")

    def load_from_env(self) -> None:
        """Load configuration from environment variables"""
        env_mappings = {
            "AWS_REGION": "aws.region",
            "AWS_PROFILE": "aws.profile",
            "LOG_BUCKET_NAME": "s3.bucket_name",
            "LOG_RETENTION_DAYS": "s3.retention_days",
            "ALERT_EMAIL": "notifications.email",
        }

        for env_var, config_key in env_mappings.items():
            value = os.getenv(env_var)
            if value:
                self.set_nested(config_key, value)
                logger.debug(f"Loaded {env_var} from environment")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value
        
        Args:
            key: Configuration key (supports nested keys with dots)
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split(".")
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
                
        return value if value is not None else default

    def set_nested(self, key: str, value: Any) -> None:
        """
        Set nested configuration value
        
        Args:
            key: Configuration key (supports nested keys with dots)
            value: Configuration value
        """
        keys = key.split(".")
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
            
        config[keys[-1]] = value

    def get_aws_config(self) -> Dict[str, Any]:
        """Get AWS-specific configuration"""
        return {
            "region": self.get("aws.region", "us-east-1"),
            "profile": self.get("aws.profile"),
        }

    def get_s3_config(self) -> Dict[str, Any]:
        """Get S3-specific configuration"""
        return {
            "bucket_name": self.get("s3.bucket_name"),
            "retention_days": int(self.get("s3.retention_days", 365)),
            "enable_versioning": self.get("s3.enable_versioning", True),
            "storage_class_transitions": self.get("s3.transitions", []),
        }

    def get_notification_config(self) -> Dict[str, Any]:
        """Get notification configuration"""
        return {
            "email": self.get("notifications.email"),
            "sns_topic_arn": self.get("notifications.sns_topic_arn"),
            "enable_alerts": self.get("notifications.enable_alerts", True),
        }

    def validate(self) -> tuple[bool, list[str]]:
        """
        Validate configuration
        
        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []
        
        # Validate required fields
        required_fields = [
            "aws.region",
            "s3.bucket_name",
        ]
        
        for field in required_fields:
            if not self.get(field):
                errors.append(f"Missing required field: {field}")

        # Validate retention days
        retention_days = self.get("s3.retention_days")
        if retention_days and not isinstance(retention_days, int):
            errors.append("s3.retention_days must be an integer")

        is_valid = len(errors) == 0
        if is_valid:
            logger.info("Configuration validation passed")
        else:
            logger.error(f"Configuration validation failed: {errors}")
            
        return is_valid, errors

    def to_dict(self) -> Dict[str, Any]:
        """Return configuration as dictionary"""
        return self.config.copy()

    def save_to_file(self, file_path: str) -> bool:
        """
        Save configuration to file
        
        Args:
            file_path: Path to save configuration
            
        Returns:
            True if successful
        """
        try:
            with open(file_path, "w") as f:
                if file_path.endswith((".yaml", ".yml")):
                    yaml.dump(self.config, f, default_flow_style=False)
                elif file_path.endswith(".json"):
                    json.dump(self.config, f, indent=2)
                else:
                    logger.error(f"Unsupported file format: {file_path}")
                    return False
                    
            logger.info(f"Saved configuration to {file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save configuration to {file_path}: {e}")
            return False
