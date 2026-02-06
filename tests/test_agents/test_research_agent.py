"""
Tests for ResearchAgent.

This module tests the ResearchAgent implementation including
initialization, execution, and research output parsing.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.agents.research_agent import ResearchAgent
from src.core.types import ExecutionStatus


class TestResearchAgent:
    """Test suite for ResearchAgent class."""

    def test_research_agent_initialization(self):
        """Test ResearchAgent initializes with correct configuration."""
        agent = ResearchAgent()

        assert agent.name == "research_agent"
        assert "WebSearch" in agent.tools
        assert "WebFetch" in agent.tools
        assert "Read" in agent.tools
        assert agent.model == "claude-sonnet-4-20250514"

    def test_research_agent_system_prompt(self):
        """Test ResearchAgent has appropriate system prompt."""
        agent = ResearchAgent()

        assert "research" in agent.system_prompt.lower()
        assert "websearch" in agent.system_prompt.lower()

    @pytest.mark.asyncio
    async def test_execute_research_task_success(self, mock_claude_client):
        """Test successful research task execution."""
        agent = ResearchAgent()

        # Mock the Claude SDK client
        with patch.object(agent, "client", mock_claude_client):
            result = await agent.execute(
                task="Latest AI trends", context={"focus": "2025"}
            )

            assert result.status == ExecutionStatus.SUCCESS
            assert result.output is not None
            assert result.execution_time > 0
            mock_claude_client.query.assert_called_once()

    @pytest.mark.asyncio
    async def test_execute_research_task_with_error(self):
        """Test research task execution with error handling."""
        agent = ResearchAgent()

        # Mock client to raise exception
        with patch.object(agent, "client") as mock_client:
            mock_client.query = AsyncMock(side_effect=Exception("API Error"))

            result = await agent.execute(task="Test topic")

            assert result.status == ExecutionStatus.ERROR
            assert result.error_message is not None
            assert "API Error" in result.error_message

    @pytest.mark.asyncio
    async def test_execute_empty_task(self):
        """Test execution with empty task string."""
        agent = ResearchAgent()

        with patch.object(agent, "client") as mock_client:
            mock_client.query = AsyncMock(return_value=MagicMock(result="Result"))

            result = await agent.execute(task="")

            # Should still execute, even with empty task
            assert result.status in [ExecutionStatus.SUCCESS, ExecutionStatus.ERROR]

    def test_parse_research_output_structure(self):
        """Test research output parsing returns correct structure."""
        agent = ResearchAgent()

        mock_response = MagicMock()
        mock_response.result = "Research findings..."
        mock_response.token_usage = {
            "input_tokens": 100,
            "output_tokens": 200,
            "total_tokens": 300,
        }

        output = agent._parse_research_output(mock_response)

        assert "findings" in output
        assert "sources" in output
        assert "confidence" in output
        assert "additional_research_needed" in output
        assert "raw_response" in output

    def test_parse_research_output_with_token_usage(self):
        """Test parsing includes token usage when available."""
        agent = ResearchAgent()

        mock_response = MagicMock()
        mock_response.result = "Research findings..."
        mock_response.token_usage = {
            "input_tokens": 150,
            "output_tokens": 300,
            "total_tokens": 450,
        }

        output = agent._parse_research_output(mock_response)

        assert "token_usage" in output
        assert output["token_usage"].input_tokens == 150
        assert output["token_usage"].output_tokens == 300

    def test_parse_research_output_without_token_usage(self):
        """Test parsing works without token usage data."""
        agent = ResearchAgent()

        mock_response = MagicMock()
        mock_response.result = "Research findings..."

        # Remove token_usage attribute
        del mock_response.token_usage

        output = agent._parse_research_output(mock_response)

        assert "findings" in output
        assert "sources" in output
        # token_usage key should not be present
        assert "token_usage" not in output or output["token_usage"] is None

    @pytest.mark.asyncio
    async def test_execute_task_interface(self):
        """Test _execute_task interface is correctly implemented."""
        agent = ResearchAgent()

        with patch.object(agent, "client") as mock_client:
            mock_client.query = AsyncMock(
                return_value=MagicMock(
                    result="Test result", token_usage={"total_tokens": 100}
                )
            )

            # Call the internal method directly
            output = await agent._execute_task("Test task", context=None)

            assert isinstance(output, dict)
            assert "raw_response" in output
            mock_client.query.assert_called_once()

    @pytest.mark.asyncio
    async def test_concurrent_executions(self, mock_claude_client):
        """Test agent can handle concurrent executions."""
        import asyncio

        agent = ResearchAgent()

        with patch.object(agent, "client", mock_claude_client):
            tasks = [
                agent.execute(task=f"Topic {i}", context=None) for i in range(3)
            ]

            results = await asyncio.gather(*tasks)

            assert len(results) == 3
            for result in results:
                assert result.status == ExecutionStatus.SUCCESS
                assert result.output is not None
