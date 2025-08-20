from pydantic import BaseModel


class QuestionRequest(BaseModel):
    article_title: str
    question: str


class QuestionResponse(BaseModel):
    answer: str
