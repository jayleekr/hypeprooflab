# HypeProof Lab - Technology Stack

## Language and Runtime

| Component | Specification |
|-----------|---------------|
| Language | Python 3.11+ |
| Package Manager | pip with pyproject.toml |
| Runtime | CPython with asyncio support |
| Type Checking | Static typing with pyright |

## Core Dependencies

### AI and Agent Framework

| Package | Version | Purpose |
|---------|---------|---------|
| claude-agent-sdk | >=1.0.0 | Claude AI SDK for agent development |
| pydantic | >=2.0 | Data validation and type safety |

**Rationale:** Claude Agent SDK provides the foundation for building multi-agent systems with proper context isolation. Pydantic 2.0 offers significant performance improvements and native support for modern Python typing features.

### Configuration and Environment

| Package | Version | Purpose |
|---------|---------|---------|
| pyyaml | >=6.0 | YAML configuration file parsing |
| python-dotenv | >=1.0.0 | Environment variable management |

**Rationale:** YAML provides human-readable configuration for agents and workflows. python-dotenv enables secure credential management through `.env` files.

### Logging and Observability

| Package | Version | Purpose |
|---------|---------|---------|
| structlog | >=23.0 | Structured JSON logging |

**Rationale:** structlog produces JSON-formatted logs suitable for production log aggregation systems. Custom processors enable API key scrubbing to prevent credential exposure.

### Async Runtime

| Package | Version | Purpose |
|---------|---------|---------|
| asyncio | >=3.4.3 | Asynchronous task execution |

**Rationale:** asyncio enables parallel agent execution, allowing independent tasks to run simultaneously and reducing total execution time from 35 minutes (sequential) to 15 minutes (parallel).

## Development Dependencies

### Testing Framework

| Package | Version | Purpose |
|---------|---------|---------|
| pytest | >=7.0 | Test framework |
| pytest-asyncio | >=0.21.0 | Async test support |
| pytest-cov | >=4.0 | Coverage reporting |
| pytest-mock | >=3.10 | Mocking utilities |

**Configuration:**
- Test discovery: `tests/` directory
- Coverage target: 85% minimum
- Async mode: auto (pytest-asyncio)
- Reports: terminal-missing + HTML

### Code Quality Tools

| Package | Version | Purpose |
|---------|---------|---------|
| black | >=23.0 | Code formatting |
| ruff | >=0.1.0 | Fast Python linting |
| pyright | >=1.1.0 | Static type checking |

**Configuration:**

**Black:**
- Line length: 88 characters
- Target version: Python 3.11

**Ruff:**
- Line length: 88 characters
- Target version: Python 3.11
- Rule sets: E, F, I, N, W, UP, B, A, C4, DTZ, T10, ISC, ICN, PIE, PT, RSE, RET, SIM, TID, TCH, ARG, PLE, PLW, TRY, RUF
- Ignored: E501 (line length handled by black)

**Pyright:**
- Mode: basic
- Include: src/
- Exclude: __pycache__, tests

## Build and Test Configuration

### pytest.ini Settings

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
asyncio_mode = auto
addopts = -v --cov=src --cov-report=term-missing --cov-report=html
```

### Coverage Configuration

**Run Settings:**
- Source: src/
- Omit: tests/*, **/__pycache__/*

**Report Exclusions:**
- `pragma: no cover` comments
- `__repr__` methods
- `raise AssertionError`
- `raise NotImplementedError`
- `if __name__ == "__main__":`
- `if TYPE_CHECKING:`
- `@abstractmethod` decorated methods

## Quality Standards (TRUST 5)

| Pillar | Tool | Requirement |
|--------|------|-------------|
| Tested | pytest + pytest-cov | 85%+ coverage |
| Readable | ruff | No lint errors |
| Unified | black | Consistent formatting |
| Secured | OWASP compliance | Input validation, key scrubbing |
| Trackable | Conventional Commits | Structured commit messages |

### LSP Quality Gates

| Phase | Requirement |
|-------|-------------|
| plan | Capture LSP baseline |
| run | Zero errors, zero type errors, zero lint errors |
| sync | Zero errors, max 10 warnings, clean LSP |

## Development Environment

### Prerequisites

- Python 3.11 or higher
- pip (latest version)
- Git

### Setup Commands

```bash
# Clone repository
git clone <repository-url>
cd hypeproof

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Unix
# or
.\venv\Scripts\activate   # Windows

# Install dependencies
pip install -e .           # Production
pip install -e ".[dev]"    # Development (includes testing and linting)
```

### Environment Variables

Required environment variables (via `.env` file):
- `ANTHROPIC_API_KEY` - Claude API authentication

### Running Tests

```bash
# Run all tests with coverage
pytest

# Run specific test file
pytest tests/test_agents.py

# Run with verbose output
pytest -v

# Generate HTML coverage report
pytest --cov-report=html
```

### Code Quality Checks

```bash
# Format code
black src/ tests/

# Run linter
ruff check src/ tests/

# Fix auto-fixable issues
ruff check --fix src/ tests/

# Type checking
pyright src/
```

## MCP Server Integration

The project integrates with Model Context Protocol (MCP) servers configured in `.mcp.json`:

| Server | Purpose |
|--------|---------|
| Context7 | Official library documentation |
| Sequential | Complex analysis and reasoning |
| Playwright | Browser automation and testing |

## Documentation Tools

| Tool | Purpose |
|------|---------|
| mkdocs | Documentation site generation |
| mkdocs-material | Material theme for mkdocs |

## Deployment Considerations

- Python 3.11+ runtime required
- Async-compatible execution environment
- Environment variable injection for API keys
- Structured log aggregation support (JSON format)
- 85%+ test coverage verification in CI/CD
