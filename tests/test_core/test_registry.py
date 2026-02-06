"""
Tests for AgentRegistry.

This module tests the central registry for agents and skills,
including registration, retrieval, and singleton patterns.
"""

import pytest

from src.agents.base_agent import BaseAgent
from src.agents.research_agent import ResearchAgent
from src.core.registry import AgentRegistry


class MockAgent(BaseAgent):
    """Mock agent for testing purposes."""

    def __init__(self, name="mock_agent", **kwargs):
        super().__init__(
            name=name,
            system_prompt="Mock agent for testing",
            tools=["Read"],
            model="claude-sonnet-4-20250514",
        )

    async def _execute_task(self, task, context=None):
        """Mock implementation."""
        return {"mock": "result"}


class TestAgentRegistry:
    """Test suite for AgentRegistry class."""

    def test_registry_initialization(self, agent_registry):
        """Test registry initializes with empty state."""
        assert len(agent_registry._agents) == 0
        assert len(agent_registry._skills) == 0
        assert len(agent_registry._agent_instances) == 0

    def test_register_agent_success(self, agent_registry):
        """Test successful agent registration."""
        agent_registry.register_agent("mock_agent", MockAgent)

        assert "mock_agent" in agent_registry._agents
        assert agent_registry._agents["mock_agent"] == MockAgent

    def test_register_agent_duplicate_raises_error(self, agent_registry):
        """Test registering duplicate agent name raises ValueError."""
        agent_registry.register_agent("mock_agent", MockAgent)

        with pytest.raises(ValueError, match="already registered"):
            agent_registry.register_agent("mock_agent", MockAgent)

    def test_register_agent_invalid_type_raises_error(self, agent_registry):
        """Test registering non-BaseAgent class raises TypeError."""

        class NotAnAgent:
            pass

        with pytest.raises(TypeError, match="must inherit from BaseAgent"):
            agent_registry.register_agent("invalid", NotAnAgent)

    def test_get_agent_creates_instance(self, agent_registry):
        """Test get_agent creates and caches agent instance."""
        agent_registry.register_agent("mock_agent", MockAgent)

        agent = agent_registry.get_agent("mock_agent")

        assert isinstance(agent, MockAgent)
        assert agent.name == "mock_agent"
        assert "mock_agent" in agent_registry._agent_instances

    def test_get_agent_returns_singleton(self, agent_registry):
        """Test get_agent returns same instance (singleton pattern)."""
        agent_registry.register_agent("mock_agent", MockAgent)

        agent1 = agent_registry.get_agent("mock_agent")
        agent2 = agent_registry.get_agent("mock_agent")

        assert agent1 is agent2  # Same instance

    def test_get_agent_not_registered_raises_error(self, agent_registry):
        """Test getting unregistered agent raises ValueError."""
        with pytest.raises(ValueError, match="not registered"):
            agent_registry.get_agent("nonexistent")

    def test_list_agents(self, agent_registry):
        """Test listing registered agents."""
        agent_registry.register_agent("mock_agent_1", MockAgent)
        agent_registry.register_agent("mock_agent_2", MockAgent)

        agents = agent_registry.list_agents()

        assert len(agents) == 2
        assert "mock_agent_1" in agents
        assert "mock_agent_2" in agents

    def test_list_skills(self, agent_registry):
        """Test listing registered skills."""
        # Skills not implemented in Phase 1, should return empty list
        skills = agent_registry.list_skills()
        assert skills == []

    def test_clear_instances(self, agent_registry):
        """Test clearing cached agent instances."""
        agent_registry.register_agent("mock_agent", MockAgent)
        agent_registry.get_agent("mock_agent")

        assert len(agent_registry._agent_instances) == 1

        agent_registry.clear_instances()

        assert len(agent_registry._agent_instances) == 0
        assert len(agent_registry._agents) == 1  # Registration preserved

    def test_register_real_agent(self, agent_registry):
        """Test registering real ResearchAgent."""
        agent_registry.register_agent("research_agent", ResearchAgent)

        agent = agent_registry.get_agent("research_agent")

        assert isinstance(agent, ResearchAgent)
        assert agent.name == "research_agent"
        assert "WebSearch" in agent.tools
        assert "WebFetch" in agent.tools
