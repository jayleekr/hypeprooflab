"""
Centralized error handling for HypeProof Lab.

This module provides standardized error handling across all agents,
ensuring consistent error logging and recovery patterns.
"""

from typing import Optional

from src.core.logger import logger
from src.core.types import AgentResult, ExecutionStatus


class HypeProofError(Exception):
    """Base exception for HypeProof Lab errors."""

    pass


class AgentExecutionError(HypeProofError):
    """Exception raised when agent execution fails."""

    pass


class ConfigurationError(HypeProofError):
    """Exception raised when configuration is invalid."""

    pass


class TimeoutError(HypeProofError):
    """Exception raised when agent execution times out."""

    pass


class ErrorHandler:
    """Centralized error handling for agent executions.

    This class provides static methods for handling exceptions
    and converting them to structured AgentResult objects.
    """

    @staticmethod
    def handle_exception(
        agent_name: str,
        task: str,
        exception: Exception,
        execution_time: float = 0.0,
    ) -> AgentResult:
        """Handle agent execution exception and return structured result.

        Args:
            agent_name: Name of the agent that failed
            task: Task that was being executed
            exception: The exception that was raised
            execution_time: Time spent before failure

        Returns:
            AgentResult with error status and details
        """
        error_type = type(exception).__name__
        error_message = str(exception)

        logger.error(
            "agent_execution_failed",
            agent=agent_name,
            task=task[:100],  # Truncate long tasks
            error=error_message,
            error_type=error_type,
        )

        # Determine status based on exception type
        if isinstance(exception, TimeoutError):
            status = ExecutionStatus.TIMEOUT
        else:
            status = ExecutionStatus.ERROR

        return AgentResult(
            status=status,
            output=None,
            execution_time=execution_time,
            error_message=f"{error_type}: {error_message}",
        )

    @staticmethod
    def handle_timeout(
        agent_name: str,
        task: str,
        timeout: int,
    ) -> AgentResult:
        """Handle agent execution timeout.

        Args:
            agent_name: Name of the agent that timed out
            task: Task that was being executed
            timeout: Timeout threshold in seconds

        Returns:
            AgentResult with timeout status
        """
        logger.warning(
            "agent_execution_timeout",
            agent=agent_name,
            task=task[:100],
            timeout=timeout,
        )

        return AgentResult(
            status=ExecutionStatus.TIMEOUT,
            output=None,
            execution_time=float(timeout),
            error_message=f"Agent execution exceeded timeout of {timeout} seconds",
        )

    @staticmethod
    def is_retriable(exception: Exception) -> bool:
        """Determine if an exception is retriable.

        Args:
            exception: The exception to check

        Returns:
            True if the exception is retriable, False otherwise
        """
        # Network errors, rate limits, and transient failures are retriable
        retriable_errors = (
            "ConnectionError",
            "TimeoutError",
            "RateLimitError",
            "ServiceUnavailable",
        )

        error_type = type(exception).__name__
        return error_type in retriable_errors or "timeout" in str(exception).lower()
