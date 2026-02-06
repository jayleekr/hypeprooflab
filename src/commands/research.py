"""
Research command handler.

This module provides the /research command handler that orchestrates
the ResearchAgent to gather and summarize information on a given topic.
"""

import asyncio
import sys
from typing import Any, Dict

from src.agents.research_agent import ResearchAgent
from src.core.logger import logger


class ResearchCommand:
    """Slash command handler for /research.

    This command executes the ResearchAgent to perform web-based research
    on a specified topic and return structured findings.
    """

    def __init__(self):
        """Initialize research command with ResearchAgent instance."""
        self.agent = ResearchAgent()
        logger.info("research_command_initialized")

    async def handle(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle /research command execution.

        Args:
            args: Command arguments dictionary with 'topic' key

        Returns:
            Structured research results including:
                - command: Command name
                - topic: Research topic
                - result: Research findings
                - status: Execution status
                - execution_time: Time taken in seconds
                - token_usage: Token usage statistics (if available)

        Raises:
            ValueError: If topic is missing or empty
        """
        topic = args.get("topic", "").strip()

        if not topic:
            raise ValueError("Research topic is required")

        logger.info("research_command_started", topic=topic)

        # Execute research agent
        result = await self.agent.execute(task=topic)

        logger.info(
            "research_command_completed",
            topic=topic,
            status=result.status,
            execution_time=result.execution_time,
        )

        # Build response
        response = {
            "command": "/research",
            "topic": topic,
            "result": result.output,
            "status": result.status.value,
            "execution_time": result.execution_time,
        }

        # Include token usage if available
        if result.token_usage:
            response["token_usage"] = {
                "input_tokens": result.token_usage.input_tokens,
                "output_tokens": result.token_usage.output_tokens,
                "total_tokens": result.token_usage.total_tokens,
                "cost_estimate": result.token_usage.cost_estimate,
            }

        # Include error message if failed
        if result.error_message:
            response["error"] = result.error_message

        return response


async def main():
    """CLI entry point for /research command.

    Usage:
        python -m src.commands.research <topic>

    Example:
        python -m src.commands.research "Latest AI trends in 2025"
    """
    if len(sys.argv) < 2:
        print("Usage: /research <topic>")
        print("Example: /research 'Latest AI trends in 2025'")
        sys.exit(1)

    # Join all arguments as topic
    topic = " ".join(sys.argv[1:])

    try:
        # Execute research command
        command = ResearchCommand()
        result = await command.handle({"topic": topic})

        # Print formatted output
        print(f"\n{'='*80}")
        print(f"Research Results: {result['topic']}")
        print(f"{'='*80}\n")

        if result["status"] == "success":
            print(result["result"])
            print(f"\nExecution time: {result['execution_time']:.2f}s")

            if "token_usage" in result:
                usage = result["token_usage"]
                print(f"Tokens used: {usage['total_tokens']} "
                      f"(input: {usage['input_tokens']}, "
                      f"output: {usage['output_tokens']})")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
            sys.exit(1)

    except Exception as e:
        print(f"Error: {str(e)}")
        logger.error("research_command_failed", error=str(e))
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
