from app.agents.base.base_agent import BaseAgent
from app.agents.base.agent_result import AgentResult
from app.agents.category.keywords import CATEGORY_KEYWORDS


class CategoryAgent(BaseAgent):

    def detect(
        self,
        title: str,
        description: str,
    ) -> AgentResult:

        text = f"{title} {description}".lower()

        best_category = "Others"
        highest_score = 0
        matched_keywords = []

        for category, keywords in CATEGORY_KEYWORDS.items():

            current_matches = []

            for keyword in keywords:

                if keyword in text:
                    current_matches.append(keyword)

            score = len(current_matches)

            if score > highest_score:
                highest_score = score
                best_category = category
                matched_keywords = current_matches

        if highest_score == 0:
            confidence = 0.0
        elif highest_score == 1:
            confidence = 0.75
        elif highest_score == 2:
            confidence = 0.90
        else:
            confidence = 0.98

        return AgentResult(
            category=best_category,
            confidence=confidence,
            provider="agent",
            matched_keywords=matched_keywords,
        )