"""
Configuration loader for HypeProof Lab.

This module handles loading and validation of YAML configuration files
for agents, skills, and workflows.
"""

import os
from pathlib import Path
from typing import Any, Dict

import yaml
from dotenv import load_dotenv

from src.core.error_handler import ConfigurationError
from src.core.logger import logger
from src.core.types import AgentConfig, SkillConfig

# Load environment variables
load_dotenv()


class ConfigLoader:
    """Configuration loader for YAML files."""

    def __init__(self, config_dir: str = "config"):
        """Initialize configuration loader.

        Args:
            config_dir: Directory containing configuration files
        """
        self.config_dir = Path(config_dir)
        if not self.config_dir.exists():
            raise ConfigurationError(
                f"Configuration directory not found: {config_dir}"
            )

    def load_yaml(self, filename: str) -> Dict[str, Any]:
        """Load a YAML configuration file.

        Args:
            filename: Name of the YAML file to load

        Returns:
            Parsed YAML content as dictionary

        Raises:
            ConfigurationError: If file not found or invalid YAML
        """
        filepath = self.config_dir / filename

        if not filepath.exists():
            raise ConfigurationError(f"Configuration file not found: {filepath}")

        try:
            with open(filepath, "r") as f:
                config = yaml.safe_load(f)

            logger.info(
                "configuration_loaded",
                filename=filename,
                keys=list(config.keys()) if config else [],
            )

            return config or {}

        except yaml.YAMLError as e:
            raise ConfigurationError(
                f"Invalid YAML in {filename}: {str(e)}"
            ) from e

    def load_agents_config(self) -> Dict[str, AgentConfig]:
        """Load and validate agents configuration.

        Returns:
            Dictionary of agent name to AgentConfig

        Raises:
            ConfigurationError: If configuration is invalid
        """
        config = self.load_yaml("agents.yaml")

        if "agents" not in config:
            raise ConfigurationError("agents.yaml must contain 'agents' key")

        agents = {}
        for agent_name, agent_data in config["agents"].items():
            try:
                agents[agent_name] = AgentConfig(**agent_data)
            except Exception as e:
                raise ConfigurationError(
                    f"Invalid configuration for agent '{agent_name}': {str(e)}"
                ) from e

        logger.info(
            "agents_configuration_loaded",
            agent_count=len(agents),
            agents=list(agents.keys()),
        )

        return agents

    def load_skills_config(self) -> Dict[str, SkillConfig]:
        """Load and validate skills configuration.

        Returns:
            Dictionary of skill name to SkillConfig

        Raises:
            ConfigurationError: If configuration is invalid
        """
        config = self.load_yaml("skills.yaml")

        if "skills" not in config:
            raise ConfigurationError("skills.yaml must contain 'skills' key")

        skills = {}
        for skill_name, skill_data in config["skills"].items():
            try:
                skills[skill_name] = SkillConfig(**skill_data)
            except Exception as e:
                raise ConfigurationError(
                    f"Invalid configuration for skill '{skill_name}': {str(e)}"
                ) from e

        logger.info(
            "skills_configuration_loaded",
            skill_count=len(skills),
            skills=list(skills.keys()),
        )

        return skills

    def load_settings(self) -> Dict[str, Any]:
        """Load general settings configuration.

        Returns:
            Settings dictionary

        Raises:
            ConfigurationError: If configuration is invalid
        """
        return self.load_yaml("settings.yaml")


def load_config(filename: str) -> Dict[str, Any]:
    """Convenience function to load a configuration file.

    Args:
        filename: Name of the YAML file to load

    Returns:
        Parsed YAML content as dictionary
    """
    loader = ConfigLoader()
    return loader.load_yaml(filename)
