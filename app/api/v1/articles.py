from http.client import HTTPException
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.services.utils.summarizer import Summarizer
from app.services.wikipedia_service import fetch_article
from app.db.utils_models import ArticleResponse
from app.db.models import Article
from app.db.base import get_db
from app.db.utils import get_article_by_title

router = APIRouter()


@router.get('/')
async def get_all_articles(db: Session = Depends(get_db)):
    articles = db.query(Article).all()
    return [
        {'id': article.id,
         'title': article.title,
         'content': article.content[:1000] + ' ...'
         if len(article.content) > 1000 else article.content,
         'link': article.link,
         }
        for article in articles
    ]


@router.get('/by-id/{article_id}')
async def get_article_by_id(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).get(article_id)
    if not article:
        raise HTTPException(status_code=404, detail='Article not found')
    return article


@router.get('/{title}', response_model=ArticleResponse)
async def get_article(title: str, db: Session = Depends(get_db)):
    content = await fetch_article(db, title)
    return ArticleResponse(title=title, content=content)


@router.get('/summary/{title}')
async def get_article_summary(title: str, db: Session = Depends(get_db)):
    article = get_article_by_title(db, title)
    if not article:
        raise HTTPException(status_code=404, detail='Article not found')

    summarizer = Summarizer()
    summary = summarizer.summarize(article.content)

    return {
        'title': article.title,
        'summary': summary,
        'link': article.link,
    }
