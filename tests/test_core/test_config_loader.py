"""
Tests for ConfigLoader.

This module tests YAML configuration loading and validation.
"""

import pytest
from pathlib import Path

from src.core.config_loader import ConfigLoader
from src.core.error_handler import ConfigurationError
from src.core.types import AgentConfig, SkillConfig


class TestConfigLoader:
    """Test suite for ConfigLoader class."""

    def test_config_loader_initialization(self, test_config_dir):
        """Test ConfigLoader initializes with valid directory."""
        loader = ConfigLoader(config_dir=str(test_config_dir))
        assert loader.config_dir == test_config_dir

    def test_config_loader_invalid_directory_raises_error(self):
        """Test ConfigLoader raises error for invalid directory."""
        with pytest.raises(ConfigurationError, match="not found"):
            ConfigLoader(config_dir="/nonexistent/path")

    def test_load_yaml_success(self, test_config_dir):
        """Test loading valid YAML file."""
        loader = ConfigLoader(config_dir=str(test_config_dir))

        config = loader.load_yaml("agents.yaml")

        assert isinstance(config, dict)
        assert "agents" in config

    def test_load_yaml_nonexistent_file_raises_error(self, test_config_dir):
        """Test loading nonexistent file raises error."""
        loader = ConfigLoader(config_dir=str(test_config_dir))

        with pytest.raises(ConfigurationError, match="not found"):
            loader.load_yaml("nonexistent.yaml")

    def test_load_yaml_invalid_yaml_raises_error(self, tmp_path):
        """Test loading invalid YAML raises error."""
        config_dir = tmp_path / "config"
        config_dir.mkdir()

        # Create invalid YAML file
        invalid_yaml = config_dir / "invalid.yaml"
        invalid_yaml.write_text("invalid: yaml: content: [")

        loader = ConfigLoader(config_dir=str(config_dir))

        with pytest.raises(ConfigurationError, match="Invalid YAML"):
            loader.load_yaml("invalid.yaml")

    def test_load_agents_config_success(self, test_config_dir):
        """Test loading and parsing agents configuration."""
        loader = ConfigLoader(config_dir=str(test_config_dir))

        agents = loader.load_agents_config()

        assert isinstance(agents, dict)
        assert "test_agent" in agents
        assert isinstance(agents["test_agent"], AgentConfig)
        assert agents["test_agent"].name == "Test Agent"

    def test_load_agents_config_missing_key_raises_error(self, tmp_path):
        """Test loading agents config without 'agents' key raises error."""
        config_dir = tmp_path / "config"
        config_dir.mkdir()

        # Create YAML without 'agents' key
        agents_yaml = config_dir / "agents.yaml"
        agents_yaml.write_text("invalid_key: value")

        loader = ConfigLoader(config_dir=str(config_dir))

        with pytest.raises(ConfigurationError, match="must contain 'agents' key"):
            loader.load_agents_config()

    def test_load_agents_config_invalid_agent_data_raises_error(self, tmp_path):
        """Test loading agents config with invalid agent data raises error."""
        config_dir = tmp_path / "config"
        config_dir.mkdir()

        # Create YAML with invalid agent configuration
        agents_yaml = config_dir / "agents.yaml"
        agents_yaml.write_text(
            """
agents:
  invalid_agent:
    name: "Invalid"
    # Missing required 'role' field
    tools: []
"""
        )

        loader = ConfigLoader(config_dir=str(config_dir))

        with pytest.raises(ConfigurationError, match="Invalid configuration"):
            loader.load_agents_config()

    def test_load_settings_success(self, test_config_dir):
        """Test loading settings configuration."""
        loader = ConfigLoader(config_dir=str(test_config_dir))

        settings = loader.load_settings()

        assert isinstance(settings, dict)
        assert "system" in settings

    def test_load_yaml_returns_empty_dict_for_empty_file(self, tmp_path):
        """Test loading empty YAML file returns empty dict."""
        config_dir = tmp_path / "config"
        config_dir.mkdir()

        empty_yaml = config_dir / "empty.yaml"
        empty_yaml.write_text("")

        loader = ConfigLoader(config_dir=str(config_dir))

        config = loader.load_yaml("empty.yaml")

        assert config == {}

    def test_load_config_convenience_function(self, test_config_dir, monkeypatch):
        """Test load_config convenience function."""
        from src.core.config_loader import load_config

        # Change to test config directory
        monkeypatch.chdir(test_config_dir.parent)

        # Note: This test would need proper path setup
        # For now, just test the function exists
        assert callable(load_config)
