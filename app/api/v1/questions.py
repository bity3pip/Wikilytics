from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.question import QuestionRequest, QuestionResponse
from app.services.rag_service import answer_question
from app.db.base import get_db


router = APIRouter()


@router.post("/", response_model=QuestionResponse)
async def ask_question(
        payload: QuestionRequest,
        db: Session = Depends(get_db)
):
    answer = await answer_question(payload.article_title, payload.question, db)
    return QuestionResponse(answer=answer)
