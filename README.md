# 🧐 About

Wikilytics is a FastAPI-based web service that lets you explore Wikipedia articles with the help of LLMs. 
It retrieves articles, preprocesses their content, and uses Retrieval-Augmented Generation (RAG) to answer natural language questions with accuracy and context.

## 📖Features
✅Wikipedia integration – fetch full article content directly from the Wikipedia API 
✅Content preprocessing – clean and chunk articles to provide high-quality context for the model
✅Question answering – ask natural language questions and get grounded answers using a RAG (Retrieval-Augmented Generation) pipeline powered by LangChain
✅Article summarization – generate concise summaries of articles
✅Related resources – return article metadata and useful links alongside answers

## ⛏️ Built Using
- [```Python```](https://www.python.org)
- [```FastAPI```](https://fastapi.tiangolo.com)
- [```sqlalchemy```](https://www.sqlalchemy.org/)
- [```alembic```](https://alembic.sqlalchemy.org/en/latest/)
- [```postgresql```](https://www.postgresql.org/)
- [```OpenAPI```](https://www.openapis.org)
- [```Wikipedia API```](https://en.wikipedia.org/w/api.php)
- [```LangChain```](https://www.langchain.com/)

## 📁 Structure

```bash
.
├── app/
│   ├── api/                             # API layer (FastAPI routers)
│   │    ├── v1/                         # Version 1 of the API endpoints
│   │    │    ├── articles.py            # Endpoints for working with articles
│   │    │    ├── questions.py           # Endpoints for handling questions
│   │    └── __init__.py 
│   ├── core/                            # Core application configuration
│   │    ├── config.py                   # Global settings (DB URL, API keys, etc.)
│   │    ├── llm_config.py               # Config for LLM (LangChain, embeddings, etc.)
│   ├── db/                              # Database layer
│   │    ├── base.py                     # Base class and session setup
│   │    ├── models.py                   # SQLAlchemy ORM models
│   │    ├── utils.py                    # Helper functions for DB operations
│   │    ├── utils_models.py             # Pydantic schemas for DB models (response/requests)
│   │    └── __init__.py 
│   ├── services/                        # Business logic / external integrations
│   │    ├── utils/                      # Utilities for services
│   │    │     ├── __init__.py          
│   │    │     ├── summarizer.py         # Summarization logic (LLM or NLP based)
│   │    │     ├── text_processing.py    # Text preprocessing/cleaning functions
│   │    ├── rag_service.py              # Retrieval-Augmented Generation (LangChain RAG pipeline)
│   │    ├── wikipedia_service.py        # Service to fetch and store Wikipedia articles
│   │    └── __init__.py 
│   ├── tests/                           # Unit and integration tests
│   └── main.py                          # Application entrypoint (FastAPI app)
│
├── requirements.txt
├── .env
├── .gitignore
└── README.md
````
## 🏁 Getting Started
These instructions will get you a copy of the API up and running on your local machine for development and testing purposes.

## Installation

For install you can use the commands are given below

```bash
  git clone https://github.com/bity3pip/Wikilytics 
  cd Wikilytics
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  uvicorn app.main:app --reload
```

## Environment variable
Create an .env file in root with these keys:
- OPENAI_API_KEY
- WIKIPEDIA_API_URL=https://en.wikipedia.org/w/api.php
- DATABASE_URL

## API Reference

#### Get all articles

```http
  GET /api/v1/articles/
```
Returns a list of all articles stored in the database.

#### Fetch article from Wikipedia by title
```http
  GET /api/v1/articles/{title}
```

| Parameter | Type     | Description                                                    |
|:----------|:---------|:---------------------------------------------------------------|
| `title`   | `string` | **Required**. Title of the article to fetch from Wikipedia API |


#### Get article by ID (from database)

```http
  GET /api/v1/articles/by-id/{article_id}
```

| Parameter    | Type      | Description                                     |
|:-------------|:----------|:------------------------------------------------|
| `article_id` | `integer` | **Required**. ID of the article in the database |


#### Get article summary (from database)

```http
  GET /api/v1/articles/summary/{title}
```

| Parameter | Type     | Description                                     |
|:----------|:---------|:------------------------------------------------|
| `title`   | `string` | **Required**. Title of the article to summarize |

#### Ask question by OpenAI

```http
  GET /api/v1/question
```

| Parameter       | Type     | Description                                     |
|:----------------|:---------|:------------------------------------------------|
| `article_title` | `string` | **Required**. Title of the article to summarize |
| `question`      | `string` | **Required**. A question which you want to ask  |


## 🔧 Running the tests
Tests include both unit and API integration tests (with mocked external dependencies).
To run tests, run the following command

``` cli
(.venv) Wikilytics % pytest .
=================================================================================== test session starts ====================================================================================
platform darwin -- Python 3.11.9, pytest-8.4.1, pluggy-1.6.0
rootdir: /Wikilytics
configfile: pytest.ini
plugins: anyio-4.9.0, mock-3.14.1, langsmith-0.4.14
collected 8 items                                                                                                                                                                          

app/tests/test_articles.py::TestArticles::test_get_articles PASSED                                                                                                                   [ 12%]
app/tests/test_articles.py::TestArticles::test_get_article_by_id PASSED                                                                                                              [ 25%]
app/tests/test_articles.py::TestArticles::test_get_article_by_title_failure PASSED                                                                                                   [ 37%]
app/tests/test_articles.py::TestArticles::test_find_article_from_wikipedia PASSED                                                                                                    [ 50%]
app/tests/test_articles.py::TestArticles::test_article_summaries PASSED                                                                                                              [ 62%]
app/tests/test_articles.py::TestArticles::test_article_summaries_failure PASSED                                                                                                      [ 75%]
app/tests/test_questions.py::TestQuestions::test_ask_question_success PASSED                                                                                                         [ 87%]
app/tests/test_questions.py::TestQuestions::test_ask_question_failure PASSED                                                                                                         [100%]

============================================================================== 8 passed in 0.37s ===========================================================================================
```

