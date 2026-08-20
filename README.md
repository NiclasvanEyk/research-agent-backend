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

and replace the LLM provider key with a real one. Set `RESEARCH_AGENT_DRIVER` to `llm`.

Make sure Docker is running, start the compose services

```shell
docker compose up -d
```

You can view the observability dashboard at http://localhost:18888 and the API docs at http://localhost:8787/docs.
The backend should have been built via Docker.
Even if you did not provide an OpenAI key in the previous step, the endpoint should still work with hardcoded responses.
