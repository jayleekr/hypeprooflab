"""
Pytest configuration and shared fixtures.

This module provides common fixtures and configuration for all tests.
"""

import sys
from unittest.mock import MagicMock, AsyncMock

# Mock claude-agent-sdk before other imports
sys.modules['claude_agent_sdk'] = MagicMock()
sys.modules['claude_agent_sdk'].ClaudeSDKClient = MagicMock
sys.modules['claude_agent_sdk'].ClaudeAgentOptions = MagicMock

import os
from pathlib import Path
from typing import Dict

import pytest

from src.core.registry import AgentRegistry
from src.core.types import AgentConfig, AgentResult, ExecutionStatus, TokenUsage


@pytest.fixture
def test_config_dir(tmp_path):
    """Create temporary config directory with test YAML files.

    Args:
        tmp_path: pytest temporary directory fixture

    Returns:
        Path to temporary config directory
    """
    config_dir = tmp_path / "config"
    config_dir.mkdir()

    # Create test agents.yaml
    agents_yaml = config_dir / "agents.yaml"
    agents_yaml.write_text(
        """
agents:
  test_agent:
    name: "Test Agent"
    role: "Testing purposes"
    tools:
      - Read
      - Write
    max_retries: 2
    timeout: 60
    model: "claude-sonnet-4-20250514"
"""
    )

    # Create test settings.yaml
    settings_yaml = config_dir / "settings.yaml"
    settings_yaml.write_text(
        """
system:
  environment: "test"
  log_level: "DEBUG"
  default_model: "claude-sonnet-4-20250514"
  max_retries: 2
  timeout: 60
"""
    )

    return config_dir


@pytest.fixture
def sample_agent_config():
    """Provide sample AgentConfig for testing.

    Returns:
        AgentConfig instance
    """
    return AgentConfig(
        name="test_agent",
        role="Test agent for unit tests",
        tools=["Read", "Write"],
        max_retries=2,
        timeout=60,
        model="claude-sonnet-4-20250514",
    )


@pytest.fixture
def sample_agent_result():
    """Provide sample AgentResult for testing.

    Returns:
        AgentResult instance with success status
    """
    return AgentResult(
        status=ExecutionStatus.SUCCESS,
        output={"message": "Test completed successfully"},
        token_usage=TokenUsage(
            input_tokens=100, output_tokens=200, total_tokens=300, cost_estimate=0.01
        ),
        execution_time=1.5,
        error_message=None,
    )


@pytest.fixture
def sample_error_result():
    """Provide sample error AgentResult for testing.

    Returns:
        AgentResult instance with error status
    """
    return AgentResult(
        status=ExecutionStatus.ERROR,
        output=None,
        token_usage=None,
        execution_time=0.5,
        error_message="Test error occurred",
    )


@pytest.fixture
def mock_claude_client():
    """Provide mock Claude SDK client.

    Returns:
        Mock ClaudeSDKClient with async query method
    """
    mock = MagicMock()
    mock.query = AsyncMock()
    mock.query.return_value = MagicMock(
        result="Test response from Claude",
        token_usage={"input_tokens": 100, "output_tokens": 200, "total_tokens": 300},
    )
    return mock


@pytest.fixture
def agent_registry():
    """Provide fresh AgentRegistry for each test.

    Returns:
        AgentRegistry instance
    """
    registry = AgentRegistry()
    return registry


@pytest.fixture
def sample_research_output():
    """Provide sample research output structure.

    Returns:
        Dict with research output format
    """
    return {
        "findings": [
            "Finding 1: Latest AI trends show significant growth",
            "Finding 2: Claude models are widely adopted",
        ],
        "sources": [
            {"url": "https://example.com/ai-trends", "title": "AI Trends 2025"},
            {"url": "https://example.com/claude", "title": "Claude Overview"},
        ],
        "confidence": "high",
        "additional_research_needed": ["Market size analysis", "Competitor comparison"],
    }


@pytest.fixture(autouse=True)
def reset_environment():
    """Reset environment variables before each test.

    This fixture runs automatically for all tests.
    """
    # Store original environment
    original_env = os.environ.copy()

    # Set test environment variables
    os.environ["ANTHROPIC_API_KEY"] = "sk-ant-test-key-123456"
    os.environ["LOG_LEVEL"] = "DEBUG"

    yield

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def event_loop_policy():
    """Set event loop policy for async tests."""
    import asyncio

    return asyncio.DefaultEventLoopPolicy()
