import logfire
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from research_agent_backend.api import router as api_router
from research_agent_backend.settings import settings

app = FastAPI(
    title="Research Agent Backend",
    debug=settings.app_debug,
)
app.include_router(api_router, tags=["api"])

# Should probably only done locally in dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if settings.enable_otel:
    logfire.configure(service_name="research-agent-backend", send_to_logfire=False)
    logfire.instrument_pydantic_ai()
    logfire.instrument_fastapi(app)
