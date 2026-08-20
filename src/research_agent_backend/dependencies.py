import logging
import os
from typing import Annotated

from fastapi import Depends

from research_agent_backend.agent import (
    FakeResearchAgent,
    LlmResearchAgent,
    ResearchAgent,
)
from research_agent_backend.settings import settings
from research_agent_backend.sources import ResearchSources

logger = logging.getLogger(__name__)


def get_research_sources() -> ResearchSources:
    return ResearchSources(settings.sources_storage_path)


ResearchSourcesDep = Annotated[ResearchSources, Depends(get_research_sources)]


def get_research_agent(research_sources: ResearchSourcesDep) -> ResearchAgent:
    if settings.research_agent_driver == "fake":
        return FakeResearchAgent(
            parts=[
                "The answer is",
                "42",
                "This is a fake research agent",
                "You probably did not have a key to an LLM",
            ]
        )
    return LlmResearchAgent(
        model_name=settings.research_agent_model_name, sources=research_sources
    )


ResearchAgentDep = Annotated[ResearchAgent, Depends(get_research_agent)]
