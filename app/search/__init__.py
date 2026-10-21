from math import sqrt
from app.db.database import session_factory
from app.search.postgres_vector_store import PostgreVectorStore

search_vector_store = PostgreVectorStore(session_factory=session_factory
                                         )

def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float],
) -> float:
    dot = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = sqrt(
        sum(b * b for b in vector_b)
    )

    return dot / (magnitude_a * magnitude_b)