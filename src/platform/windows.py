# src/platform/windows.py
import subprocess
import time
import os
import shutil
import zipfile
import requests
import tarfile
from .base import TorPlatform

class WindowsPlatform(TorPlatform):
    """Windows-specific implementation of Tor operations"""
    
    def __init__(self, logger):
        self.logger = logger
        self.current_dir = os.getcwd()
        self.tor_path = os.path.join(self.current_dir , "executables" , "windows", "tor")
        self.tor_exe = os.path.join(self.tor_path, "tor.exe")
        self.tor_process = None
    
    # def is_tor_installed(self):
    #     """Check if Tor is installed on the system"""
    #     return os.path.exists(self.tor_exe)
    
    # def install_tor(self):
    #     """Download and install Tor for Windows"""
    #     self.logger.info("[+] Installing Tor for Windows...")
        
    #     # Create installation directory
    #     os.makedirs(self.tor_path, exist_ok=True)
        
    #     # Download Tor Expert Bundle
    #     tor_url = "https://archive.torproject.org/tor-package-archive/torbrowser/14.5/tor-expert-bundle-windows-x86_64-14.5.tar.gz"
    #     zip_path = os.path.join(self.tor_path, "tor.tar.gz")
        
    #     self.logger.info(f"Downloading Tor from {tor_url}")
    #     response = requests.get(tor_url, stream=True)
    #     with open(zip_path, 'wb') as f:
    #         for chunk in response.iter_content(chunk_size=8192):
    #             f.write(chunk)
        
    #     # Extract Tor
    #     self.logger.info("Extracting Tor...")

    # WHY ALL OF THISS ???? 
    # JUST Download the files in a separate folder and run it !! 
            
    #     tor_file = tarfile.open(zip_path)
    #     tor_file.extractall(self.tor_path)
    #     self.logger.info("Extracted Tor_expert_bundle to --> {}".format(self.tor_path))
    #     # Clean up
    #     os.remove(self.zip_path)
    #     self.logger.info("Tor installed successfully")
    
    def is_tor_running(self):
        """Check if Tor process is running"""
        if self.tor_process:
            return self.tor_process.poll() is None
        return False
    

    def start_tor_service(self):
        """Start Tor as a subprocess"""
        if self.is_tor_running():
            return
            
        self.logger.info("[+] Starting Tor service...")
        torrc_path = os.path.join(self.tor_path, "torrc")
        
        # Create a basic torrc file if it doesn't exist
        if not os.path.exists(torrc_path):
            
            with open(torrc_path, 'w') as f:
                print(f"torrc path {torrc_path}")
                f.write("SocksPort 9050\n")
                f.write("ControlPort 9051\n")
                f.write("CookieAuthentication 1\n")
        
        # Start Tor
        self.tor_process = subprocess.Popen(
            [self.tor_exe, "-f", torrc_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        time.sleep(5)  # Give Tor time to start
        
        if self.is_tor_running():
            self.logger.info("Tor service started")
        else:
            self.logger.error("Failed to start Tor")
    
    def stop_tor_service(self):
        """Stop the Tor process"""
        if self.tor_process:
            self.logger.info("Stopping Tor service...")
            self.tor_process.terminate()
            self.tor_process.wait(timeout=10)
            self.tor_process = None
            self.logger.info("Tor service stopped")
            