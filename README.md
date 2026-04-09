# Hermes Reddit

Public source repository for the MeshPilot/Hermes Reddit integration.

This repository is intentionally small and non-sensitive. It exists to satisfy Reddit app registration requirements and to document the shape of the integration without exposing credentials or private operational data.

## What this project is for
- Reading public Reddit content
- Authenticated posting and replying via Reddit API
- Lightweight operator workflow for Hermes / MeshPilot

## Repository contents
- `src/hermes_reddit/` — small Python package with client/config/CLI scaffolding
- `.env.example` — example environment variables, with no secrets
- `pyproject.toml` — package metadata and dependencies

## Security / privacy
- No API keys or tokens are stored in this repository.
- No private customer data is stored here.
- The repo is public because Reddit asks for a public source-code URL during app registration.

## Local setup
```bash
python -m pip install -e .
cp .env.example .env
python -m hermes_reddit.cli health
```

## Notes
- Public monitoring works without auth.
- Authenticated actions require Reddit app credentials stored locally, not in git.
