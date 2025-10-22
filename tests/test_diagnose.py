"""
Tests for IT Helpdesk Auto-Responder
Copyright (c) 2025 IT Helpdesk Auto-Responder Contributors
MIT License - See LICENSE file
"""

import os
import pytest
import json
from fastapi.testclient import TestClient
from unittest.mock import patch

from src.main import app
from src.diagnostics import DiagnosticsExecutor

# Configure test client
client = TestClient(app)

@pytest.fixture
def mock_command_output():
    """Mock diagnostic command output."""
    return {
        "cmd": "ping -c 4 google.com",
        "stdout": "4 packets transmitted, 4 received, 0% packet loss",
        "stderr": "",
        "returncode": 0,
        "runtime_ms": 100
    }

def test_diagnose_endpoint_success(mock_command_output):
    """Test successful diagnosis request."""
    # Mock the command execution
    with patch.object(DiagnosticsExecutor, 'run_command', return_value=mock_command_output):
        response = client.post(
            "/diagnose",
            json={
                "username": "testuser",
                "issue": "My internet is slow"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Check required fields
        assert "diagnosis" in data
        assert "suggested_fix" in data
        assert "ticket_id" in data
        assert isinstance(data["ticket_id"], int)
        
        # Check command execution
        assert data["executed_command"] == "ping -c 4 google.com"
        assert "0% packet loss" in data["command_output"]

def test_diagnose_endpoint_bad_request():
    """Test invalid request handling."""
    response = client.post(
        "/diagnose",
        json={"username": "testuser"}  # Missing required 'issue' field
    )
    assert response.status_code == 422

def test_command_whitelist():
    """Test command security whitelist."""
    dx = DiagnosticsExecutor()
    
    # Test allowed commands
    assert dx.is_allowed("ping -c 4 google.com")
    assert dx.is_allowed("systeminfo")
    
    # Test disallowed commands
    assert not dx.is_allowed("rm -rf /")
    assert not dx.is_allowed("sudo reboot")
    assert not dx.is_allowed("ping google.com | grep")

def test_simulation_mode():
    """Test simulation mode functionality."""
    # Enable simulation
    os.environ["FORCE_SIMULATION"] = "true"
    dx = DiagnosticsExecutor()
    
    result = dx.simulate_command("ping -c 4 google.com")
    assert "packet loss" in result["stdout"]
    assert result["returncode"] == 0
    
    # Cleanup
    os.environ.pop("FORCE_SIMULATION", None)

def test_mock_llm_responses():
    """Test mock LLM response patterns."""
    from src.mock_llm import MockLLM
    llm = MockLLM()
    
    # Test network issue
    response = llm.query("My internet is slow and keeps disconnecting")
    assert "Category: Network" in response
    assert "COMMAND:" in response
    
    # Test printer issue
    response = llm.query("The printer isn't working")
    assert "Category: Print" in response
    assert "COMMAND:" in response
    
    # Test system issue
    response = llm.query("My computer is very slow")
    assert "Category: System" in response
    assert "COMMAND:" in response

def test_database_operations():
    """Test ticket database operations."""
    from src.db import TicketStore
    db = TicketStore()
    
    # Test ticket creation and retrieval
    ticket_id = db.create_ticket("testuser", "Test issue")
    assert ticket_id > 0
    
    ticket = db.get_ticket(ticket_id)
    assert ticket["username"] == "testuser"
    assert ticket["issue"] == "Test issue"
    
    # Test ticket update
    success = db.update_ticket(
        ticket_id,
        diagnosis="Test diagnosis",
        fix="Test fix"
    )
    assert success
    
    updated = db.get_ticket(ticket_id)
    assert updated["diagnosis"] == "Test diagnosis"
    assert updated["fix"] == "Test fix"