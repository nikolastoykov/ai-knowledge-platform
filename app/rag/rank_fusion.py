from app.domain.search import ChunkSearchResult, HybridSearchResult, KeywordSearchResult

def reciprocal_rank_fusion(semantic_results: list[ChunkSearchResult], keyword_results: list[KeywordSearchResult], k: int = 60) -> list[HybridSearchResult]:
    scores: dict[tuple[str, int], float] = {}
    chunks = {}

    for rank, result in enumerate(semantic_results, start=1):
        key = (result.chunk.source_id, result.chunk.index)
        scores[key] = scores.get(key, 0) + 1 / (k + rank)
        chunks[key] = result.chunk

    for rank, result in enumerate(keyword_results, start=1):
        key = (result.chunk.source_id, result.chunk.index)
        scores[key] = scores.get(key, 0) + 1 / (k + rank)
        chunks[key] = result.chunk

    results = [HybridSearchResult(chunk=chunks[key], score=score) for key, score in scores.items()]

    return sorted(results, key=lambda result: result.score, reverse=True)