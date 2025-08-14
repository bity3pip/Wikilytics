from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.wikipedia_service import fetch_article
from app.models.article import ArticleResponse
from app.db.base import get_db

router = APIRouter()


@router.get("/{title}", response_model=ArticleResponse)
async def get_article(title: str, db: Session = Depends(get_db)):
    content = await fetch_article(db, title)
    return ArticleResponse(title=title, content=content)
