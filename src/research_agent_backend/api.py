import asyncio

from fastapi import APIRouter, UploadFile
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, PositiveInt
from pydantic_extra_types.mime_types import MimeType

from research_agent_backend.dependencies import ResearchAgentDep, ResearchSourcesDep

router = APIRouter(prefix="/api")


class ResearchRequest(BaseModel):
    request: str


@router.post("/research", response_class=StreamingResponse)
async def research(request: ResearchRequest, agent: ResearchAgentDep):
    """
    Forwards the research request string to our agent and streams the result.
    """
    async for chunk in agent.research(request.request):
        yield chunk


class UploadedFile(BaseModel):
    name: str
    size: PositiveInt
    type: MimeType


class SourcesResponse(BaseModel):
    uploaded: list[UploadedFile]


@router.post("/sources")
async def sources(
    files: list[UploadFile],
    sources: ResearchSourcesDep,
) -> SourcesResponse:
    """
    Uploads more context files for the agent to use for its research.
    """
    uploaded_sources = await asyncio.gather(*(sources.store(file) for file in files))
    return SourcesResponse(
        uploaded=[
            UploadedFile(
                name=source.location.name,
                size=source.size,
                type=source.mime_type,
            )
            for source in uploaded_sources
        ]
    )
