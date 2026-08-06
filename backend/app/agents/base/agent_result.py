from dataclasses import dataclass


@dataclass
class AgentResult:
    category: str
    confidence: float
    matched_keywords: list[str]