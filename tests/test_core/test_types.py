"""
Tests for core type definitions.

This module tests the Pydantic models and enums used throughout
the HypeProof Lab system.
"""

import pytest
from pydantic import ValidationError

from src.core.types import (
    AgentConfig,
    AgentResult,
    ExecutionStatus,
    SkillConfig,
    TokenUsage,
)


class TestExecutionStatus:
    """Test suite for ExecutionStatus enum."""

    def test_execution_status_values(self):
        """Test ExecutionStatus has correct values."""
        assert ExecutionStatus.SUCCESS == "success"
        assert ExecutionStatus.ERROR == "error"
        assert ExecutionStatus.TIMEOUT == "timeout"

    def test_execution_status_from_string(self):
        """Test creating ExecutionStatus from string."""
        status = ExecutionStatus("success")
        assert status == ExecutionStatus.SUCCESS


class TestTokenUsage:
    """Test suite for TokenUsage model."""

    def test_token_usage_creation(self):
        """Test creating TokenUsage instance."""
        usage = TokenUsage(
            input_tokens=100,
            output_tokens=200,
            total_tokens=300,
            cost_estimate=0.015,
        )

        assert usage.input_tokens == 100
        assert usage.output_tokens == 200
        assert usage.total_tokens == 300
        assert usage.cost_estimate == 0.015

    def test_token_usage_default_cost(self):
        """Test TokenUsage has default cost_estimate of 0.0."""
        usage = TokenUsage(
            input_tokens=100,
            output_tokens=200,
            total_tokens=300,
        )

        assert usage.cost_estimate == 0.0

    def test_token_usage_validation(self):
        """Test TokenUsage validates field types."""
        with pytest.raises(ValidationError):
            TokenUsage(
                input_tokens="invalid",  # Should be int
                output_tokens=200,
                total_tokens=300,
            )


class TestAgentResult:
    """Test suite for AgentResult model."""

    def test_agent_result_success(self):
        """Test creating successful AgentResult."""
        result = AgentResult(
            status=ExecutionStatus.SUCCESS,
            output={"data": "test"},
            execution_time=1.5,
        )

        assert result.status == ExecutionStatus.SUCCESS
        assert result.output == {"data": "test"}
        assert result.execution_time == 1.5
        assert result.token_usage is None
        assert result.error_message is None

    def test_agent_result_error(self):
        """Test creating error AgentResult."""
        result = AgentResult(
            status=ExecutionStatus.ERROR,
            output=None,
            execution_time=0.5,
            error_message="Test error",
        )

        assert result.status == ExecutionStatus.ERROR
        assert result.output is None
        assert result.error_message == "Test error"

    def test_agent_result_with_token_usage(self):
        """Test AgentResult with token usage."""
        usage = TokenUsage(
            input_tokens=100,
            output_tokens=200,
            total_tokens=300,
        )

        result = AgentResult(
            status=ExecutionStatus.SUCCESS,
            output={"data": "test"},
            token_usage=usage,
            execution_time=2.0,
        )

        assert result.token_usage == usage
        assert result.token_usage.input_tokens == 100


class TestAgentConfig:
    """Test suite for AgentConfig model."""

    def test_agent_config_creation(self):
        """Test creating AgentConfig instance."""
        config = AgentConfig(
            name="test_agent",
            role="Testing agent",
            tools=["Read", "Write"],
            max_retries=3,
            timeout=300,
            model="claude-sonnet-4-20250514",
        )

        assert config.name == "test_agent"
        assert config.role == "Testing agent"
        assert config.tools == ["Read", "Write"]
        assert config.max_retries == 3
        assert config.timeout == 300
        assert config.model == "claude-sonnet-4-20250514"

    def test_agent_config_defaults(self):
        """Test AgentConfig has correct default values."""
        config = AgentConfig(
            name="test_agent",
            role="Testing",
            tools=["Read"],
        )

        assert config.max_retries == 3
        assert config.timeout == 300
        assert config.model == "claude-sonnet-4-20250514"

    def test_agent_config_validation(self):
        """Test AgentConfig validates required fields."""
        with pytest.raises(ValidationError):
            AgentConfig(
                name="test",
                # Missing required 'role' field
                tools=["Read"],
            )


class TestSkillConfig:
    """Test suite for SkillConfig model."""

    def test_skill_config_creation(self):
        """Test creating SkillConfig instance."""
        config = SkillConfig(
            name="test_skill",
            description="Test skill",
            agents=["agent1", "agent2"],
            parallel=True,
        )

        assert config.name == "test_skill"
        assert config.description == "Test skill"
        assert config.agents == ["agent1", "agent2"]
        assert config.parallel is True

    def test_skill_config_defaults(self):
        """Test SkillConfig has correct default values."""
        config = SkillConfig(
            name="test_skill",
            description="Test",
            agents=["agent1"],
        )

        assert config.parallel is False

    def test_skill_config_validation(self):
        """Test SkillConfig validates field types."""
        with pytest.raises(ValidationError):
            SkillConfig(
                name="test_skill",
                description="Test",
                agents="not_a_list",  # Should be list
            )
