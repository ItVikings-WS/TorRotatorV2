# Developed by Mostafa Amed @itvikings 
# under the guidance of Sr- Ahmed Samy 
import os
import sys
import time
import platform as platform_module

from src.utils.config import Config
from src.utils.logger import Logger
from src.core.ip_service import IPService
from src.core.tor_controller import TorController
from src.ui.cli import CLI

def get_platform(logger):
    """Get the appropriate platform implementation"""
    system = platform_module.system().lower()
    
    if system == "linux":
        from src.platform.linux import LinuxPlatform
        return LinuxPlatform(logger)
    elif system == "windows":
        from src.platform.windows import WindowsPlatform
        return WindowsPlatform(logger)
    elif system == "darwin":  # macOS
        from src.platform.macos import MacOSPlatform
        return MacOSPlatform(logger)
    else:
        logger.error(f"Unsupported platform: {system}")
        sys.exit(1)

def main():
    # Parse command-line arguments
    cli = CLI()
    args = cli.parse_args()
    
    # Load configuration
    config_file = args.config or os.path.join("config", "default.yaml")
    config = Config(config_file)
    
    # Override config with command-line arguments
    if args.interval:
        config.set("refresh_interval", args.interval)
    if args.log_level:
        config.set("log_level", args.log_level)
    
    # Initialize logger
    logger = Logger(config)
    logger.info("Starting Tor IP Rotator")
    
    try:
        # Get platform-specific implementation
        platform = get_platform(logger)
        
        # Initialize services
        ip_service = IPService(logger, config)
        tor_controller = TorController(platform, ip_service, logger, config)
        
        # Set up Tor
        tor_controller.setup()
        
        # Run the IP rotation loop
        tor_controller.run_rotation_loop(callback=cli.display_ip)
    except Exception as e:
        logger.error(f"Unhandled exception: {str(e)}")
        sys.exit(1)

## check with curl ------> curl  --socks5 127.0.0.1:9050 'https://api.ipify.org?format=json'
if __name__ == "__main__":

    print('[+] Started Proxy-Server at 127.0.0.1:9050 ')
    main()