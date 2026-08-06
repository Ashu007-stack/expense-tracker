from dataclasses import dataclass


@dataclass
class ProviderResult:
    category: str
    confidence: float
    provider: str