"""
Diagnostics Executor - Safely runs whitelisted system commands
Copyright (c) 2025 IT Helpdesk Auto-Responder Contributors
MIT License - See LICENSE file
"""

import os
import time
import subprocess
import platform
from typing import Dict, List, Union
import shlex

# Whitelist of allowed diagnostic commands
# SECURITY: Only add commands that are safe for automated execution
ALLOWED_COMMANDS = {
    # Network diagnostics - basic connectivity
    "ping": ["ping", "ping -c 4", "ping -n 4"],
    "traceroute": ["traceroute", "tracert"],
    
    # Network configuration
    "ipconfig": ["ipconfig /all"],
    "ifconfig": ["ifconfig -a"],
    "netstat": ["netstat -an"],
    
    # System info
    "systeminfo": ["systeminfo"],
    "hostname": ["hostname"],
    
    # Printer diagnostics
    "lpstat": ["lpstat -p", "lpstat -v"],
    
    # Process info (no kill commands)
    "ps": ["ps aux", "ps -ef"],
    "top": ["top -n 1", "top -b -n 1"],
}

# Platform-specific command simulations
SIMULATED_OUTPUT = {
    "ping -c 4 google.com": """
PING google.com (142.250.190.78) 56(84) bytes of data.
64 bytes from lax31s07-in-f14.1e100.net (142.250.190.78): icmp_seq=1 ttl=56 time=31.2 ms
64 bytes from lax31s07-in-f14.1e100.net (142.250.190.78): icmp_seq=2 ttl=56 time=30.8 ms
64 bytes from lax31s07-in-f14.1e100.net (142.250.190.78): icmp_seq=3 ttl=56 time=30.9 ms
64 bytes from lax31s07-in-f14.1e100.net (142.250.190.78): icmp_seq=4 ttl=56 time=31.0 ms

--- google.com ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3004ms
rtt min/avg/max/mdev = 30.827/30.992/31.236/0.151 ms
""",
    "lpstat -p": """
printer HP_LaserJet_M402n is idle. enabled since Tue Oct 22 09:00:00 2025
""",
    "systeminfo": """
Host Name:                 DESKTOP-ABC123
OS Name:                   Microsoft Windows 10 Pro
OS Version:               10.0.19045 N/A Build 19045
System Type:               x64-based PC
Processor(s):             1 Processor(s) Installed, Intel64 Family 6
Memory:                   16,384 MB RAM
""",
}

class DiagnosticsExecutor:
    """Safely executes whitelisted system diagnostic commands."""
    
    def __init__(self):
        self.force_simulation = os.getenv("FORCE_SIMULATION", "").lower() == "true"
        self.is_codespace = os.getenv("CODESPACES", "").lower() == "true"
    
    def is_allowed(self, command: str) -> bool:
        """
        Check if a command is in the whitelist.
        SECURITY: Strict matching against pre-approved commands only.
        """
        cmd_parts = shlex.split(command)
        base_cmd = cmd_parts[0]
        
        if base_cmd not in ALLOWED_COMMANDS:
            return False
            
        # Check if exact command (with args) is allowed
        return command in ALLOWED_COMMANDS[base_cmd]
    
    async def run_command(self, command: str, timeout: int = 10) -> Dict[str, str]:
        """
        Execute a whitelisted command or return simulated output.
        
        Args:
            command: The command to execute
            timeout: Maximum execution time in seconds
            
        Returns:
            Dict with cmd, stdout, stderr, returncode, and runtime_ms
        """
        if not self.is_allowed(command):
            raise ValueError(f"Command not allowed: {command}")
            
        # Use simulation if forced or in Codespace
        if self.force_simulation or self.is_codespace:
            return await self.simulate_command(command)
            
        try:
            start_time = time.time()
            
            # SECURITY: Use shlex.split to properly handle command arguments
            result = subprocess.run(
                shlex.split(command),
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False  # Don't raise on non-zero exit
            )
            
            runtime_ms = int((time.time() - start_time) * 1000)
            
            return {
                "cmd": command,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "runtime_ms": runtime_ms
            }
            
        except subprocess.TimeoutExpired:
            return {
                "cmd": command,
                "stdout": "",
                "stderr": f"Command timed out after {timeout} seconds",
                "returncode": -1,
                "runtime_ms": timeout * 1000
            }
    
    async def simulate_command(self, command: str) -> Dict[str, str]:
        """
        Return pre-defined simulation output for demo/test commands.
        """
        # Return pre-defined output if available
        if command in SIMULATED_OUTPUT:
            return {
                "cmd": command,
                "stdout": SIMULATED_OUTPUT[command],
                "stderr": "",
                "returncode": 0,
                "runtime_ms": 100  # Simulated runtime
            }
            
        # Generic simulation based on command type
        if command.startswith("ping"):
            return {
                "cmd": command,
                "stdout": "Simulated ping: 4 packets transmitted, 4 received, 0% packet loss",
                "stderr": "",
                "returncode": 0,
                "runtime_ms": 100
            }
            
        if "systeminfo" in command or "hostname" in command:
            return {
                "cmd": command,
                "stdout": f"Simulated {command} on {platform.system()} {platform.release()}",
                "stderr": "",
                "returncode": 0,
                "runtime_ms": 100
            }
            
        # Generic fallback
        return {
            "cmd": command,
            "stdout": f"Simulated output for: {command}",
            "stderr": "",
            "returncode": 0,
            "runtime_ms": 100
        }