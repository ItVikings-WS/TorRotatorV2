# src/core/tor_controller.py
import time
from stem import Signal
from stem.control import Controller

class TorController:
    """Core functionality for controlling Tor circuits"""
    
    def __init__(self, platform, ip_service, logger, config):
        self.platform = platform
        self.ip_service = ip_service
        self.logger = logger
        self.config = config
        self.control_port = config.get("tor_control_port", 9051)
        self.refresh_interval = config.get("refresh_interval", 10)
    
    def setup(self):
        """Set up Tor if necessary"""
        # if not self.platform.is_tor_installed():
        #     self.platform.install_tor()
        
        if not self.platform.is_tor_running():
            self.platform.start_tor_service()
            
        self.logger.info("Tor setup complete and running")
    
    def get_current_ip(self):
        """Get the current public IP address"""
        return self.ip_service.get_ip()
    
    def renew_ip(self):
        """Request a new Tor circuit and IP address"""
        try:
            with Controller.from_port(port=self.control_port) as controller:
                controller.authenticate()
                controller.signal(Signal.NEWNYM)
                self.logger.info("[+] New Tor circuit created")
                # Wait a moment for the circuit to be created
                time.sleep(5)
            return True
        except Exception as e:
            self.logger.error(f"Failed to rotate IP: {str(e)}")
            return False
    
    def run_rotation_loop(self, callback=None):
        """Run the IP rotation loop"""
        self.logger.info("Starting IP rotation loop")
        
        try:
            while True:
                current_ip = self.get_current_ip()
                self.logger.info(f"Current IP: {current_ip}")
                
                if callback:
                    callback(current_ip)
                
                self.logger.info(f"Sleeping for {self.refresh_interval} seconds...")
                time.sleep(self.refresh_interval)
                
                self.logger.info("Rotating IP...")
                self.renew_ip()
        except KeyboardInterrupt:
            self.logger.info("IP rotation stopped by user")