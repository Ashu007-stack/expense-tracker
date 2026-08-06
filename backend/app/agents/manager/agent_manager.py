from app.agents.category.category_agent import CategoryAgent
from app.agents.llm.llm_manager import LLMManager


class AgentManager:

    def __init__(self):
        self.category_agent = CategoryAgent()
        self.llm = LLMManager()

    def categorize(
        self,
        title: str,
        description: str,
    ):

        result = self.category_agent.detect(
            title=title,
            description=description,
        )

        # Good enough
        if result.confidence >= 0.50:
            return result

        # Otherwise ask AI
        return self.llm.categorize(
            title=title,
            description=description,
        )