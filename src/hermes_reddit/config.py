from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os

ENV_PATHS = (Path('.env'), Path.home() / '.hermes' / '.env')


@dataclass
class RedditConfig:
    client_id: str | None = None
    client_secret: str | None = None
    refresh_token: str | None = None
    username: str | None = None
    password: str | None = None
    user_agent: str = 'HermesReddit/1.0'


def _parse_env_file(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    if not path.exists():
        return data
    for raw in path.read_text(encoding='utf-8').splitlines():
        line = raw.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def load_config() -> RedditConfig:
    merged: dict[str, str] = {}
    for path in ENV_PATHS:
        merged.update(_parse_env_file(path))
    merged.update({k: v for k, v in os.environ.items() if k.startswith('REDDIT_')})
    return RedditConfig(
        client_id=merged.get('REDDIT_CLIENT_ID'),
        client_secret=merged.get('REDDIT_CLIENT_SECRET'),
        refresh_token=merged.get('REDDIT_REFRESH_TOKEN'),
        username=merged.get('REDDIT_USERNAME'),
        password=merged.get('REDDIT_PASSWORD'),
        user_agent=merged.get('REDDIT_USER_AGENT', 'HermesReddit/1.0'),
    )
