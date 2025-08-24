from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.db.base import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), unique=True, index=True)
    content = Column(Text, nullable=False)
    link = Column(String(512), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
