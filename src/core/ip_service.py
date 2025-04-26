# src/core/ip_service.py
import requests

class IPService:
    """Service for detecting IP addresses"""
    
    def __init__(self, logger, config):
        self.logger = logger
        self.config = config
        self.proxy = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
        self.ip_apis = config.get("ip_apis", ["https://api.ipify.org?format=json"])
    
    def get_ip(self):
        """Get the current public IP address using the Tor network"""
        for api in self.ip_apis:
            try:
                response = requests.get(api, proxies=self.proxy, timeout=10)
                if response.status_code == 200:
                    if "json" in api:
                        return response.json()['ip']
                    else:
                        return response.text.strip()
            except Exception as e:
                self.logger.warning(f"Error with {api}: {str(e)}")
                continue
        
        return "[-] Unknown (check connection)"