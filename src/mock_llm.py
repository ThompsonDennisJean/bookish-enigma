"""
Mock LLM Implementation - Provides deterministic responses for testing
Copyright (c) 2025 IT Helpdesk Auto-Responder Contributors
MIT License - See LICENSE file
"""

import re
from typing import Dict, Optional

class MockLLM:
    """
    Mock LLM that returns pre-defined responses for common IT issues.
    Includes category, diagnostic command, and suggested fix.
    """
    
    def __init__(self):
        self.templates = {
            # Network connectivity issues
            "network": {
                "triggers": ["can't connect", "no internet", "wifi", "network", "slow connection"],
                "responses": [{
                    "first_turn": """
Category: Network Connectivity
COMMAND: ping -c 4 google.com
Likely cause: Network connectivity or DNS issues""",
                    "second_turn": {
                        "success": """
Diagnosis: Network appears to be functioning normally with good response times
Fix: Issue may be application-specific. Try clearing browser cache and cookies.""",
                        "failure": """
Diagnosis: Network connectivity issue detected - high packet loss or no response
Fix: 1. Check Wi-Fi is enabled and connected
2. Restart router/modem
3. Contact ISP if issue persists"""
                    }
                }]
            },
            
            # Printer issues
            "printer": {
                "triggers": ["printer", "won't print", "print error", "printing"],
                "responses": [{
                    "first_turn": """
Category: Printing System
COMMAND: lpstat -p
Likely cause: Printer queue or driver issues""",
                    "second_turn": {
                        "success": """
Diagnosis: Printer is online and ready but may have queued jobs
Fix: 1. Clear print queue
2. Send test page
3. Check paper tray""",
                        "failure": """
Diagnosis: Printer appears offline or in error state
Fix: 1. Check printer power and network cable
2. Restart printer
3. Reinstall printer driver"""
                    }
                }]
            },
            
            # System performance
            "performance": {
                "triggers": ["slow", "sluggish", "freezing", "not responding"],
                "responses": [{
                    "first_turn": """
Category: System Performance
COMMAND: systeminfo
Likely cause: Resource constraints or system issues""",
                    "second_turn": {
                        "success": """
Diagnosis: System resources appear normal
Fix: 1. Close unused applications
2. Clear temporary files
3. Run disk cleanup""",
                        "failure": """
Diagnosis: Potential system resource issues detected
Fix: 1. Restart computer
2. Check for malware
3. Consider memory upgrade"""
                    }
                }]
            }
        }
    
    def query(self, prompt: str) -> str:
        """
        Return a deterministic response based on issue keywords.
        Always includes COMMAND: line in first turn.
        """
        # Check if this is a second-turn prompt
        is_second_turn = "output:" in prompt.lower() or "command output" in prompt.lower()
        
        if is_second_turn:
            return self._generate_second_turn(prompt)
        
        return self._generate_first_turn(prompt)
    
    def _generate_first_turn(self, prompt: str) -> str:
        """Generate initial analysis with diagnostic command."""
        # Default response if no matches
        default_response = """
Category: General Issue
COMMAND: systeminfo
Likely cause: Unknown - gathering system information"""
        
        # Find matching category based on keywords
        prompt_lower = prompt.lower()
        for category, template in self.templates.items():
            if any(trigger in prompt_lower for trigger in template["triggers"]):
                return template["responses"][0]["first_turn"].strip()
        
        return default_response.strip()
    
    def _generate_second_turn(self, prompt: str) -> str:
        """Generate final diagnosis based on command output."""
        # Determine success/failure from command output
        has_error = any(err in prompt.lower() for err in 
            ["error", "failure", "timeout", "not found", "offline"])
        
        # Find matching category
        prompt_lower = prompt.lower()
        for category, template in self.templates.items():
            if any(trigger in prompt_lower for trigger in template["triggers"]):
                response = template["responses"][0]["second_turn"]
                return (response["failure" if has_error else "success"]).strip()
        
        # Default response
        return """
Diagnosis: Unable to determine specific issue
Fix: Please contact IT support for further assistance""".strip()