"""
IT Helpdesk Auto-Responder FastAPI Application
Copyright (c) 2025 IT Helpdesk Auto-Responder Contributors
MIT License - See LICENSE file
"""

import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .mock_llm import MockLLM
from .diagnostics import DiagnosticsExecutor
from .db import TicketStore

# Initialize FastAPI app
app = FastAPI(
    title="IT Helpdesk Auto-Responder",
    description="Automated IT issue diagnostics and resolution",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For demo only - configure properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static frontend
app.mount("/static", StaticFiles(directory="src/frontend"), name="static")

# Initialize components
llm = MockLLM()  # Can be swapped for OpenAI or Bedrock
diagnostics = DiagnosticsExecutor()
db = TicketStore()

class DiagnosisRequest(BaseModel):
    username: str
    issue: str

class DiagnosisResponse(BaseModel):
    ticket_id: int
    diagnosis: str
    executed_command: Optional[str]
    command_output: Optional[str]
    suggested_fix: str

@app.post("/diagnose", response_model=DiagnosisResponse)
async def diagnose_issue(request: DiagnosisRequest):
    """
    Process an IT help request:
    1. Store initial ticket
    2. Get LLM analysis and command suggestion
    3. Execute safe diagnostic command
    4. Get final LLM diagnosis
    5. Store and return results
    """
    try:
        # Create ticket
        ticket_id = await db.create_ticket(request.username, request.issue)

        # Get initial LLM analysis
        initial_response = llm.query(
            f"User '{request.username}' reports issue: {request.issue}\n"
            "Analyze the issue and suggest ONE safe diagnostic command.\n"
            "Format: Category: <category>\nCOMMAND: <command>\nLikely cause: <cause>"
        )

        # Extract command if present
        command = None
        command_output = None
        for line in initial_response.split("\n"):
            if line.startswith("COMMAND:"):
                command = line.replace("COMMAND:", "").strip()
                break

        # Execute command if safe
        if command and diagnostics.is_allowed(command):
            result = await diagnostics.run_command(command)
            command_output = result["stdout"] + "\n" + result["stderr"]

        # Get final diagnosis with command output context
        context = f"Initial analysis: {initial_response}\n"
        if command_output:
            context += f"Command '{command}' output:\n{command_output}\n"
        
        final_response = llm.query(
            f"{context}\n"
            "Based on this information, provide a final diagnosis and fix:\n"
            "Format: Diagnosis: <diagnosis>\nFix: <specific steps>"
        )

        # Extract diagnosis and fix
        diagnosis = "Unknown issue"
        suggested_fix = "Please contact IT support"
        for line in final_response.split("\n"):
            if line.startswith("Diagnosis:"):
                diagnosis = line.replace("Diagnosis:", "").strip()
            elif line.startswith("Fix:"):
                suggested_fix = line.replace("Fix:", "").strip()

        # Store results
        await db.update_ticket(
            ticket_id,
            diagnosis=diagnosis,
            command=command,
            output=command_output,
            fix=suggested_fix
        )

        return DiagnosisResponse(
            ticket_id=ticket_id,
            diagnosis=diagnosis,
            executed_command=command,
            command_output=command_output,
            suggested_fix=suggested_fix
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """Serve the frontend HTML"""
    return StaticFiles(directory="src/frontend", html=True)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)