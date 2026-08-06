from abc import ABC, abstractmethod

from app.agents.base.agent_result import AgentResult


class BaseAgent(ABC):

    @abstractmethod
    def detect(
        self,
        title: str,
        description: str,
    ) -> AgentResult:
        """
        Detect information from the given input
        and return an AgentResult.
        """
        pass