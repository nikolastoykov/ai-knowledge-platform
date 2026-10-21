from app.domain.search import DocumentChunk


def chunk_text(
    source_id: str,
    text: str,
    chunk_size: int = 1000,
    overlap: int = 200,
) -> list[DocumentChunk]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0.")

    if overlap < 0:
        raise ValueError("overlap cannot be negative.")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size.")

    text = text.strip()

    if not text:
        return []

    chunks: list[DocumentChunk] = []
    start = 0
    index = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))

        if end < len(text):
            sentence_boundary = find_sentence_boundary(
                text=text,
                start=start,
                end=end,
            )

            if sentence_boundary > start:
                end = sentence_boundary
            else:
                last_space = text.rfind(" ", start, end)

                if last_space > start:
                    end = last_space

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(
                DocumentChunk(
                    source_id=source_id,
                    index=index,
                    text=chunk,
                )
            )
            index += 1

        if end >= len(text):
            break

        next_start = max(0, end - overlap)

        sentence_start = find_next_sentence_start(
            text=text,
            start=next_start,
            end=end,
        )

        if sentence_start != -1:
            start = sentence_start
        else:
            first_space = text.find(" ", next_start, end)

            if first_space != -1:
                start = first_space + 1
            else:
                start = end

    return chunks

def find_sentence_boundary(text: str, start: int, end: int) -> int:
    sentence_endings = [". ", "! ", "? "]

    positions = [text.rfind(ending, start, end) for ending in sentence_endings]

    valid_positions = [position for position in positions if position != -1]

    if not valid_positions:
        return -1

    return max(valid_positions) + 1

def find_next_sentence_start(text: str, start: int, end: int) -> int:
    sentence_endings = [". ", "! ", "? "]

    positions = [text.find(ending, start, end) for ending in sentence_endings]

    valid_positions = [position for position in positions if position != -1]

    if not valid_positions:
        return -1

    position = min(valid_positions)

    return position + 2