import aiohttp
import ssl
import certifi
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db import crud


async def fetch_article(db: Session, title: str) -> str:
    existing = crud.get_article_by_title(db, title)
    if existing:
        return existing.content

    ssl_context = ssl.create_default_context(cafile=certifi.where())
    params = {
        "action": "query",
        "prop": "extracts",
        "explaintext": "true",
        "titles": title,
        "format": "json"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(settings.wikipedia_api_url, params=params, ssl=ssl_context) as resp:
            data = await resp.json()
            pages = data.get("query", {}).get("pages", {})
            content = next(iter(pages.values())).get("extract", "")

    if content:
        crud.create_article(db, title, content)
    return content
