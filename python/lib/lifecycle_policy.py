"""
Lifecycle Policy Manager
Reusable lifecycle policy operations and templates
"""

from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class LifecyclePolicyManager:
    """Manages S3 lifecycle policies with templates and validation"""

    @staticmethod
    def create_retention_rule(
        rule_id: str,
        expiration_days: int,
        prefix: str = "",
        enabled: bool = True,
        transitions: Optional[List[Dict]] = None,
    ) -> Dict:
        """
        Create a basic retention rule
        
        Args:
            rule_id: Unique rule identifier
            expiration_days: Days until object expiration
            prefix: Object key prefix filter
            enabled: Whether rule is enabled
            transitions: Optional list of storage class transitions
            
        Returns:
            Lifecycle rule dict
        """
        rule = {
            "ID": rule_id,
            "Status": "Enabled" if enabled else "Disabled",
            "Filter": {"Prefix": prefix},
            "Expiration": {"Days": expiration_days},
        }

        if transitions:
            rule["Transitions"] = transitions

        logger.debug(f"Created retention rule: {rule_id}")
        return rule

    @staticmethod
    def create_dea_c01_compliant_rule(prefix: str = "") -> Dict:
        """
        Create DEA-C01 compliant retention rule (1 year retention)
        
        Args:
            prefix: Object key prefix filter
            
        Returns:
            DEA-C01 compliant lifecycle rule
        """
        return LifecyclePolicyManager.create_retention_rule(
            rule_id="dea-c01-compliance",
            expiration_days=365,
            prefix=prefix,
            enabled=True,
            transitions=[
                {"Days": 30, "StorageClass": "STANDARD_IA"},
                {"Days": 90, "StorageClass": "GLACIER"},
                {"Days": 180, "StorageClass": "DEEP_ARCHIVE"},
            ],
        )

    @staticmethod
    def create_cost_optimized_rule(prefix: str = "") -> Dict:
        """
        Create cost-optimized lifecycle rule with aggressive transitions
        
        Args:
            prefix: Object key prefix filter
            
        Returns:
            Cost-optimized lifecycle rule
        """
        return {
            "ID": "cost-optimization",
            "Status": "Enabled",
            "Filter": {"Prefix": prefix},
            "Transitions": [
                {"Days": 7, "StorageClass": "STANDARD_IA"},
                {"Days": 30, "StorageClass": "GLACIER"},
                {"Days": 90, "StorageClass": "DEEP_ARCHIVE"},
            ],
            "Expiration": {"Days": 365},
            "NoncurrentVersionTransitions": [
                {"NoncurrentDays": 30, "StorageClass": "GLACIER"}
            ],
            "NoncurrentVersionExpiration": {"NoncurrentDays": 90},
            "AbortIncompleteMultipartUpload": {"DaysAfterInitiation": 7},
        }

    @staticmethod
    def create_immediate_delete_rule(
        prefix: str, days: int = 1, rule_id: str = "immediate-delete"
    ) -> Dict:
        """
        Create rule for immediate/fast deletion
        
        Args:
            prefix: Object key prefix filter
            days: Days until deletion (minimum 1)
            rule_id: Unique rule identifier
            
        Returns:
            Immediate deletion lifecycle rule
        """
        return {
            "ID": rule_id,
            "Status": "Enabled",
            "Filter": {"Prefix": prefix},
            "Expiration": {"Days": max(1, days)},
            "AbortIncompleteMultipartUpload": {"DaysAfterInitiation": 1},
        }

    @staticmethod
    def validate_rule(rule: Dict) -> tuple[bool, Optional[str]]:
        """
        Validate lifecycle rule structure
        
        Args:
            rule: Lifecycle rule dict
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        required_fields = ["ID", "Status", "Filter"]
        
        for field in required_fields:
            if field not in rule:
                return False, f"Missing required field: {field}"

        if rule["Status"] not in ["Enabled", "Disabled"]:
            return False, "Status must be 'Enabled' or 'Disabled'"

        # Must have at least one action
        actions = ["Expiration", "Transitions", "NoncurrentVersionExpiration", "NoncurrentVersionTransitions"]
        if not any(action in rule for action in actions):
            return False, "Rule must have at least one action (Expiration, Transitions, etc.)"

        # Validate transition order
        if "Transitions" in rule:
            days = [t["Days"] for t in rule["Transitions"]]
            if days != sorted(days):
                return False, "Transition days must be in ascending order"

        logger.debug(f"Validated rule: {rule['ID']}")
        return True, None

    @staticmethod
    def merge_rules(rules: List[Dict]) -> List[Dict]:
        """
        Merge and deduplicate lifecycle rules
        
        Args:
            rules: List of lifecycle rules
            
        Returns:
            Merged list of unique rules
        """
        seen_ids = set()
        merged = []
        
        for rule in rules:
            rule_id = rule.get("ID")
            if rule_id not in seen_ids:
                seen_ids.add(rule_id)
                merged.append(rule)
            else:
                logger.warning(f"Duplicate rule ID found: {rule_id}, skipping")
                
        logger.info(f"Merged {len(rules)} rules into {len(merged)} unique rules")
        return merged

    @staticmethod
    def get_template(template_name: str, **kwargs) -> Optional[Dict]:
        """
        Get lifecycle rule from template
        
        Args:
            template_name: Name of the template
            **kwargs: Template parameters
            
        Returns:
            Lifecycle rule dict or None
        """
        templates = {
            "dea-c01": LifecyclePolicyManager.create_dea_c01_compliant_rule,
            "cost-optimized": LifecyclePolicyManager.create_cost_optimized_rule,
            "immediate-delete": LifecyclePolicyManager.create_immediate_delete_rule,
        }
        
        template_func = templates.get(template_name)
        if template_func:
            return template_func(**kwargs)
        
        logger.error(f"Unknown template: {template_name}")
        return None
