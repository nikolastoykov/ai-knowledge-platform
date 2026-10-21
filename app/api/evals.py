from fastapi import APIRouter

from app.evals.rag_retrieval import evaluate_rag_retrieval
from app.evals.rag_answers import evaluate_rag_answers


router = APIRouter(prefix="/evals", tags=["Evals"])

@router.post("/rag-retrieval")
async def run_rag_retrieval_eval() -> dict:
    return await evaluate_rag_retrieval()

@router.post("/rag-answers")
async def run_rag_answer_eval() -> dict:
    return await evaluate_rag_answers()