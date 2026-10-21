from math import sqrt


def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float],
) -> float:
    if len(vector_a) != len(vector_b):
        raise ValueError(
            "Vectors must have the same dimensions."
        )

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

    if magnitude_a == 0 or magnitude_b == 0:
        raise ValueError(
            "Cannot calculate cosine similarity for a zero-length vector."
        )

    return dot / (magnitude_a * magnitude_b)