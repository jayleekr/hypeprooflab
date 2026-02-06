# HypeProof Lab - Project Structure

## Directory Tree

```
hypeproof/
├── src/                          # Source code (Python package)
│   ├── __init__.py
│   ├── agents/                   # Specialized AI agents
│   │   ├── __init__.py
│   │   ├── base_agent.py         # Abstract base agent class
│   │   ├── research_agent.py     # Web search and information gathering
│   │   ├── analysis_agent.py     # Data analysis and synthesis
│   │   └── writing_agent.py      # Content generation
│   ├── commands/                 # Slash command handlers
│   │   ├── __init__.py
│   │   └── research.py           # /research command implementation
│   ├── skills/                   # Orchestration layer (Phase 1.5 placeholder)
│   │   └── __init__.py
│   └── core/                     # Core infrastructure
│       ├── __init__.py
│       ├── types.py              # Type definitions and data models
│       ├── logger.py             # Structured logging with key scrubbing
│       ├── error_handler.py      # Custom exceptions and retry logic
│       ├── config_loader.py      # YAML configuration parsing
│       └── registry.py           # Agent registry (singleton pattern)
│
├── config/                       # Configuration files
│   ├── agents.yaml               # Agent definitions and settings
│   └── settings.yaml             # Application settings
│
├── tests/                        # Test suite
│   └── (pytest test files)       # 85%+ coverage requirement
│
├── docs/                         # Documentation
│   ├── architecture.md           # Architecture reference document
│   └── ai_agent_system.md        # AI agent system documentation
│
├── content/                      # Podcast content management
│   ├── seasons/                  # Season-based organization
│   │   └── season_1/
│   │       └── _season_info.md
│   └── topic_pool.md             # Topic ideas and backlog
│
├── research/                     # Research system
│   ├── claims/                   # Claim tracking
│   │   └── _index.md
│   └── lens/                     # Research lens framework
│       └── labeling_guide.md
│
├── templates/                    # Content templates
│   ├── episode_prep.md           # Episode preparation template
│   ├── light_runsheet.md         # Light runsheet template
│   ├── claim_card.md             # Claim card template
│   └── action_item_weekly.md     # Weekly action items
│
├── members/                      # Team member profiles
│   ├── Jay/profile.md
│   ├── TJ/profile.md
│   ├── Kiwon/profile.md
│   ├── 지웅/profile.md
│   └── 진용/profile.md
│
├── action_items/                 # Action item tracking
│   └── 2026/01_january/
│       └── week_03.md
│
├── workflows/                    # Workflow documentation
│   └── feedback.md               # Feedback workflow
│
├── meeting_notes/                # Meeting documentation
│   └── (meeting transcripts)
│
├── .moai/                        # MoAI-ADK configuration
│   ├── config/                   # MoAI configuration
│   │   └── sections/
│   │       ├── quality.yaml      # Quality gate settings
│   │       ├── user.yaml         # User preferences
│   │       └── language.yaml     # Language settings
│   ├── docs/                     # Generated documentation
│   ├── logs/                     # Execution logs
│   ├── memory/                   # Agent memory storage
│   ├── project/                  # Project documentation
│   ├── specs/                    # SPEC documents
│   ├── backups/                  # Configuration backups
│   └── reports/                  # Generated reports
│
├── .claude/                      # Claude Code configuration
│   ├── agents/moai/              # MoAI agent definitions
│   ├── commands/                 # Custom slash commands
│   ├── skills/                   # Skill definitions
│   └── rules/moai/               # MoAI rule files
│
├── pyproject.toml                # Python project configuration
├── pytest.ini                    # Pytest configuration
├── requirements.txt              # Production dependencies
├── requirements-dev.txt          # Development dependencies
├── CLAUDE.md                     # Claude Code project instructions
└── .mcp.json                     # MCP server configuration
```

## Module Organization

### Source Code (`src/`)

#### Agents Layer (`src/agents/`)
Specialized AI agents that execute tasks in isolated contexts.

| File | Purpose |
|------|---------|
| `base_agent.py` | Abstract base class defining agent interface with `execute()` method |
| `research_agent.py` | Web search and information gathering using WebSearch/WebFetch |
| `analysis_agent.py` | Data analysis, synthesis, and insight extraction |
| `writing_agent.py` | Content creation including scripts, articles, documentation |

#### Commands Layer (`src/commands/`)
User-facing slash command handlers that trigger workflows.

| File | Purpose |
|------|---------|
| `research.py` | Handles `/research` command for deep research workflows |

#### Skills Layer (`src/skills/`)
Orchestration layer for coordinating multiple agents (Phase 1.5 placeholder).

| Status | Description |
|--------|-------------|
| Planned | Will contain skill orchestrators like `content_creation.py`, `deep_research.py` |

#### Core Infrastructure (`src/core/`)
Shared utilities and system infrastructure.

| File | Purpose |
|------|---------|
| `types.py` | Type definitions, data models, and Pydantic schemas |
| `logger.py` | Structured JSON logging with API key scrubbing |
| `error_handler.py` | Custom exception hierarchy with retry support |
| `config_loader.py` | YAML configuration file parsing |
| `registry.py` | Singleton agent registry for efficient management |

### Configuration (`config/`)

| File | Purpose |
|------|---------|
| `agents.yaml` | Agent definitions, tools, and settings |
| `settings.yaml` | Application-wide configuration |

### Tests (`tests/`)
Pytest test suite targeting 85%+ code coverage with async support.

### Documentation (`docs/`)
Project documentation including architecture reference and system design.

## Key File Locations

| Purpose | Location |
|---------|----------|
| Entry point | `src/__init__.py` |
| Agent base class | `src/agents/base_agent.py` |
| Research command | `src/commands/research.py` |
| Logging utility | `src/core/logger.py` |
| Type definitions | `src/core/types.py` |
| Agent registry | `src/core/registry.py` |
| Project config | `pyproject.toml` |
| Test config | `pytest.ini` |
| Quality settings | `.moai/config/sections/quality.yaml` |

## Architecture Layers

```
┌─────────────────────────────────────────────────────────┐
│                 Commands Layer (Interface)               │
│  /research, /podcast (future), /proposal (future)       │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│               Skills Layer (Orchestration)               │
│  Content Creation, Deep Research, Quality Check          │
│  (Phase 1.5 - Currently placeholder)                     │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                 Agents Layer (Execution)                 │
│  Research Agent | Analysis Agent | Writing Agent         │
│  (Each with independent context window)                  │
└─────────────────────────────────────────────────────────┘
```
