from app.evals.rag_cases import RAG_EVAL_CASES
from app.services.knowledge_search import knowledge_search_service
from app.config import settings


async def evaluate_rag_retrieval() -> dict:
    top_1_passed_count = 0
    clean_passed_count = 0
    results = []

    for case in RAG_EVAL_CASES:
        retrieved = await knowledge_search_service.search_reranked(
            query=case["question"],
            limit=5,
            min_similarity=settings.rag_min_similarity,
        )

        retrieved_source_ids = [
            result.chunk.source_id
            for result in retrieved
        ]

        expected_source_ids = set(case["expected_source_ids"])
        retrieved_source_ids_set = set(retrieved_source_ids)

        if not expected_source_ids:
            top_1_passed = len(retrieved_source_ids) == 0
            clean_passed = len(retrieved_source_ids) == 0
        else:
            top_1_passed = (
                bool(retrieved_source_ids)
                and retrieved_source_ids[0] in expected_source_ids
            )

            clean_passed = (
                retrieved_source_ids_set == expected_source_ids
            )

        if top_1_passed:
            top_1_passed_count += 1

        if clean_passed:
            clean_passed_count += 1

        results.append({
            "question": case["question"],
            "expected_source_ids": case["expected_source_ids"],
            "retrieved_source_ids": retrieved_source_ids,
            "top_1_passed": top_1_passed,
            "clean_passed": clean_passed,
        })

    total = len(RAG_EVAL_CASES)

    return {
        "total": total,
        "top_1_accuracy": top_1_passed_count / total if total else 0,
        "clean_accuracy": clean_passed_count / total if total else 0,
        "results": results,
    }