# src/ui/cli.py
import argparse
import sys
from rich.console import Console
from rich.table import Table

class CLI:
    """Command-line interface for Tor IP Rotator"""
    
    def __init__(self):
        self.console = Console()
        self.parser = self._create_parser()
    
    def _create_parser(self):
        """Create command-line argument parser"""
        parser = argparse.ArgumentParser(description="Tor IP Rotator - Automatically change your IP address using Tor")
        parser.add_argument("--config", type=str, help="Path to configuration file")
        parser.add_argument("--interval", type=int, help="IP rotation interval in seconds")
        parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], help="Logging level")
        return parser
    
    def parse_args(self):
        """Parse command-line arguments"""
        return self.parser.parse_args()
    
    def display_ip(self, ip_address):
        """Display the current IP address"""
        self.console.print(f"[bold green]Current IP:[/bold green] {ip_address}")
    
    def display_rotating(self):
        """Display that the IP is being rotated"""
        self.console.print("[bold yellow]Rotating IP...[/bold yellow]")