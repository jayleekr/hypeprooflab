"""
Base Agent implementation for HypeProof Lab.

This module provides the base class for all agents, implementing
common functionality including Claude SDK integration, error handling,
and execution tracking.
"""

import time
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient

from src.core.error_handler import ErrorHandler
from src.core.logger import logger
from src.core.types import AgentResult, ExecutionStatus, TokenUsage


class BaseAgent(ABC):
    """Base class for all agents with Claude SDK integration.

    This abstract class provides:
    - Claude SDK client management
    - Independent context isolation
    - Structured error handling
    - Execution time tracking
    - Token usage monitoring
    - Logging integration

    Subclasses must implement the `_execute_task` method to define
    agent-specific execution logic.

    Attributes:
        name: Unique agent identifier
        system_prompt: System prompt defining agent behavior
        tools: List of allowed tools for this agent
        model: Claude model to use
        client: Claude SDK client instance
    """

    def __init__(
        self,
        name: str,
        system_prompt: str,
        tools: List[str],
        model: str = "claude-sonnet-4-20250514",
        options: Optional[Dict[str, Any]] = None,
    ):
        """Initialize base agent.

        Args:
            name: Agent identifier
            system_prompt: System prompt for agent behavior
            tools: List of allowed tools
            model: Claude model identifier
            options: Additional options for Claude SDK
        """
        self.name = name
        self.system_prompt = system_prompt
        self.tools = tools
        self.model = model

        # Create isolated Claude SDK client
        self.options = ClaudeAgentOptions(
            allowed_tools=tools,
            system_prompt=system_prompt,
            permission_mode="acceptEdits",
            model=model,
            **(options or {}),
        )
        self.client = ClaudeSDKClient(options=self.options)

        logger.info(
            "agent_initialized",
            agent=self.name,
            tools=self.tools,
            model=self.model,
        )

    async def execute(
        self, task: str, context: Optional[Dict[str, Any]] = None
    ) -> AgentResult:
        """Execute agent task in isolated context.

        This method provides the execution framework including:
        - Execution time tracking
        - Error handling and recovery
        - Structured logging
        - Result formatting

        Args:
            task: Task description or instruction
            context: Optional context information

        Returns:
            AgentResult with execution status and output
        """
        start_time = time.time()

        try:
            logger.info(
                "agent_execution_started",
                agent=self.name,
                task=task[:100],  # Truncate long tasks for logging
            )

            # Execute agent-specific logic
            output = await self._execute_task(task, context)

            execution_time = time.time() - start_time

            logger.info(
                "agent_execution_completed",
                agent=self.name,
                status="success",
                execution_time=execution_time,
            )

            return AgentResult(
                status=ExecutionStatus.SUCCESS,
                output=output,
                execution_time=execution_time,
            )

        except Exception as e:
            execution_time = time.time() - start_time
            return ErrorHandler.handle_exception(
                agent_name=self.name,
                task=task,
                exception=e,
                execution_time=execution_time,
            )

    @abstractmethod
    async def _execute_task(
        self, task: str, context: Optional[Dict[str, Any]]
    ) -> Any:
        """Execute agent-specific task logic.

        This method must be implemented by subclasses to define
        the actual agent behavior.

        Args:
            task: Task description or instruction
            context: Optional context information

        Returns:
            Agent output (format defined by subclass)
        """
        pass

    def _parse_response(self, response: Any) -> Dict[str, Any]:
        """Parse Claude SDK response into structured format.

        Args:
            response: Raw response from Claude SDK

        Returns:
            Structured response dictionary
        """
        # Extract result from response
        if hasattr(response, "result"):
            output = response.result
        else:
            output = str(response)

        # Extract token usage if available
        token_usage = None
        if hasattr(response, "token_usage"):
            token_usage = TokenUsage(
                input_tokens=response.token_usage.get("input_tokens", 0),
                output_tokens=response.token_usage.get("output_tokens", 0),
                total_tokens=response.token_usage.get("total_tokens", 0),
            )

        return {
            "output": output,
            "token_usage": token_usage,
        }
