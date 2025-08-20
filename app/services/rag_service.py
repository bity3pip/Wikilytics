from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from sqlalchemy.orm import Session
from app.services.wikipedia_service import fetch_article
from app.utils.text_processing import chunk_text_by_tokens
from app.core.llm_config import get_llm
from app.core.config import settings


async def answer_question(article_title: str, question: str, db: Session) -> str:
    article_content = await fetch_article(db, article_title)

    chunks = chunk_text_by_tokens(article_content, max_tokens=500, overlap_tokens=50)

    embeddings = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)
    vectorstore = FAISS.from_texts(chunks, embedding=embeddings)

    relevant_docs = vectorstore.similarity_search(question, k=3)
    context = "\n\n".join([doc.page_content for doc in relevant_docs])

    prompt = (f"Answer the question based only on the following context:"
              f"\n{context}\n\nQuestion: {question}")

    llm = get_llm()
    response = llm.invoke(prompt)

    return response.content
