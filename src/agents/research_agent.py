"""
Research Agent implementation for HypeProof Lab.

This module provides a specialized agent for web search and information gathering,
using Claude's WebSearch and WebFetch capabilities.
"""

from typing import Any, Dict, Optional

from src.agents.base_agent import BaseAgent


class ResearchAgent(BaseAgent):
    """Web search and information gathering specialist.

    This agent specializes in:
    - Web searching for recent information
    - Retrieving content from URLs
    - Identifying credible sources
    - Summarizing findings with citations
    - Flagging information requiring verification

    The agent maintains an independent context window to prevent
    contamination of the main session context.
    """

    def __init__(self):
        """Initialize Research Agent with search capabilities."""
        super().__init__(
            name="research_agent",
            system_prompt="""You are a research specialist focused on gathering accurate information.

Your responsibilities:
1. Use WebSearch to find recent, credible sources
2. Use WebFetch to retrieve full content when needed
3. Prioritize official documentation, research papers, and authoritative sources
4. Summarize findings with clear citations
5. Flag information that requires further verification

Output Format:
Your response should be structured as follows:
- **Key Findings**: Bullet points of main discoveries
- **Sources**: URLs with brief descriptions
- **Confidence Level**: Your confidence in each finding (high/medium/low)
- **Additional Research**: Areas requiring further investigation

Always cite your sources and indicate when information is uncertain.""",
            tools=["Read", "WebSearch", "WebFetch"],
        )

    async def _execute_task(
        self, task: str, context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Execute research task using Claude SDK.

        Args:
            task: Research topic or question
            context: Optional context (not used for research agent)

        Returns:
            Structured research findings
        """
        # Build comprehensive research prompt
        prompt = f"""Research the following topic and provide comprehensive findings:

Topic: {task}

Please search for:
1. Latest information and trends
2. Official sources and documentation
3. Research papers or authoritative articles
4. Key statistics and data points
5. Expert opinions and analysis

Provide structured output with:
- Key Findings (bullet points)
- Sources (URLs with descriptions)
- Confidence Level for each finding
- Areas needing additional research"""

        # Execute via Claude SDK
        # Note: In actual implementation, this would use the SDK's query method
        # For now, we'll structure the expected output format
        response = await self.client.query(prompt)

        # Parse and structure the result
        return self._parse_research_output(response)

    def _parse_research_output(self, raw_output: Any) -> Dict[str, Any]:
        """Parse research output into structured format.

        Args:
            raw_output: Raw output from Claude SDK

        Returns:
            Structured research results
        """
        # Parse the SDK response
        parsed = self._parse_response(raw_output)

        # Structure research findings
        # In a real implementation, this would extract structured data
        # from the agent's response using patterns or explicit formatting
        structured_output = {
            "findings": [],  # List of key findings
            "sources": [],  # List of source URLs with descriptions
            "confidence": "high",  # Overall confidence level
            "additional_research_needed": [],  # Areas requiring more research
            "raw_response": parsed["output"],  # Full response for reference
        }

        # If we have token usage info, include it
        if parsed.get("token_usage"):
            structured_output["token_usage"] = parsed["token_usage"]

        return structured_output
