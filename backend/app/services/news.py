"""Consolidated newsfeed (Python).

Combines two real sources into one /news payload:
  - FirstStep's 8 curated Delaware items (firststep_news.json)
  - HomeMatch's live HUD/DSHA/Section 8 RSS via their actual news_service
    (fetch_personalized_news → feedparser)

Both are normalized to one shape so the frontend renders them uniformly. The
live fetch is best-effort: if the network/feeds are down, the static items still
load (HomeMatch's _fetch_feed already fails silently).
"""

import json
from pathlib import Path

from app.homematch.news_service import fetch_personalized_news

_STATIC_FILE = Path(__file__).resolve().parent.parent / "data" / "firststep_news.json"


def load_static() -> list[dict]:
    """FirstStep's curated items, normalized to the common news shape."""
    raw = json.loads(_STATIC_FILE.read_text())
    records = raw.get("records", raw) if isinstance(raw, dict) else raw
    out = []
    for r in records:
        if r.get("active") is False:
            continue
        out.append({
            "id": r.get("id"),
            "headline": r.get("headline"),
            "summary": r.get("summary"),
            "source": r.get("source_name"),
            "url": r.get("source_url"),
            "published": r.get("published"),
            "urgency": r.get("urgency"),
            "why_it_matters": r.get("why_it_matters"),
            "category": r.get("type"),
        })
    return out


def _normalize_live(item: dict) -> dict:
    """HomeMatch RSS item ({title, summary, link, …}) → the common news shape."""
    return {
        "id": item.get("link") or item.get("title"),
        "headline": item.get("title"),
        "summary": item.get("summary") or "",
        "source": item.get("source"),
        "url": item.get("link"),
        "published": item.get("published"),
        "urgency": "info",
        "why_it_matters": None,
        "category": "news",
    }


async def get_news(include_live: bool = True) -> list[dict]:
    """Static FirstStep items first, then live HUD/DSHA (best-effort)."""
    items = load_static()
    if include_live:
        try:
            live = await fetch_personalized_news(income_type=None, voucher_type="section8", limit=6)
            items += [_normalize_live(x) for x in live]
        except Exception:
            pass  # never fail the feed on a network hiccup
    return items
