# src/platform/linux.py
import shutil
import subprocess
import time
from .base import TorPlatform

class LinuxPlatform(TorPlatform):
    """Linux-specific implementation of Tor operations"""
    
    def __init__(self, logger):
        self.logger = logger
    
    def is_tor_installed(self):
        """Check if Tor is installed on the system"""
        return shutil.which("tor") is not None
    
    def install_tor(self):
        """Install Tor using apt"""
        self.logger.info("Installing Tor...")
        subprocess.run(["sudo", "apt", "update"], check=True )
        subprocess.run(["sudo", "apt", "install", "-y", "tor"], check=True)
        self.logger.info("Tor installed successfully")
    
    def is_tor_running(self):
        """Check if Tor service is active"""
        result = subprocess.run(["systemctl", "is-active", "--quiet", "tor"])
        return result.returncode == 0
    
    def start_tor_service(self):
        """Start the Tor service"""
        self.logger.info("Starting Tor service...")
        subprocess.run(["sudo", "systemctl", "start", "tor"], check=True)
        time.sleep(5)  # Give Tor some time to initialize
        self.logger.info("Tor service started")
        
    def stop_tor_service(self):
        """Stop the Tor service"""
        self.logger.info("Stopping Tor service...")
        subprocess.run(["sudo", "systemctl", "stop", "tor"], check=True)
        self.logger.info("Tor service stopped")