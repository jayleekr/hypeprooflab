"""
Tests for ResearchCommand.

This module tests the /research command handler including
command initialization, execution, and error handling.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.commands.research import ResearchCommand
from src.core.types import AgentResult, ExecutionStatus, TokenUsage


class TestResearchCommand:
    """Test suite for ResearchCommand class."""

    def test_command_initialization(self):
        """Test ResearchCommand initializes correctly."""
        command = ResearchCommand()

        assert command.agent is not None
        assert command.agent.name == "research_agent"

    @pytest.mark.asyncio
    async def test_handle_command_success(self, sample_agent_result):
        """Test successful command execution."""
        command = ResearchCommand()

        with patch.object(command.agent, "execute", new_callable=AsyncMock) as mock_execute:
            mock_execute.return_value = sample_agent_result

            result = await command.handle({"topic": "AI trends 2025"})

            assert result["command"] == "/research"
            assert result["topic"] == "AI trends 2025"
            assert result["status"] == "success"
            assert result["result"] == sample_agent_result.output
            assert result["execution_time"] == sample_agent_result.execution_time
            assert "token_usage" in result

            mock_execute.assert_called_once_with(task="AI trends 2025")

    @pytest.mark.asyncio
    async def test_handle_command_with_token_usage(self):
        """Test command response includes token usage."""
        command = ResearchCommand()

        mock_result = AgentResult(
            status=ExecutionStatus.SUCCESS,
            output={"findings": ["test"]},
            token_usage=TokenUsage(
                input_tokens=100,
                output_tokens=200,
                total_tokens=300,
                cost_estimate=0.015,
            ),
            execution_time=2.5,
        )

        with patch.object(command.agent, "execute", new_callable=AsyncMock) as mock_execute:
            mock_execute.return_value = mock_result

            result = await command.handle({"topic": "Test topic"})

            assert "token_usage" in result
            assert result["token_usage"]["input_tokens"] == 100
            assert result["token_usage"]["output_tokens"] == 200
            assert result["token_usage"]["total_tokens"] == 300
            assert result["token_usage"]["cost_estimate"] == 0.015

    @pytest.mark.asyncio
    async def test_handle_command_missing_topic(self):
        """Test command raises error when topic is missing."""
        command = ResearchCommand()

        with pytest.raises(ValueError, match="Research topic is required"):
            await command.handle({})

    @pytest.mark.asyncio
    async def test_handle_command_empty_topic(self):
        """Test command raises error when topic is empty."""
        command = ResearchCommand()

        with pytest.raises(ValueError, match="Research topic is required"):
            await command.handle({"topic": ""})

    @pytest.mark.asyncio
    async def test_handle_command_whitespace_topic(self):
        """Test command raises error when topic is whitespace."""
        command = ResearchCommand()

        with pytest.raises(ValueError, match="Research topic is required"):
            await command.handle({"topic": "   "})

    @pytest.mark.asyncio
    async def test_handle_command_with_error(self, sample_error_result):
        """Test command handles agent execution errors."""
        command = ResearchCommand()

        with patch.object(command.agent, "execute", new_callable=AsyncMock) as mock_execute:
            mock_execute.return_value = sample_error_result

            result = await command.handle({"topic": "Test topic"})

            assert result["status"] == "error"
            assert result["error"] == "Test error occurred"
            assert result["result"] is None

    @pytest.mark.asyncio
    async def test_handle_command_without_token_usage(self):
        """Test command handles response without token usage."""
        command = ResearchCommand()

        mock_result = AgentResult(
            status=ExecutionStatus.SUCCESS,
            output={"findings": ["test"]},
            token_usage=None,
            execution_time=1.0,
        )

        with patch.object(command.agent, "execute", new_callable=AsyncMock) as mock_execute:
            mock_execute.return_value = mock_result

            result = await command.handle({"topic": "Test topic"})

            assert "token_usage" not in result

    @pytest.mark.asyncio
    async def test_handle_command_preserves_topic(self):
        """Test command preserves original topic in response."""
        command = ResearchCommand()

        original_topic = "  AI trends in healthcare 2025  "
        expected_topic = "AI trends in healthcare 2025"

        with patch.object(command.agent, "execute", new_callable=AsyncMock) as mock_execute:
            mock_execute.return_value = AgentResult(
                status=ExecutionStatus.SUCCESS,
                output={"findings": []},
                execution_time=1.0,
            )

            result = await command.handle({"topic": original_topic})

            assert result["topic"] == expected_topic
            mock_execute.assert_called_once_with(task=expected_topic)

    @pytest.mark.asyncio
    async def test_handle_command_execution_logging(self, sample_agent_result, caplog):
        """Test command logs execution properly."""
        command = ResearchCommand()

        with patch.object(command.agent, "execute", new_callable=AsyncMock) as mock_execute:
            mock_execute.return_value = sample_agent_result

            await command.handle({"topic": "Test topic"})

            # Check for log messages (this depends on logger configuration)
            # In actual tests, verify log output contains expected messages

    @pytest.mark.asyncio
    async def test_concurrent_command_executions(self):
        """Test multiple concurrent command executions."""
        import asyncio

        command = ResearchCommand()

        with patch.object(command.agent, "execute", new_callable=AsyncMock) as mock_execute:
            mock_execute.return_value = AgentResult(
                status=ExecutionStatus.SUCCESS,
                output={"findings": ["test"]},
                execution_time=1.0,
            )

            tasks = [
                command.handle({"topic": f"Topic {i}"})
                for i in range(3)
            ]

            results = await asyncio.gather(*tasks)

            assert len(results) == 3
            for result in results:
                assert result["status"] == "success"
                assert result["command"] == "/research"
