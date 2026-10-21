from app.evals.rag_answer_cases import RAG_ANSWER_EVAL_CASES
from app.services.rag import rag_service
from app.services.rag_answer_judge import rag_answer_judge
import asyncio


async def evaluate_rag_answers() -> dict:
    async def evaluate_case(case: dict) -> dict:
        result = await rag_service.answer(question=case["question"], limit=5)

        answer_lower = result.answer.lower()
        expected_phrases = [phrase.lower() for phrase in case["expected_answer_contains"]]

        if expected_phrases:
            success = all(any(option in answer_lower for option in phrase.split("|")) for phrase in expected_phrases)
        else:
            success = len(result.sources) == 0

        context = "\n\n".join(
            f"[Source: {source.chunk.source_id}, Chunk: {source.chunk.index}]\n{source.chunk.text}"
            for source in result.sources
        )

        judge_result = await rag_answer_judge.evaluate(
            question=case["question"],
            answer=result.answer,
            context=context,
        )

        return {
            "question": case["question"],
            "answer": result.answer,
            "expected_answer_contains": case["expected_answer_contains"],
            "passed": success,
            "judge_correct": judge_result.correct,
            "judge_grounded": judge_result.grounded,
            "judge_score": judge_result.score,
            "judge_reason": judge_result.reason,
        }

    results = await asyncio.gather(
        *(evaluate_case(case) for case in RAG_ANSWER_EVAL_CASES)
    )

    total = len(results)
    passed = sum(1 for result in results if result["passed"])
    judge_correct_count = sum(1 for result in results if result["judge_correct"])
    judge_grounded_count = sum(1 for result in results if result["judge_grounded"])
    judge_score_total = sum(result["judge_score"] for result in results)

    return {
        "passed": passed,
        "total": total,
        "accuracy": passed / total if total else 0,
        "judge_correct_accuracy": judge_correct_count / total if total else 0,
        "judge_grounded_accuracy": judge_grounded_count / total if total else 0,
        "judge_average_score": judge_score_total / total if total else 0,
        "results": results,
    }