from sqlalchemy.orm import Session
from app.db.models import Article


def get_article_by_title(db: Session, title: str):
    return db.query(Article).filter(Article.title == title).first()


def create_article(db: Session, title: str, content: str, link: str):
    article = Article(title=title, content=content, link=link)
    db.add(article)
    db.commit()
    db.refresh(article)
    return article
