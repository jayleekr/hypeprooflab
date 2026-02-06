"""
Core type definitions for HypeProof Lab Agent Orchestration System.

This module defines the core data models used throughout the system,
including agent results, execution status, and token usage tracking.
"""

from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class ExecutionStatus(str, Enum):
    """Agent execution status enumeration."""

    SUCCESS = "success"
    ERROR = "error"
    TIMEOUT = "timeout"


class TokenUsage(BaseModel):
    """Token usage statistics for an agent execution."""

    input_tokens: int = Field(..., description="Number of input tokens")
    output_tokens: int = Field(..., description="Number of output tokens")
    total_tokens: int = Field(..., description="Total tokens used")
    cost_estimate: float = Field(
        default=0.0, description="Estimated cost based on pricing"
    )

    def __init__(self, **data):
        """Calculate total_tokens if not provided."""
        if "total_tokens" not in data:
            data["total_tokens"] = data.get("input_tokens", 0) + data.get(
                "output_tokens", 0
            )
        super().__init__(**data)


class AgentResult(BaseModel):
    """Structured agent execution result.

    This model captures the complete result of an agent execution,
    including status, output, token usage, execution time, and any errors.

    Attributes:
        status: Execution status (success, error, timeout)
        output: Agent output (can be any type - text, dict, list, etc.)
        token_usage: Optional token usage statistics
        execution_time: Execution time in seconds
        error_message: Optional error message if execution failed
    """

    status: ExecutionStatus = Field(..., description="Execution status")
    output: Any = Field(None, description="Agent output")
    token_usage: Optional[TokenUsage] = Field(
        None, description="Token usage statistics"
    )
    execution_time: float = Field(..., description="Execution time in seconds")
    error_message: Optional[str] = Field(
        None, description="Error message if failed"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "success",
                    "output": {
                        "findings": ["Finding 1", "Finding 2"],
                        "sources": ["url1", "url2"],
                    },
                    "token_usage": {
                        "input_tokens": 1000,
                        "output_tokens": 2000,
                        "total_tokens": 3000,
                    },
                    "execution_time": 15.3,
                    "error_message": None,
                }
            ]
        }
    }


class AgentConfig(BaseModel):
    """Agent configuration from YAML."""

    name: str = Field(..., description="Agent display name")
    role: str = Field(..., description="Agent role description")
    tools: list[str] = Field(default_factory=list, description="Available tools")
    max_retries: int = Field(default=3, description="Maximum retry attempts")
    timeout: int = Field(default=300, description="Timeout in seconds")
    model: str = Field(
        default="claude-sonnet-4-20250514", description="Claude model"
    )


class SkillConfig(BaseModel):
    """Skill configuration from YAML."""

    name: str = Field(..., description="Skill name")
    description: str = Field(..., description="Skill description")
    agents: list[str] = Field(..., description="Required agents")
    parallel: bool = Field(default=False, description="Enable parallel execution")
    quality_threshold: float = Field(
        default=0.8, description="Quality threshold"
    )
