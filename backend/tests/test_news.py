"""Tests for the consolidated /news feed (FirstStep + HomeMatch HUD/DSHA)."""

import app.services.news as news_mod


def test_load_static_normalizes_firststep_items():
    items = news_mod.load_static()
    assert len(items) >= 1
    assert all({"headline", "summary", "source", "why_it_matters", "category"} <= set(i) for i in items)


async def test_news_endpoint_returns_static_without_network(async_client, monkeypatch):
    # Stub live fetch so the test never touches the network.
    async def _no_live(*args, **kwargs):
        return []

    monkeypatch.setattr(news_mod, "fetch_personalized_news", _no_live)
    r = await async_client.get("/news")
    assert r.status_code == 200
    body = r.json()
    assert len(body) >= 1
    assert any(i.get("why_it_matters") for i in body)   # FirstStep items carry this


async def test_news_endpoint_merges_live_rss(async_client, monkeypatch):
    async def _fake_live(*args, **kwargs):
        return [{"title": "HUD raises voucher limits", "summary": "", "link": "http://x",
                 "published": "2026-06-10", "source": "HUD"}]

    monkeypatch.setattr(news_mod, "fetch_personalized_news", _fake_live)
    r = await async_client.get("/news")
    headlines = [i["headline"] for i in r.json()]
    assert "HUD raises voucher limits" in headlines
