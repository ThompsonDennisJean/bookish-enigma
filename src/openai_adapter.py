"""
OpenAI Integration (Optional) - Requires API Key
Copyright (c) 2025 IT Helpdesk Auto-Responder Contributors
MIT License - See LICENSE file
"""

import os
from typing import Dict, Optional
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class OpenAIAdapter:
    """
    OpenAI API integration for IT diagnostics.
    Requires OPENAI_API_KEY environment variable.
    
    TODO: Uncomment and configure to enable OpenAI integration
    """
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Please set OPENAI_API_KEY environment variable. "
                "For testing/demo, use MockLLM instead."
            )
        
        # TODO: Configure your preferred model
        self.model = "gpt-4-1106-preview"  # or "gpt-3.5-turbo" for lower cost
        
        self.prompt_template = """
You are an expert IT support technician. Analyze the following issue:

{user_input}

Provide a structured response with:
1. Issue category
2. ONE diagnostic command to run (start with COMMAND:)
3. Likely cause and recommended fix

Only suggest commands from this safe list:
- ping, ping -c 4
- traceroute, tracert
- ipconfig /all, ifconfig -a
- systeminfo
- lpstat -p, lpstat -v
- ps aux, top -n 1

Response format:
Category: <category>
COMMAND: <safe command>
Likely cause: <brief explanation>
"""

        self.followup_template = """
Analyze the diagnostic results:

Initial assessment:
{initial_response}

Command output:
{command_output}

Provide a final diagnosis and specific fix steps.

Format:
Diagnosis: <clear explanation>
Fix: <numbered steps>
"""
    
    async def query(self, prompt: str) -> str:
        """
        Send query to OpenAI API and return structured response.
        
        TODO: Uncomment and complete implementation
        """
        """
        if "Command output:" in prompt:
            system_prompt = self.followup_template
        else:
            system_prompt = self.prompt_template
            
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "messages": [
                            {
                                "role": "system",
                                "content": system_prompt
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        "temperature": 0.7
                    }
                )
                
                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"]
                
        except Exception as e:
            return f"Error calling OpenAI API: {str(e)}"
        """
        raise NotImplementedError(
            "OpenAI integration is disabled by default. "
            "Uncomment the code and set OPENAI_API_KEY to enable."
        )