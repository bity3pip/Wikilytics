import pytest
from app.db.models import Article


class TestArticles:
    def test_get_articles(self, client):
        response = client.get("/api/v1/articles/")
        assert response.status_code == 200

    def test_get_article_by_id(self, client, db):
        article = Article(
            title='title',
            content='content',
            link='https://example.com',
        )
        db.add(article)
        db.commit()
        db.refresh(article)

        response = client.get(f"/api/v1/articles/by-id/{article.id}")
        assert response.status_code == 200

    def test_get_article_by_title_failure(self, client):
        response = client.get("/api/v1/articles/by-id/123/")
        assert response.status_code == 404
        assert response.json() == {"detail": "Article not found"}

    @pytest.mark.asyncio
    def test_find_article_from_wikipedia(self, client, monkeypatch):
        fake_article_content = "Python is a programming language"

        async def fake_fetch_article(db, title):
            return fake_article_content

        monkeypatch.setattr("app.api.v1.articles.fetch_article", fake_fetch_article)

        response = client.get("/api/v1/articles/123")

        assert response.status_code == 200
        assert response.json()["title"] == "123"
        assert response.json()["content"] == fake_article_content

    @pytest.mark.asyncio
    def test_article_summaries(self, client, monkeypatch):
        fake_article = type("FakeArticle", (), {
            "title": "Python",
            "content": "Python is a popular programming language.",
            "link": "https://en.wikipedia.org/wiki/Python_(programming_language)"
        })()

        def fake_get_article_by_title(db, title):
            return fake_article

        monkeypatch.setattr("app.api.v1.articles.get_article_by_title", fake_get_article_by_title)

        class FakeSummarizer:
            def summarize(self, text):
                return 'Short summary'

        monkeypatch.setattr("app.api.v1.articles.Summarizer", FakeSummarizer)
        response = client.get("/api/v1/articles/summary/Python")

        assert response.status_code == 200
        data = response.json()
        assert data['title'] == 'Python'
        assert data['summary'] == "Short summary"
        assert data['link'] == fake_article.link

    def test_article_summaries_failure(self, client):
        response = client.get("/api/v1/articles/summary/Unknown")
        assert response.status_code == 404
        assert response.json() == {"detail": "Article not found"}
