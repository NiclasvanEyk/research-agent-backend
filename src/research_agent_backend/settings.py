from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class ResearchAgentBackendSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    app_debug: bool = False
    """
    Enables debugging info, e.g. FastAPI is set to debug mode.
    """

    sources_storage_path: Path = Path(__file__).parent.parent.parent / "files"
    """
    Where the uploaded research sources should be stored.
    """

    research_agent_model_name: str = "openrouter:google/gemini-3.5-flash-lite"
    research_agent_driver: Literal["llm", "fake"] = "fake"

    enable_otel: bool = True


load_dotenv(".env")

settings = ResearchAgentBackendSettings()
if settings.app_debug:
    print(settings.model_dump_json(indent=4))
