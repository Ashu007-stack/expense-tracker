from dataclasses import dataclass


@dataclass
class AgentResult:
    category: str
    confidence: float
    provider: str
    matched_keywords: list[str]