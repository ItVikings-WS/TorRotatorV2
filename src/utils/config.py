# src/utils/config.py
import os
import yaml

class Config:
    """Configuration manager for the application"""
    
    def __init__(self, config_file=None):
        self.config = {
            "tor_proxy_port": 9050,
            "tor_control_port": 9051,
            "refresh_interval": 10,
            "log_level": "INFO",
            "log_directory": "logs",
            "ip_apis": [
               # "https://api.ipify.org?format=json",
                "https://api.myip.com"
               
            ]
        }
        
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r') as f:
                user_config = yaml.safe_load(f)
                if user_config:
                    self.config.update(user_config)
    
    def get(self, key, default=None):
        """Get a configuration value"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Set a configuration value"""
        self.config[key] = value