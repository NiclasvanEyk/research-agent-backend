# Research Agent Backend

## Setup

Install dependencies

```shell
uv sync
```

copy the example env file

```shell
cp .env.template .env
```

and replace the `OPENROUTER_API_KEY` with a real one. Set `RESEARCH_AGENT_DRIVER` to `llm`.

Make sure Docker is running, start the compose services

```shell
docker compose up -d
```

You can view the dashboard at http://localhost:18888

Finally run

```shell
uv run fastapi dev --port 8787 src/research_agent_backend/__init__.py
```

to start the backend.
