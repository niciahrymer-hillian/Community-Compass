"""
Personalized benefits/housing news, matched to a user's qualification type.

Sources are Google News RSS topic searches (reliable, real-time) so renters
see current updates on the programs that actually affect them:
  HUD          → all renters (federal housing)
  Section 8    → voucher holders (section8 / hcv / srap)
  Social Security (SSA) → ssi / ssdi / fixed-income renters
  DSHA         → Delaware State Housing Authority / SRAP recipients

Each source fails silently so the feed always loads.
"""
import re
import feedparser
import httpx

_GN = "https://news.google.com/rss/search?q={}&hl=en-US&gl=US&ceid=US:en"

FEEDS = {
    # Housing news is scoped to Delaware (renters here only want local programs).
    "hud":      [_GN.format("Delaware+HUD+housing+assistance+OR+%22public+housing%22")],
    "section8": [_GN.format("Delaware+%22Section+8%22+housing+voucher")],
    # Social Security benefits are federal, so this stays national (e.g., COLA).
    "ssa":      [_GN.format("SSI+OR+SSDI+Social+Security+benefits+increase")],
    # DSHA = OFFICIAL Delaware government feed (agency press releases), with a
    # Google News fallback in case the state site is unreachable.
    "dsha":     ["https://news.delaware.gov/tag/dsha/feed/",
                 "https://news.delaware.gov/category/dsha/feed/",
                 _GN.format("%22Delaware+State+Housing+Authority%22")],
}

SOURCE_LABELS = {
    "hud": "HUD", "section8": "Section 8", "ssa": "Social Security", "dsha": "DSHA",
}

# income_type / voucher_type → which sources to include
QUALIFICATION_SOURCES = {
    "section8":  ["hud", "section8", "dsha"],
    "hcv":       ["hud", "section8", "dsha"],
    "srap":      ["hud", "dsha", "section8"],
    "ssi":       ["hud", "ssa"],
    "ssdi":      ["hud", "ssa"],
    "fixed":     ["hud", "ssa"],
    "employment":["hud"],
    None:        ["hud", "section8"],
}

# Listing program → news sources. Used for landlords, whose relevant news is
# derived from the programs their own inventory accepts (55+ / SSI / Section 8…).
PROGRAM_SOURCES = {
    "section8":          ["hud", "section8", "dsha"],
    "srap":              ["hud", "dsha", "section8"],
    "age55plus":         ["hud", "ssa", "dsha"],
    "income_restricted": ["hud", "dsha"],
}


def sources_for_programs(programs: list[str]) -> list[str]:
    """News source keys for a set of listing programs (HUD always included)."""
    keys = ["hud"]
    for p in programs or []:
        for k in PROGRAM_SOURCES.get(p, []):
            if k not in keys:
                keys.append(k)
    return keys


async def stored_news_for(db, source_keys: list[str], limit: int = 6) -> list[dict]:
    """Read personalized news from the news_items table (populated by the
    refresh job), round-robined across sources so every program is represented.

    Reading from storage — not live RSS — keeps the feed instant and reliable
    during a demo even if an upstream feed is slow or offline.
    """
    from sqlalchemy import select
    from app.models.news_item import NewsItem

    buckets: dict[str, list] = {}
    for key in source_keys:
        rows = await db.execute(
            select(NewsItem).where(NewsItem.source == key)
            .order_by(NewsItem.fetched_at.desc()).limit(4)
        )
        buckets[key] = rows.scalars().all()

    out: list[dict] = []
    seen: set[str] = set()
    for i in range(4):
        for key in source_keys:
            bucket = buckets.get(key, [])
            if i < len(bucket) and bucket[i].title not in seen:
                seen.add(bucket[i].title)
                out.append({
                    "title": bucket[i].title, "summary": bucket[i].summary,
                    "link": bucket[i].link, "source": SOURCE_LABELS.get(key, key.upper()),
                })
            if len(out) >= limit:
                return out
    return out


def _clean(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text or "").strip()


async def _fetch_feed(url: str, source_label: str, limit: int = 3) -> list[dict]:
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(url, timeout=8.0, follow_redirects=True,
                                 headers={"User-Agent": "Mozilla/5.0 HomeMatch/1.0"})
        if not r.is_success:
            return []
        parsed = feedparser.parse(r.text)
        items = []
        for entry in parsed.entries[:limit]:
            items.append({
                "title": _clean(entry.get("title", "Update")),
                "summary": "",  # Google News summaries are HTML link-lists; omit for clean cards
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
                "source": source_label,
            })
        return items
    except Exception:
        return []


async def fetch_personalized_news(
    income_type: str | None,
    voucher_type: str | None,
    limit: int = 6,
) -> list[dict]:
    """Return news relevant to the user's programs (SSA, HUD, Section 8, DSHA)."""
    source_keys: list[str] = []
    for key in (QUALIFICATION_SOURCES.get(income_type, QUALIFICATION_SOURCES[None])
                + QUALIFICATION_SOURCES.get(voucher_type, [])):
        if key not in source_keys:
            source_keys.append(key)

    # Fetch a few per source, then round-robin so every program is represented
    per_source: list[list[dict]] = []
    for key in source_keys:
        bucket: list[dict] = []
        for url in FEEDS.get(key, []):
            bucket += await _fetch_feed(url, SOURCE_LABELS.get(key, key.upper()), limit=3)
        per_source.append(bucket)

    all_items: list[dict] = []
    seen_titles: set[str] = set()
    for round_i in range(3):
        for bucket in per_source:
            if round_i < len(bucket):
                item = bucket[round_i]
                if item["title"] and item["title"] not in seen_titles:
                    seen_titles.add(item["title"])
                    all_items.append(item)
            if len(all_items) >= limit:
                return all_items
    return all_items[:limit]
