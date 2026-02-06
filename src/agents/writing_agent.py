"""
Writing Agent implementation for HypeProof Lab.

This module provides a specialized agent for creating engaging content
from research and analysis, supporting multiple formats including podcast scripts,
technical articles, and documentation.
"""

import re
from typing import Any, Dict, List, Optional

from src.agents.base_agent import BaseAgent


class WritingAgent(BaseAgent):
    """Content creation and storytelling specialist.

    This agent specializes in:
    - Creating engaging podcast scripts
    - Writing technical articles and blog posts
    - Generating professional documentation
    - Adapting tone and style for different audiences
    - Structuring content with clear narrative flow
    - Formatting content for various output formats

    The agent maintains an independent context window to prevent
    contamination of the main session context.
    """

    def __init__(self):
        """Initialize Writing Agent with content creation capabilities."""
        super().__init__(
            name="writing_agent",
            system_prompt="""You are a professional content writer and storyteller specializing in creating engaging, well-structured content.

Your responsibilities:
1. Create compelling narratives from research and analysis data
2. Adapt tone and style based on target audience (technical, general, executive)
3. Structure content with clear introduction, body, and conclusion
4. Use engaging language that maintains reader/listener interest
5. Format content appropriately for the target medium (podcast, article, docs)

Content Formats:
- **Podcast Scripts**: Conversational tone, natural speech patterns, clear host cues
- **Technical Articles**: Professional tone, clear explanations, code examples where relevant
- **Documentation**: Clear, concise, structured with headings and examples

Quality Standards:
- Clear narrative arc with engaging introduction
- Well-organized sections with logical flow
- Appropriate technical depth for target audience
- Engaging language that maintains interest
- Professional polish with attention to detail

Output Structure:
Your response should include:
- **Introduction**: Engaging hook and context setting
- **Main Content**: Well-organized body with clear sections
- **Conclusion**: Strong closing with key takeaways
- **Metadata**: Word count, tone, target audience

Always maintain professional quality while adapting to the specific format and audience needs.""",
            tools=["Write", "Edit"],
        )

    async def _execute_task(
        self, task: str, context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Execute writing task using Claude SDK.

        Args:
            task: Writing instruction (e.g., "Create podcast script about AI trends")
            context: Optional context with analysis_data, tone, audience, format

        Returns:
            Structured writing output with content and metadata
        """
        # Extract context parameters
        analysis_data = context.get("analysis_data") if context else None
        tone = context.get("tone", "professional") if context else "professional"
        audience = context.get("audience", "technical") if context else "technical"
        content_format = context.get("format", "article") if context else "article"

        # Build comprehensive writing prompt
        prompt = self._build_writing_prompt(
            task=task,
            analysis_data=analysis_data,
            tone=tone,
            audience=audience,
            content_format=content_format,
        )

        # Execute via Claude SDK
        response = await self.client.query(prompt)

        # Parse and structure the result
        return self._parse_writing_response(
            response=response,
            content_format=content_format,
            tone=tone,
            audience=audience,
        )

    def _build_writing_prompt(
        self,
        task: str,
        analysis_data: Any,
        tone: str = "professional",
        audience: str = "technical",
        content_format: str = "article",
    ) -> str:
        """Build writing prompt for Claude SDK.

        Args:
            task: User's writing request
            analysis_data: Optional analysis data to base content on
            tone: Content tone (professional, casual, technical, engaging)
            audience: Target audience (technical, general, executive)
            content_format: Output format (podcast_script, article, documentation)

        Returns:
            Formatted prompt string
        """
        prompt_parts = [
            "Create engaging content based on the following requirements:",
            "",
            f"Task: {task}",
            f"Format: {content_format}",
            f"Tone: {tone}",
            f"Target Audience: {audience}",
        ]

        if analysis_data:
            prompt_parts.extend([
                "",
                "Source Material (Analysis Data):",
                str(analysis_data),
            ])

        # Add format-specific instructions
        format_instructions = self._get_format_instructions(content_format)
        if format_instructions:
            prompt_parts.extend(["", "Format-Specific Requirements:", format_instructions])

        # Add quality requirements
        prompt_parts.extend([
            "",
            "Content Requirements:",
            "1. Create a compelling introduction that hooks the reader/listener",
            "2. Organize content into clear, logical sections",
            "3. Maintain consistent tone throughout",
            f"4. Adjust technical depth for {audience} audience",
            "5. Include a strong conclusion with key takeaways",
            "6. Ensure content is engaging and maintains interest",
            "",
            "Please structure your response with clear sections:",
            "- Introduction",
            "- Main Content (organized into subsections)",
            "- Conclusion",
        ])

        return "\n".join(prompt_parts)

    def _get_format_instructions(self, content_format: str) -> str:
        """Get format-specific writing instructions.

        Args:
            content_format: Target format (podcast_script, article, documentation)

        Returns:
            Format-specific instructions
        """
        format_instructions = {
            "podcast_script": """- Use conversational, natural speech patterns
- Include host cues and transitions in [brackets]
- Break complex ideas into digestible segments
- Use rhetorical questions to engage listeners
- Include clear section transitions
- Aim for 1500-2000 words (10-15 minutes spoken)""",
            "article": """- Use professional but engaging tone
- Include clear headings and subheadings
- Use bullet points for key takeaways
- Include relevant examples or case studies
- Aim for 1200-1800 words
- Use active voice and clear language""",
            "documentation": """- Use clear, concise language
- Include step-by-step instructions where applicable
- Use numbered lists for procedures
- Include examples for complex concepts
- Use consistent formatting
- Aim for clarity over creativity""",
        }

        return format_instructions.get(content_format, "")

    def _parse_writing_response(
        self,
        response: Any,
        content_format: str,
        tone: str,
        audience: str,
    ) -> Dict[str, Any]:
        """Parse writing response into structured format.

        Args:
            response: Raw output from Claude SDK
            content_format: Content format used
            tone: Tone applied
            audience: Target audience

        Returns:
            Structured writing results with content and metadata
        """
        # Parse the SDK response
        parsed = self._parse_response(response)
        content = parsed["output"]

        # Extract sections from content
        sections = self._extract_sections(content)

        # Calculate metadata
        word_count = len(content.split())
        section_names = list(sections.keys())

        # Structure writing output
        structured_output = {
            "status": "success",
            "content": content,
            "format": content_format,
            "metadata": {
                "word_count": word_count,
                "tone": tone,
                "audience": audience,
                "sections": section_names,
            },
            "sections": sections,
            "raw_response": content,
        }

        # Include token usage if available
        if parsed.get("token_usage"):
            structured_output["token_usage"] = parsed["token_usage"]

        return structured_output

    def _extract_sections(self, content: str) -> Dict[str, str]:
        """Extract sections from content based on headings.

        Args:
            content: Full content text

        Returns:
            Dictionary mapping section names to content
        """
        sections = {}

        # Try to extract sections based on common patterns
        # Look for markdown headings or bold section labels
        section_pattern = r'(?:^|\n)(?:\*\*|##\s*)([A-Z][^:\n]+)(?:\*\*)?:?\s*\n((?:(?!\n(?:\*\*|##)).)*)'

        matches = re.finditer(section_pattern, content, re.MULTILINE | re.DOTALL)

        for match in matches:
            section_name = match.group(1).strip()
            section_content = match.group(2).strip()
            sections[section_name.lower().replace(" ", "_")] = section_content

        # If no sections found, create default structure
        if not sections:
            # Split content into roughly equal parts
            content_lines = content.split("\n\n")
            third = len(content_lines) // 3

            sections = {
                "introduction": "\n\n".join(content_lines[:third]),
                "main_content": "\n\n".join(content_lines[third:third*2]),
                "conclusion": "\n\n".join(content_lines[third*2:]),
            }

        return sections

    def _format_for_podcast(self, content: str) -> str:
        """Format content as podcast script with host cues.

        Args:
            content: Raw content to format

        Returns:
            Podcast-formatted content
        """
        # Add podcast-specific formatting
        formatted = f"""[PODCAST SCRIPT]

[Host Introduction]
{content}

[Closing]
Thanks for listening! We'll be back next time with more insights.
"""
        return formatted

    def _format_for_article(self, content: str) -> str:
        """Format content as technical article with proper structure.

        Args:
            content: Raw content to format

        Returns:
            Article-formatted content
        """
        # Add article-specific formatting
        # In a real implementation, this would add proper headings,
        # format code blocks, add metadata, etc.
        return content

    def calculate_reading_time(self, word_count: int) -> int:
        """Calculate estimated reading time in minutes.

        Args:
            word_count: Number of words in content

        Returns:
            Estimated reading time in minutes (assuming 200 words/minute)
        """
        words_per_minute = 200
        return max(1, round(word_count / words_per_minute))

    def calculate_speaking_time(self, word_count: int) -> int:
        """Calculate estimated speaking time in minutes for podcast.

        Args:
            word_count: Number of words in content

        Returns:
            Estimated speaking time in minutes (assuming 150 words/minute)
        """
        words_per_minute = 150
        return max(1, round(word_count / words_per_minute))
