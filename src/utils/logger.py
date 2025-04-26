# src/utils/logger.py
import logging
import sys
import os
from datetime import datetime

class Logger:
    """Handles application logging"""
    
    def __init__(self, config):
        self.config = config
        log_level = getattr(logging, config.get("log_level", "INFO").upper())
        log_dir = config.get("log_directory", "logs")
        
        # Create log directory if it doesn't exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        # Set up file handler
        log_file = os.path.join(log_dir, f"tor_rotator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        
        # Configure logger
        self.logger = logging.getLogger("tor_rotator")
        self.logger.setLevel(log_level)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_format)
        
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_format)
        
        # Add handlers
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def info(self, message):
        self.logger.info(message)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def error(self, message):
        self.logger.error(message)
    
    def debug(self, message):
        self.logger.debug(message)