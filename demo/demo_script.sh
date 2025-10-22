#!/bin/bash
# Demo script for IT Helpdesk Auto-Responder
# Copyright (c) 2025 IT Helpdesk Auto-Responder Contributors
# MIT License - See LICENSE file

# Ensure we're in simulation mode
export FORCE_SIMULATION=true

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting IT Helpdesk Auto-Responder demo...${NC}"

# Start the server in background
echo "Starting FastAPI server..."
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 &
SERVER_PID=$!

# Wait for server to start
sleep 5

# Function to make API requests and save output
make_request() {
    local username=$1
    local issue=$2
    local outfile=$3
    
    echo -e "${GREEN}Testing: $issue${NC}"
    
    # Make the request
    curl -s -X POST http://localhost:8000/diagnose \
        -H "Content-Type: application/json" \
        -d "{\"username\": \"$username\", \"issue\": \"$issue\"}" \
        | tee -a "$outfile"
        
    echo -e "\n" >> "$outfile"
    echo "----------------------------------------" >> "$outfile"
}

# Create output directory
mkdir -p demo
OUTPUT_FILE="demo/demo_output.txt"

# Clear previous output
echo "IT Helpdesk Auto-Responder Demo Results" > $OUTPUT_FILE
echo "Generated: $(date)" >> $OUTPUT_FILE
echo "----------------------------------------" >> $OUTPUT_FILE

# Test Case 1: Network Issue
make_request "alice" "My internet connection is very slow and keeps dropping" $OUTPUT_FILE

# Test Case 2: Printer Issue
make_request "bob" "The office printer says offline and won't print anything" $OUTPUT_FILE

# Cleanup
echo "Stopping server..."
kill $SERVER_PID

echo -e "${BLUE}Demo complete! Results saved to demo/demo_output.txt${NC}"
echo "To run the demo yourself:"
echo "1. python -m venv venv"
echo "2. source venv/bin/activate  # or 'venv\\Scripts\\activate' on Windows"
echo "3. pip install -r requirements.txt"
echo "4. export FORCE_SIMULATION=true  # or 'set FORCE_SIMULATION=true' on Windows"
echo "5. ./demo/demo_script.sh"