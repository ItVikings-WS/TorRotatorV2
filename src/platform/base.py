# src/platform/base.py
from abc import ABC, abstractmethod

class TorPlatform(ABC):
    """Base class for platform-specific Tor operations"""
    
    # @abstractmethod
    # def is_tor_installed(self):
    #     """Check if Tor is installed on the system"""
    #     pass
    
    # @abstractmethod
    # def install_tor(self):
    #     """Install Tor on the system"""
    #     pass
    
    @abstractmethod
    def is_tor_running(self):
        """Check if Tor service is running"""
        pass
    
    @abstractmethod
    def start_tor_service(self):
        """Start the Tor service"""
        pass
    
    @abstractmethod
    def stop_tor_service(self):
        """Stop the Tor service"""
        pass