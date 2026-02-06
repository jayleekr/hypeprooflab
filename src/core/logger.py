"""
Structured logging system for HypeProof Lab.

This module provides structured JSON logging with automatic API key scrubbing
and contextual information for debugging and monitoring.
"""

import logging
import re
from typing import Any

import structlog


# API key patterns to scrub from logs
API_KEY_PATTERNS = [
    re.compile(r"sk-ant-[a-zA-Z0-9-]+"),  # Anthropic API keys
    re.compile(r"Bearer [a-zA-Z0-9_\-\.]+"),  # Bearer tokens
    re.compile(r'"api_key"\s*:\s*"[^"]+"'),  # JSON api_key fields
]


def scrub_sensitive_data(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
    """Scrub sensitive data like API keys from log messages.

    This is a structlog processor that removes sensitive information from logs.

    Args:
        logger: Logger instance (unused but required by structlog)
        method_name: Logging method name (unused but required by structlog)
        event_dict: Log event dictionary

    Returns:
        Scrubbed event dictionary
    """
    if "event" in event_dict:
        event_str = str(event_dict["event"])
        for pattern in API_KEY_PATTERNS:
            event_str = pattern.sub("[REDACTED]", event_str)
        event_dict["event"] = event_str

    # Scrub all string values in the event dict
    for key, value in event_dict.items():
        if isinstance(value, str):
            for pattern in API_KEY_PATTERNS:
                value = pattern.sub("[REDACTED]", value)
            event_dict[key] = value

    return event_dict


def setup_logger(level: str = "INFO") -> Any:
    """Setup structured logging with JSON output.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)

    Returns:
        Configured structlog logger
    """
    log_level = getattr(logging, level.upper(), logging.INFO)

    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            scrub_sensitive_data,  # Custom scrubber
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Configure root logger
    logging.basicConfig(
        format="%(message)s",
        level=log_level,
    )

    return structlog.get_logger()


# Global logger instance
logger = setup_logger()
