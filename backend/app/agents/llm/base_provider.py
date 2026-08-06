from abc import ABC, abstractmethod

from app.agents.llm.provider_result import ProviderResult


class BaseProvider(ABC):

    @abstractmethod
    def categorize(
        self,
        title: str,
        description: str,
    ) -> ProviderResult:
        """
        Analyze the expense using an AI model
        and return the predicted category.
        """
        pass