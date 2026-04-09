from __future__ import annotations

from typing import Any

import praw
import requests

from .config import RedditConfig

DEFAULT_USER_AGENT = 'HermesReddit/1.0 by u/unknown'


def make_reddit(cfg: RedditConfig) -> praw.Reddit:
    if not cfg.client_id or not cfg.client_secret:
        raise ValueError('Missing REDDIT_CLIENT_ID / REDDIT_CLIENT_SECRET')

    kwargs: dict[str, Any] = {
        'client_id': cfg.client_id,
        'client_secret': cfg.client_secret,
        'user_agent': cfg.user_agent or DEFAULT_USER_AGENT,
    }
    if cfg.refresh_token:
        kwargs['refresh_token'] = cfg.refresh_token
    elif cfg.username and cfg.password:
        kwargs['username'] = cfg.username
        kwargs['password'] = cfg.password

    return praw.Reddit(**kwargs)


def health(cfg: RedditConfig) -> dict[str, Any]:
    info: dict[str, Any] = {
        'client_id_present': bool(cfg.client_id),
        'client_secret_present': bool(cfg.client_secret),
        'refresh_token_present': bool(cfg.refresh_token),
        'password_grant_present': bool(cfg.username and cfg.password),
    }
    if not (cfg.client_id and cfg.client_secret):
        return info
    try:
        reddit = make_reddit(cfg)
        me = reddit.user.me()
        info['authenticated'] = me is not None
        info['username'] = str(me) if me is not None else None
    except Exception as exc:
        info['auth_error'] = repr(exc)
    return info


def public_subreddit(subreddit: str, limit: int = 10) -> list[dict[str, Any]]:
    url = f'https://www.reddit.com/r/{subreddit}/new.json'
    payload = requests.get(url, headers={'User-Agent': DEFAULT_USER_AGENT}, params={'limit': limit, 'raw_json': 1}, timeout=30).json()
    rows: list[dict[str, Any]] = []
    for child in payload.get('data', {}).get('children', [])[:limit]:
        if child.get('kind') != 't3':
            continue
        data = child.get('data', {})
        rows.append({
            'title': data.get('title'),
            'author': data.get('author'),
            'score': data.get('score'),
            'num_comments': data.get('num_comments'),
            'permalink': 'https://www.reddit.com' + data.get('permalink', ''),
        })
    return rows
