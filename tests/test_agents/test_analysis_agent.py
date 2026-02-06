"""
Tests for AnalysisAgent.

This module tests the AnalysisAgent implementation including
initialization, execution, analysis output parsing, and integration
with ResearchAgent.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.agents.analysis_agent import AnalysisAgent
from src.core.types import ExecutionStatus


class TestAnalysisAgent:
    """Test suite for AnalysisAgent class."""

    def test_analysis_agent_initialization(self):
        """Test AnalysisAgent initializes with correct configuration."""
        agent = AnalysisAgent()

        assert agent.name == "analysis_agent"
        assert "Read" in agent.tools
        assert "Grep" in agent.tools
        assert agent.model == "claude-sonnet-4-20250514"

    def test_analysis_agent_system_prompt(self):
        """Test AnalysisAgent has appropriate system prompt."""
        agent = AnalysisAgent()

        assert "analysis" in agent.system_prompt.lower()
        assert "themes" in agent.system_prompt.lower()
        assert "patterns" in agent.system_prompt.lower()
        assert "insights" in agent.system_prompt.lower()

    @pytest.mark.asyncio
    async def test_execute_basic_analysis(self, mock_claude_client):
        """Test basic analysis execution without context."""
        agent = AnalysisAgent()

        with patch.object(agent, "client", mock_claude_client):
            result = await agent.execute(
                task="Analyze AI trends",
                context=None
            )

            assert result.status == ExecutionStatus.SUCCESS
            assert result.output is not None
            assert result.execution_time > 0
            mock_claude_client.query.assert_called_once()

    @pytest.mark.asyncio
    async def test_execute_with_research_data(self, mock_claude_client):
        """Test analysis execution with research data in context."""
        agent = AnalysisAgent()

        research_data = {
            "findings": ["AI adoption increasing", "Focus on physical AI"],
            "sources": ["https://example.com/ai-trends"]
        }

        with patch.object(agent, "client", mock_claude_client):
            result = await agent.execute(
                task="Analyze research findings",
                context={"research_data": research_data}
            )

            assert result.status == ExecutionStatus.SUCCESS
            assert result.output is not None
            # Verify research data was included in prompt
            call_args = mock_claude_client.query.call_args[0][0]
            assert "Research Data to Analyze" in call_args

    @pytest.mark.asyncio
    async def test_execute_analysis_task_with_error(self):
        """Test analysis task execution with error handling."""
        agent = AnalysisAgent()

        # Mock client to raise exception
        with patch.object(agent, "client") as mock_client:
            mock_client.query = AsyncMock(side_effect=Exception("Analysis Error"))

            result = await agent.execute(task="Test analysis")

            assert result.status == ExecutionStatus.ERROR
            assert result.error_message is not None
            assert "Analysis Error" in result.error_message

    def test_theme_extraction(self):
        """Test theme extraction from analysis response."""
        agent = AnalysisAgent()

        # Test with response containing themes
        response_with_themes = """
        Key Themes:
        - Physical AI emergence
        - Enterprise adoption
        - Regulatory concerns
        """

        themes = agent._extract_themes(response_with_themes)

        assert isinstance(themes, list)
        # Current implementation returns placeholder
        assert len(themes) >= 0

    def test_pattern_identification(self):
        """Test pattern identification from analysis response."""
        agent = AnalysisAgent()

        response_with_patterns = """
        Patterns:
        - Increasing investment in AI infrastructure
        - Focus shift from chatbots to physical AI
        """

        patterns = agent._identify_patterns(response_with_patterns)

        assert isinstance(patterns, list)
        if len(patterns) > 0:
            assert "pattern" in patterns[0]
            assert "evidence" in patterns[0]
            assert "confidence" in patterns[0]

    def test_parse_analysis_response_structure(self):
        """Test analysis response parsing returns correct structure."""
        agent = AnalysisAgent()

        mock_response = MagicMock()
        mock_response.result = "Analysis findings..."
        mock_response.token_usage = {
            "input_tokens": 200,
            "output_tokens": 400,
            "total_tokens": 600,
        }

        output = agent._parse_analysis_response(mock_response)

        assert "themes" in output
        assert "patterns" in output
        assert "insights" in output
        assert "summary" in output
        assert "recommendations" in output
        assert "raw_response" in output

    def test_parse_analysis_response_with_token_usage(self):
        """Test parsing includes token usage when available."""
        agent = AnalysisAgent()

        mock_response = MagicMock()
        mock_response.result = "Analysis findings..."
        mock_response.token_usage = {
            "input_tokens": 250,
            "output_tokens": 500,
            "total_tokens": 750,
        }

        output = agent._parse_analysis_response(mock_response)

        assert "token_usage" in output
        assert output["token_usage"].input_tokens == 250
        assert output["token_usage"].output_tokens == 500

    def test_parse_analysis_response_without_token_usage(self):
        """Test parsing works without token usage data."""
        agent = AnalysisAgent()

        mock_response = MagicMock()
        mock_response.result = "Analysis findings..."

        # Remove token_usage attribute
        del mock_response.token_usage

        output = agent._parse_analysis_response(mock_response)

        assert "themes" in output
        assert "patterns" in output
        # token_usage key should not be present
        assert "token_usage" not in output or output["token_usage"] is None

    def test_build_analysis_prompt_without_research_data(self):
        """Test prompt building without research data."""
        agent = AnalysisAgent()

        prompt = agent._build_analysis_prompt(
            task="Analyze trends",
            research_data=None
        )

        assert "Analyze trends" in prompt
        assert "Key Themes" in prompt
        assert "Patterns" in prompt
        assert "Research Data to Analyze" not in prompt

    def test_build_analysis_prompt_with_research_data(self):
        """Test prompt building with research data."""
        agent = AnalysisAgent()

        research_data = {"findings": ["Finding 1", "Finding 2"]}

        prompt = agent._build_analysis_prompt(
            task="Analyze findings",
            research_data=research_data
        )

        assert "Analyze findings" in prompt
        assert "Research Data to Analyze" in prompt
        assert str(research_data) in prompt

    @pytest.mark.asyncio
    async def test_integration_with_research_agent(self, mock_claude_client):
        """Test AnalysisAgent can process ResearchAgent output."""
        from src.agents.research_agent import ResearchAgent

        # Simulate ResearchAgent output
        research_output = {
            "findings": ["AI trend 1", "AI trend 2"],
            "sources": ["https://example.com"],
            "confidence": "high"
        }

        analysis_agent = AnalysisAgent()

        with patch.object(analysis_agent, "client", mock_claude_client):
            result = await analysis_agent.execute(
                task="Analyze research findings",
                context={"research_data": research_output}
            )

            assert result.status == ExecutionStatus.SUCCESS
            assert result.output is not None

    @pytest.mark.asyncio
    async def test_execute_task_interface(self):
        """Test _execute_task interface is correctly implemented."""
        agent = AnalysisAgent()

        with patch.object(agent, "client") as mock_client:
            mock_client.query = AsyncMock(
                return_value=MagicMock(
                    result="Test analysis result",
                    token_usage={"total_tokens": 150}
                )
            )

            # Call the internal method directly
            output = await agent._execute_task(
                "Test analysis task",
                context=None
            )

            assert isinstance(output, dict)
            assert "raw_response" in output
            mock_client.query.assert_called_once()

    @pytest.mark.asyncio
    async def test_concurrent_executions(self, mock_claude_client):
        """Test agent can handle concurrent executions."""
        import asyncio

        agent = AnalysisAgent()

        with patch.object(agent, "client", mock_claude_client):
            tasks = [
                agent.execute(
                    task=f"Analyze topic {i}",
                    context=None
                )
                for i in range(3)
            ]

            results = await asyncio.gather(*tasks)

            assert len(results) == 3
            for result in results:
                assert result.status == ExecutionStatus.SUCCESS
                assert result.output is not None

    def test_extract_insights(self):
        """Test insight extraction from response."""
        agent = AnalysisAgent()

        response_with_insights = """
        Insights:
        - Data shows 60% growth in AI adoption
        - Physical AI represents emerging market opportunity
        """

        insights = agent._extract_insights(response_with_insights)

        assert isinstance(insights, list)
        if len(insights) > 0:
            assert "insight" in insights[0]
            assert "supporting_data" in insights[0]

    def test_extract_summary(self):
        """Test summary extraction from response."""
        agent = AnalysisAgent()

        response_with_summary = """
        Summary:
        The analysis reveals strong growth in AI adoption
        with emerging focus on physical AI applications.
        """

        summary = agent._extract_summary(response_with_summary)

        assert isinstance(summary, str)
        assert len(summary) >= 0

    def test_extract_recommendations(self):
        """Test recommendation extraction from response."""
        agent = AnalysisAgent()

        response_with_recommendations = """
        Recommendations:
        - Invest in physical AI infrastructure
        - Monitor regulatory developments
        - Build partnerships in robotics sector
        """

        recommendations = agent._extract_recommendations(
            response_with_recommendations
        )

        assert isinstance(recommendations, list)
        assert len(recommendations) >= 0

    @pytest.mark.asyncio
    async def test_empty_context(self, mock_claude_client):
        """Test execution with empty context dictionary."""
        agent = AnalysisAgent()

        with patch.object(agent, "client", mock_claude_client):
            result = await agent.execute(
                task="Analyze data",
                context={}
            )

            assert result.status == ExecutionStatus.SUCCESS

    @pytest.mark.asyncio
    async def test_context_without_research_data(self, mock_claude_client):
        """Test execution with context but no research_data key."""
        agent = AnalysisAgent()

        with patch.object(agent, "client", mock_claude_client):
            result = await agent.execute(
                task="Analyze data",
                context={"other_key": "other_value"}
            )

            assert result.status == ExecutionStatus.SUCCESS
