# Contributing to IT Helpdesk Auto-Responder

We love your input! We want to make contributing to IT Helpdesk Auto-Responder as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## We Develop with Github

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## Code Style & Standards

1. We use [Black](https://github.com/psf/black) for Python code formatting:
```bash
black src/ tests/
```

2. Type hints are required for all function parameters and returns:
```python
def process_ticket(username: str, issue: str) -> Dict[str, Any]:
    ...
```

3. Docstrings (Google style) for all public functions and classes:
```python
def diagnose_issue(issue: str) -> str:
    """
    Analyze an IT issue and suggest diagnostics.
    
    Args:
        issue: The user-reported issue description
        
    Returns:
        Structured diagnosis with suggested commands
        
    Raises:
        ValueError: If issue description is empty
    """
    ...
```

4. Security-focused development:
- No arbitrary command execution
- Input validation required
- Clear error handling
- Explicit security comments

## Development Process

1. Fork the repo and create your branch from `main`
2. Make your changes
3. Ensure tests pass (`pytest`)
4. Update documentation if needed
5. Issue that pull request!

## Pull Request Process

1. Update the README.md with details of changes if needed
2. Update docs/ with any new information
3. The PR will be merged once you have the sign-off of a maintainer

## Testing Requirements

1. Add tests for any new functionality
2. Run the full test suite before submitting:
```bash
# Run all tests
pytest

# With coverage
pytest --cov=src tests/
```

3. Maintain or improve code coverage

## Security Guidelines

1. Command Safety:
- Only add safe diagnostic commands
- No system modifications
- No privileged operations
- Clear documentation

2. Input Validation:
- Sanitize all inputs
- Validate command arguments
- Check file paths
- Handle edge cases

3. Error Handling:
- Graceful degradation
- Clear error messages
- No sensitive data exposure
- Proper logging

## Local Development

1. Set up your environment:
```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

2. Enable development mode:
```bash
export FORCE_SIMULATION=true
```

3. Run the server:
```bash
uvicorn src.main:app --reload --port 8000
```

## Documentation

1. Keep README.md updated
2. Document all new features
3. Update architecture diagrams
4. Add example conversations

## Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

## License

By contributing, you agree that your contributions will be licensed under its MIT License.

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Black Code Style](https://black.readthedocs.io/en/stable/)