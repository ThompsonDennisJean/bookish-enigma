# IT Helpdesk Auto-Responder Setup Instructions

This guide provides step-by-step instructions for setting up and running the IT Helpdesk Auto-Responder on different platforms.

## Prerequisites

- Python 3.10 or higher
- Git
- Basic command line familiarity

## Setup Instructions

### Linux/macOS

1. Clone the repository:
```bash
git clone https://github.com/your-username/it-helpdesk-autoresponder.git
cd it-helpdesk-autoresponder
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Enable simulation mode for safe testing:
```bash
export FORCE_SIMULATION=true
```

5. Start the server:
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Windows (PowerShell)

1. Clone the repository:
```powershell
git clone https://github.com/your-username/it-helpdesk-autoresponder.git
cd it-helpdesk-autoresponder
```

2. Create a virtual environment:
```powershell
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:
```powershell
pip install -r requirements.txt
```

4. Enable simulation mode:
```powershell
$env:FORCE_SIMULATION = "true"
```

5. Start the server:
```powershell
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## Running Tests

1. Ensure you're in the virtual environment
2. Run the test suite:
```bash
pytest
```

3. Run with coverage report:
```bash
pytest --cov=src tests/
```

## Running the Demo Script

### Linux/macOS
```bash
chmod +x demo/demo_script.sh
./demo/demo_script.sh
```

### Windows (PowerShell)
```powershell
.\demo\demo_script.bat
```

## Optional: Streamlit UI

1. Start the FastAPI server (as above)

2. In a new terminal, run:
```bash
streamlit run src/streamlit_app.py
```

## Optional: Cloud Integration

### OpenAI Setup

1. Add your API key to `.env`:
```bash
OPENAI_API_KEY=your-key-here
```

2. Update `src/main.py`:
```python
from src.openai_adapter import OpenAIAdapter
llm = OpenAIAdapter()
```

### AWS Bedrock Setup

1. Configure AWS credentials:
```bash
aws configure
```

2. Update `src/main.py`:
```python
from src.aws_stubs.bedrock_stub import BedrockAdapter
llm = BedrockAdapter()
```

## Verification

1. Open http://127.0.0.1:8000 in your browser
2. Submit a test ticket:
   - Name: "Test User"
   - Issue: "My internet is slow"
3. Check for response with diagnosis and fix

## Troubleshooting

### Server Won't Start
- Check Python version: `python --version`
- Verify virtual environment is active
- Confirm no other service on port 8000

### Database Issues
- Check write permissions in `data/` directory
- Delete and let system recreate database
- Try JSON fallback mode

### Command Execution
- Verify FORCE_SIMULATION setting
- Check command whitelist
- Review security settings

## Next Steps

1. Review `docs/project_description.md`
2. Study `examples/sample_conversation.md`
3. Check `CONTRIBUTING.md` for development
4. Explore cloud integration options

## Support

- Create GitHub issue for bugs
- Check documentation for usage
- Review security guidelines