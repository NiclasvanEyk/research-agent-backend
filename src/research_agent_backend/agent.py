import asyncio
from collections.abc import AsyncGenerator
from typing import Protocol

from pydantic_ai import Agent, BinaryContent
from pydantic_ai.capabilities import WebSearch

from research_agent_backend.sources import ResearchSources


class ResearchAgent(Protocol):
    def research(self, request: str) -> AsyncGenerator[str]:
        pass


class FakeResearchAgent(ResearchAgent):
    """
    A fake implementation that can be used to test the API / frontend without an LLM key.
    """

    def __init__(
        self,
        parts: list[str],
        pause: float = 1,
    ) -> None:
        if len(parts) <= 0:
            raise ValueError("parts must not be empty")
        self._parts = parts
        if pause < 0:
            raise ValueError("pause must be positive")
        self._pause = pause

    async def research(self, request: str) -> AsyncGenerator[str]:
        for part in [
            f"Surely I can handle your request ({request})",
            "let me think...",
            *self._parts,
        ]:
            yield f"{part} "
            await asyncio.sleep(self._pause)


class LlmResearchAgent(ResearchAgent):
    def __init__(
        self,
        model_name: str,
        sources: ResearchSources,
    ) -> None:
        agent = Agent(
            model_name,
            instructions=(
                "You are a research associate. Help the user to fulfill their research requests. "
                "Be thorough and consult web searches or user-uploaded files when appropriate."
            ),
            capabilities=[WebSearch(local=True)],
        )

        @agent.tool_plain
        async def list_user_files() -> list[str]:
            """List the names of user uploaded files in our storage."""
            return await sources.list_sources()

        @agent.tool_plain
        async def read_user_file(name: str) -> BinaryContent:
            """Read the contents of a user uploaded file by its name."""
            source_content = await sources.read_source_content(name)
            return BinaryContent(
                data=source_content.content,
                media_type=source_content.mime_type,
                identifier=name,
            )

        self._agent = agent

    async def research(self, request: str) -> AsyncGenerator[str]:
        async with self._agent.run_stream(request) as run:
            async for part in run.stream_text():
                yield f"{part} "
