from dataclasses import dataclass


@dataclass
class ManagedSearchResult:
    file_id: str
    filename: str
    text: str
    score: float