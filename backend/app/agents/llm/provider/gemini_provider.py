import json
import os

from google import genai

from app.agents.llm.base_provider import BaseProvider
from app.agents.base.agent_result import AgentResult


class GeminiProvider(BaseProvider):

    def __init__(self):
        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

    def categorize(
        self,
        title: str,
        description: str,
    ) -> AgentResult:

        prompt = f"""
You are an AI expense categorization assistant.

Your job is to determine the most appropriate expense category.

Available categories:

- Food
- Travel
- Shopping
- Entertainment
- Bills
- Health
- Education
- Others

Expense Title:
{title}

Expense Description:
{description}

Think carefully about the MEANING.

Do not rely only on keywords.

Return ONLY valid JSON.

Example:

{{
    "category":"Travel",
    "confidence":0.94
}}
"""

        response = self.client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
        )

        result = json.loads(response.text)

        return AgentResult(
            category=result["category"],
            confidence=result["confidence"],
            provider="Gemini",
            matched_keywords=[],
        )