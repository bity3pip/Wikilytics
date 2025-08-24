from app.core.llm_config import get_llm


class Summarizer:
    def __init__(self):
        self.llm = get_llm()

    def summarize(self, text: str, max_length: int = 200) -> str:
        prompt = f"Summarize the following text in {max_length} words or less:\n\n{text}"
        response = self.llm.invoke(prompt)
        return response.content.strip()
