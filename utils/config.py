"""
Configuration Management
"""

import yaml
import json
from typing import Dict, Any
import os


class ConfigManager:
    """Manages configuration settings"""
    
    def __init__(self, config_file: str = 'config/config.yaml'):
        self.config_file = config_file
        self.config = {}
        self.load_config()
    
    def load_config(self):
        """Load configuration from YAML file"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = yaml.safe_load(f)
        else:
            print(f"Config file {self.config_file} not found")
            self.config = self._get_default_config()
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        
        return value if value is not None else default
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            yaml.dump(self.config, f)
    
    def get_allocation_config(self) -> Dict[str, float]:
        """Get capital allocation configuration"""
        return self.get('capital_allocation', {})
    
    def get_roi_config(self) -> Dict[str, float]:
        """Get ROI configuration"""
        return self.get('daily_roi', {})
    
    def get_cloning_config(self) -> Dict:
        """Get cloning configuration"""
        return self.get('cloning', {})
    
    def _get_default_config(self) -> Dict:
        """Get default configuration"""
        return {
            'trader': {
                'initial_capital': 10.0,
                'name': 'MainAI_v1',
                'risk_level': 'medium'
            },
            'capital_allocation': {
                'crypto_trading': 0.30,
                'stock_trading': 0.10,
                'dropshipping': 0.15,
                'content_creation': 0.12,
                'digital_products': 0.12,
                'affiliate_marketing': 0.08,
                'freelancing': 0.08,
                'gig_tasks': 0.05
            },
            'simulation': {
                'enabled': True,
                'days': 30
            }
        }
