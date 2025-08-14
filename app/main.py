from fastapi import FastAPI
from app.api.v1 import articles, questions

app = FastAPI(title="Wikipedia Q&A API")

app.include_router(articles.router, prefix="/api/v1/articles", tags=["Articles"])
app.include_router(questions.router, prefix="/api/v1/questions", tags=["Questions"])
