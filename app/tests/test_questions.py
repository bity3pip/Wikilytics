import pytest
from fastapi import HTTPException


class TestQuestions:
    @pytest.mark.asyncio
    def test_ask_question_success(self, client, monkeypatch):
        async def fake_answer_question(article_title, question, db):
            assert article_title == "Python"
            assert question == "What is Python?"
            return "Python is a programming language"

        monkeypatch.setattr("app.api.v1.questions.answer_question", fake_answer_question)

        response = client.post(
            "/api/v1/questions/",
            json={"article_title": "Python", "question": "What is Python?"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["answer"] == "Python is a programming language"

    @pytest.mark.asyncio
    def test_ask_question_failure(self, client, monkeypatch):
        async def fake_answer_question(article_title, question, db):
            raise HTTPException(status_code=404, detail="Article not found")

        monkeypatch.setattr("app.api.v1.questions.answer_question", fake_answer_question)

        response = client.post(
            '/api/v1/questions/',
            json={"article_title": "Unknown", "question": "?"}
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Article not found"
