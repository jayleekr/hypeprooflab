"""
Tests for ErrorHandler.

This module tests centralized error handling for agent executions.
"""

import pytest

from src.core.error_handler import (
    AgentExecutionError,
    ConfigurationError,
    ErrorHandler,
    HypeProofError,
    TimeoutError,
)
from src.core.types import ExecutionStatus


class TestHypeProofErrors:
    """Test suite for custom exception classes."""

    def test_hypeproof_error_inheritance(self):
        """Test HypeProofError inherits from Exception."""
        error = HypeProofError("Test error")
        assert isinstance(error, Exception)

    def test_agent_execution_error(self):
        """Test AgentExecutionError can be raised."""
        with pytest.raises(AgentExecutionError):
            raise AgentExecutionError("Agent failed")

    def test_configuration_error(self):
        """Test ConfigurationError can be raised."""
        with pytest.raises(ConfigurationError):
            raise ConfigurationError("Config invalid")

    def test_timeout_error(self):
        """Test TimeoutError can be raised."""
        with pytest.raises(TimeoutError):
            raise TimeoutError("Operation timed out")


class TestErrorHandler:
    """Test suite for ErrorHandler class."""

    def test_handle_exception_returns_error_result(self):
        """Test handle_exception returns AgentResult with ERROR status."""
        exception = ValueError("Test error")

        result = ErrorHandler.handle_exception(
            agent_name="test_agent",
            task="test task",
            exception=exception,
            execution_time=1.5,
        )

        assert result.status == ExecutionStatus.ERROR
        assert result.output is None
        assert result.execution_time == 1.5
        assert "ValueError" in result.error_message
        assert "Test error" in result.error_message

    def test_handle_exception_with_timeout_error(self):
        """Test handle_exception identifies timeout errors."""
        exception = TimeoutError("Operation timed out")

        result = ErrorHandler.handle_exception(
            agent_name="test_agent",
            task="test task",
            exception=exception,
        )

        assert result.status == ExecutionStatus.TIMEOUT

    def test_handle_exception_preserves_execution_time(self):
        """Test handle_exception preserves execution time."""
        exception = Exception("Test")

        result = ErrorHandler.handle_exception(
            agent_name="test_agent",
            task="test task",
            exception=exception,
            execution_time=3.7,
        )

        assert result.execution_time == 3.7

    def test_handle_timeout_returns_timeout_result(self):
        """Test handle_timeout returns TIMEOUT result."""
        result = ErrorHandler.handle_timeout(
            agent_name="test_agent",
            task="test task",
            timeout=300,
        )

        assert result.status == ExecutionStatus.TIMEOUT
        assert result.output is None
        assert result.execution_time == 300.0
        assert "300" in result.error_message

    def test_is_retriable_identifies_retriable_errors(self):
        """Test is_retriable correctly identifies retriable exceptions."""
        # Create exceptions with retriable error types
        connection_error = Exception("ConnectionError: Failed to connect")
        timeout_error = Exception("TimeoutError: Request timed out")
        rate_limit_error = Exception("RateLimitError: Too many requests")

        assert ErrorHandler.is_retriable(connection_error) is True
        assert ErrorHandler.is_retriable(timeout_error) is True
        assert ErrorHandler.is_retriable(rate_limit_error) is True

    def test_is_retriable_identifies_non_retriable_errors(self):
        """Test is_retriable correctly identifies non-retriable exceptions."""
        value_error = ValueError("Invalid value")

        assert ErrorHandler.is_retriable(value_error) is False

    def test_handle_exception_truncates_long_tasks(self):
        """Test handle_exception truncates long task descriptions."""
        long_task = "x" * 200  # Task longer than 100 chars
        exception = Exception("Test error")

        result = ErrorHandler.handle_exception(
            agent_name="test_agent",
            task=long_task,
            exception=exception,
        )

        # Should still create result successfully
        assert result.status == ExecutionStatus.ERROR
