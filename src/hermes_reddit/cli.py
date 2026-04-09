from __future__ import annotations

import argparse
import json

import praw

from .client import health, make_reddit, public_subreddit
from .config import load_config


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description='Hermes Reddit helper')
    sub = p.add_subparsers(dest='cmd', required=True)

    sub.add_parser('health', help='Show credential readiness and auth status')

    s = sub.add_parser('subreddit', help='List new public posts from a subreddit')
    s.add_argument('subreddit')
    s.add_argument('--limit', type=int, default=10)

    s = sub.add_parser('me', help='Print authenticated username')

    s = sub.add_parser('auth-url', help='Create an OAuth authorization URL')
    s.add_argument('--redirect-uri', default='http://localhost:8080')
    s.add_argument('--scope', default='identity read submit mysubreddits')
    s.add_argument('--duration', default='permanent', choices=['temporary', 'permanent'])
    s.add_argument('--state', default='hermes-reddit')

    s = sub.add_parser('exchange-code', help='Exchange an OAuth code for a refresh token')
    s.add_argument('code')
    s.add_argument('--redirect-uri', default='http://localhost:8080')

    return p


def main() -> int:
    args = build_parser().parse_args()
    cfg = load_config()

    if args.cmd == 'health':
        print(json.dumps(health(cfg), indent=2, sort_keys=True))
        return 0

    if args.cmd == 'subreddit':
        print(json.dumps(public_subreddit(args.subreddit, args.limit), indent=2, sort_keys=True))
        return 0

    if args.cmd == 'me':
        reddit = make_reddit(cfg)
        me = reddit.user.me()
        print(str(me) if me is not None else '')
        return 0

    if args.cmd == 'auth-url':
        if not cfg.client_id or not cfg.client_secret:
            raise SystemExit('Missing REDDIT_CLIENT_ID / REDDIT_CLIENT_SECRET')
        reddit = praw.Reddit(
            client_id=cfg.client_id,
            client_secret=cfg.client_secret,
            user_agent=cfg.user_agent,
        )
        url = reddit.auth.url(
            scopes=args.scope.split(),
            state=args.state,
            duration=args.duration,
            redirect_uri=args.redirect_uri,
        )
        print(url)
        return 0

    if args.cmd == 'exchange-code':
        if not cfg.client_id or not cfg.client_secret:
            raise SystemExit('Missing REDDIT_CLIENT_ID / REDDIT_CLIENT_SECRET')
        reddit = praw.Reddit(
            client_id=cfg.client_id,
            client_secret=cfg.client_secret,
            redirect_uri=args.redirect_uri,
            user_agent=cfg.user_agent,
        )
        print(reddit.auth.authorize(args.code))
        return 0

    return 1


if __name__ == '__main__':
    raise SystemExit(main())
