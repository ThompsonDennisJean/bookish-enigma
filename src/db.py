"""
Database Layer - SQLite + JSON Fallback for Ticket Storage
Copyright (c) 2025 IT Helpdesk Auto-Responder Contributors
MIT License - See LICENSE file
"""

import os
import json
import sqlite3
import aiosqlite
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Union

class TicketStore:
    """
    Manages IT support tickets using SQLite with JSON fallback.
    Handles both storage methods transparently.
    """
    
    def __init__(self):
        # Ensure data directory exists
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        
        self.db_path = self.data_dir / "tickets.db"
        self.json_path = self.data_dir / "diagnostics_log.json"
        
        # Try SQLite first, fall back to JSON if needed
        self.use_sqlite = True
        try:
            self._init_db()
        except sqlite3.Error:
            print("Warning: SQLite initialization failed. Using JSON fallback.")
            self.use_sqlite = False
            
    def _init_db(self):
        """Initialize SQLite database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                issue TEXT NOT NULL,
                diagnosis TEXT,
                command TEXT,
                output TEXT,
                fix TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
    async def create_ticket(self, username: str, issue: str) -> int:
        """Create a new support ticket and return its ID."""
        if self.use_sqlite:
            try:
                async with aiosqlite.connect(self.db_path) as db:
                    cursor = await db.execute(
                        "INSERT INTO tickets (username, issue) VALUES (?, ?)",
                        (username, issue)
                    )
                    await db.commit()
                    return cursor.lastrowid
            except Exception as e:
                print(f"SQLite error: {e}")
                self.use_sqlite = False
                
        # JSON fallback
        try:
            if self.json_path.exists():
                with open(self.json_path) as f:
                    tickets = json.load(f)
                next_id = max(int(t["id"]) for t in tickets) + 1
            else:
                tickets = []
                next_id = 1
                
            tickets.append({
                "id": next_id,
                "username": username,
                "issue": issue,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            })
            
            with open(self.json_path, "w") as f:
                json.dump(tickets, f, indent=2)
                
            return next_id
            
        except Exception as e:
            print(f"Error creating ticket: {e}")
            return -1
            
    async def update_ticket(
        self,
        ticket_id: int,
        diagnosis: Optional[str] = None,
        command: Optional[str] = None,
        output: Optional[str] = None,
        fix: Optional[str] = None
    ) -> bool:
        """Update an existing ticket with diagnostic results."""
        if self.use_sqlite:
            try:
                async with aiosqlite.connect(self.db_path) as db:
                    # Build dynamic update query based on provided fields
                    fields = []
                    values = []
                    if diagnosis:
                        fields.append("diagnosis = ?")
                        values.append(diagnosis)
                    if command:
                        fields.append("command = ?")
                        values.append(command)
                    if output:
                        fields.append("output = ?")
                        values.append(output)
                    if fix:
                        fields.append("fix = ?")
                        values.append(fix)
                        
                    fields.append("updated_at = CURRENT_TIMESTAMP")
                    values.append(ticket_id)
                    
                    query = f"UPDATE tickets SET {', '.join(fields)} WHERE id = ?"
                    await db.execute(query, values)
                    await db.commit()
                    return True
                    
            except Exception as e:
                print(f"SQLite error: {e}")
                self.use_sqlite = False
                
        # JSON fallback
        try:
            if not self.json_path.exists():
                return False
                
            with open(self.json_path) as f:
                tickets = json.load(f)
                
            for ticket in tickets:
                if ticket["id"] == ticket_id:
                    if diagnosis:
                        ticket["diagnosis"] = diagnosis
                    if command:
                        ticket["command"] = command
                    if output:
                        ticket["output"] = output
                    if fix:
                        ticket["fix"] = fix
                    ticket["updated_at"] = datetime.now().isoformat()
                    break
                    
            with open(self.json_path, "w") as f:
                json.dump(tickets, f, indent=2)
                
            return True
            
        except Exception as e:
            print(f"Error updating ticket: {e}")
            return False
            
    async def get_ticket(self, ticket_id: int) -> Optional[Dict]:
        """Retrieve a ticket by ID."""
        if self.use_sqlite:
            try:
                async with aiosqlite.connect(self.db_path) as db:
                    async with db.execute(
                        "SELECT * FROM tickets WHERE id = ?",
                        (ticket_id,)
                    ) as cursor:
                        row = await cursor.fetchone()
                        if row:
                            columns = [desc[0] for desc in cursor.description]
                            return dict(zip(columns, row))
                        return None
                        
            except Exception as e:
                print(f"SQLite error: {e}")
                self.use_sqlite = False
                
        # JSON fallback
        try:
            if not self.json_path.exists():
                return None
                
            with open(self.json_path) as f:
                tickets = json.load(f)
                
            for ticket in tickets:
                if ticket["id"] == ticket_id:
                    return ticket
                    
            return None
            
        except Exception as e:
            print(f"Error retrieving ticket: {e}")
            return None