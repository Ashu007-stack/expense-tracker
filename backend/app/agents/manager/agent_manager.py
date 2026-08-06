from app.agents.category.category_agent import CategoryAgent


class AgentManager:

    def __init__(self):
        self.category_agent = CategoryAgent()

    def categorize(
        self,
        title: str,
        description: str,
    ):
        return self.category_agent.detect(
            title=title,
            description=description,
        )