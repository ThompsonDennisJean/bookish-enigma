// IT Helpdesk Auto-Responder Frontend
// Copyright (c) 2025 IT Helpdesk Auto-Responder Contributors
// MIT License - See LICENSE file

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('helpdesk-form');
    const submitBtn = document.getElementById('submit-btn');
    const loading = document.getElementById('loading');
    const error = document.getElementById('error');
    const result = document.getElementById('result');
    
    // Result display elements
    const diagnosisEl = document.getElementById('diagnosis');
    const commandEl = document.getElementById('command');
    const outputEl = document.getElementById('output');
    const fixEl = document.getElementById('fix');
    const ticketEl = document.getElementById('ticket');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Reset display
        error.style.display = 'none';
        result.style.display = 'none';
        loading.style.display = 'block';
        submitBtn.disabled = true;
        
        try {
            // Get form data
            const username = document.getElementById('username').value;
            const issue = document.getElementById('issue').value;
            
            // Call API
            const response = await fetch('/diagnose', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, issue })
            });
            
            if (!response.ok) {
                throw new Error('Server error: ' + response.statusText);
            }
            
            // Parse and display results
            const data = await response.json();
            
            diagnosisEl.textContent = data.diagnosis || 'No diagnosis available';
            commandEl.textContent = data.executed_command || 'No command executed';
            outputEl.textContent = data.command_output || 'No command output';
            fixEl.textContent = data.suggested_fix || 'No fix suggested';
            ticketEl.textContent = `#${data.ticket_id}`;
            
            result.style.display = 'block';
            
        } catch (err) {
            error.textContent = 'Error: ' + err.message;
            error.style.display = 'block';
        } finally {
            loading.style.display = 'none';
            submitBtn.disabled = false;
        }
    });
});