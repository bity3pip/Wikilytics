from pydantic import BaseModel


class ArticleResponse(BaseModel):
    title: str
    content: str


class QuestionRequest(BaseModel):
    article_title: str
    question: str


class QuestionResponse(BaseModel):
    answer: str
