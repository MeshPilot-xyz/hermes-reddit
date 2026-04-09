# Hermes Reddit

A small public repository for the MeshPilot / Hermes Reddit integration.

It provides a lightweight Python scaffold for working with Reddit through the API, including:
- reading public Reddit content
- authenticated posting and replies
- a simple local CLI for configuration and health checks

## Repository contents
- `src/hermes_reddit/` — Python package with config, client, and CLI helpers
- `.env.example` — example environment variables, with no secrets
- `pyproject.toml` — package metadata and dependencies
- `LICENSE` — MIT license

## Security / privacy
- No API keys or tokens are stored in this repository.
- No private customer data is stored here.
- Runtime credentials are expected to live locally, outside git.

## Local setup
```bash
python -m pip install -e .
cp .env.example .env
python -m hermes_reddit.cli health
```

## Notes
- Public monitoring works without auth.
- Authenticated actions require Reddit app credentials stored locally.
