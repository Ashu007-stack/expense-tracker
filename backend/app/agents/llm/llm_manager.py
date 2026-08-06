import os

from app.agents.llm.provider.gemini_provider import GeminiProvider


class LLMManager:

    def __init__(self):

        provider = os.getenv("AI_PROVIDER", "gemini").lower()

        if provider == "gemini":
            self.provider = GeminiProvider()

        else:
            raise ValueError(
                f"Unsupported AI Provider: {provider}"
            )

    def categorize(
        self,
        title: str,
        description: str,
    ):

        return self.provider.categorize(
            title,
            description,
        )