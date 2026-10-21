from dataclasses import dataclass


@dataclass
class SearchDocument:
    id: str
    text: str
    embedding: list[float]

@dataclass
class SearchResult:
    document: SearchDocument
    similarity: float   

@dataclass
class DocumentChunk:
    source_id: str
    index: int
    text: str

@dataclass
class ChunkSearchResult:
    chunk: DocumentChunk
    similarity: float


@dataclass
class HybridSearchResult:
    chunk: DocumentChunk
    score: float

@dataclass
class RerankedSearchResult:
    chunk: DocumentChunk
    relevance_score: float

@dataclass
class RAGResult:
    answer: str
    sources: list[RerankedSearchResult]

@dataclass
class KnowledgeDocument:
    id: str
    text: str

@dataclass
class EmbeddedDocumentChunk:
    source_id: str
    index: int
    text: str
    embedding: list[float]

@dataclass
class KeywordSearchResult:
    chunk: DocumentChunk
    rank: float
