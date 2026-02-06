"""
Central registry for agents and skills.

This module provides a singleton registry for managing agent and skill
instances with dependency injection support.
"""

from typing import Any, Dict, Type

from src.agents.base_agent import BaseAgent


class AgentRegistry:
    """Central registry for agents and skills.

    This registry manages agent and skill classes and instances,
    implementing a singleton pattern for agent instances to ensure
    efficient resource usage and context management.

    Attributes:
        _agents: Dictionary mapping agent names to agent classes
        _skills: Dictionary mapping skill names to skill classes
        _agent_instances: Dictionary caching agent instances (singleton)
    """

    def __init__(self):
        """Initialize empty registry."""
        self._agents: Dict[str, Type[BaseAgent]] = {}
        self._skills: Dict[str, Type[Any]] = {}  # BaseSkill will be added in Phase 1.5
        self._agent_instances: Dict[str, BaseAgent] = {}

    def register_agent(self, name: str, agent_class: Type[BaseAgent]) -> None:
        """Register an agent class.

        Args:
            name: Unique agent identifier
            agent_class: Agent class (must inherit from BaseAgent)

        Raises:
            ValueError: If agent name already registered
            TypeError: If agent_class is not a BaseAgent subclass
        """
        if name in self._agents:
            raise ValueError(f"Agent '{name}' is already registered")

        if not issubclass(agent_class, BaseAgent):
            raise TypeError(
                f"Agent class must inherit from BaseAgent, got {agent_class}"
            )

        self._agents[name] = agent_class

    def register_skill(self, name: str, skill_class: Type[Any]) -> None:
        """Register a skill class.

        Args:
            name: Unique skill identifier
            skill_class: Skill class (must inherit from BaseSkill)

        Raises:
            ValueError: If skill name already registered

        Note:
            BaseSkill will be implemented in Phase 1.5
        """
        if name in self._skills:
            raise ValueError(f"Skill '{name}' is already registered")

        self._skills[name] = skill_class

    def get_agent(self, name: str, **kwargs) -> BaseAgent:
        """Get agent instance (singleton pattern).

        Returns cached instance if available, otherwise creates new instance.
        This ensures each agent type has only one instance, maintaining
        efficient resource usage and consistent context management.

        Args:
            name: Agent identifier
            **kwargs: Additional arguments passed to agent constructor
                     (only used when creating new instance)

        Returns:
            Agent instance

        Raises:
            ValueError: If agent not registered
        """
        # Return cached instance if available
        if name in self._agent_instances:
            return self._agent_instances[name]

        # Get agent class
        agent_class = self._agents.get(name)
        if not agent_class:
            raise ValueError(
                f"Agent '{name}' not registered. "
                f"Available agents: {list(self._agents.keys())}"
            )

        # Create and cache new instance
        self._agent_instances[name] = agent_class(**kwargs)
        return self._agent_instances[name]

    def get_skill(self, name: str) -> Any:
        """Get skill instance.

        Args:
            name: Skill identifier

        Returns:
            Skill instance

        Raises:
            ValueError: If skill not registered

        Note:
            BaseSkill and skill implementation will be added in Phase 1.5
        """
        skill_class = self._skills.get(name)
        if not skill_class:
            raise ValueError(
                f"Skill '{name}' not registered. "
                f"Available skills: {list(self._skills.keys())}"
            )

        # Skills receive registry reference for agent access
        return skill_class(registry=self)

    def list_agents(self) -> list[str]:
        """List all registered agent names.

        Returns:
            List of agent names
        """
        return list(self._agents.keys())

    def list_skills(self) -> list[str]:
        """List all registered skill names.

        Returns:
            List of skill names
        """
        return list(self._skills.keys())

    def clear_instances(self) -> None:
        """Clear all cached agent instances.

        This is useful for testing or when you need to reset agent state.
        """
        self._agent_instances.clear()


# Global registry instance
registry = AgentRegistry()
