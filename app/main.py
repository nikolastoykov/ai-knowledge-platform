from fastapi import FastAPI

from app.api.generation import router as generation_router
from app.api.summarization import router as summarization_router
from app.api.rewrite import router as rewrite_router
from app.api.ticket_classifier import router as ticket_classifier_router
from app.api.order_assistant import router as order_assistant_router
from app.api.embeddings import router as embeddings_router
from app.api.semantic_search import router as semantic_search_router
from app.api.rag import router as rag_router
from app.api.knowledge import router as knowledge_router
from app.api.evals import router as evals_router
from app.api.managed_rag import router as managed_rag
from app.api.agent import router as agent_router


app = FastAPI(title="AI Knowledge Platform")

app.include_router(generation_router)
app.include_router(summarization_router)
app.include_router(rewrite_router)
app.include_router(ticket_classifier_router)
app.include_router(order_assistant_router)
app.include_router(embeddings_router)
app.include_router(semantic_search_router)
app.include_router(rag_router)
app.include_router(knowledge_router)
app.include_router(evals_router)
app.include_router(managed_rag)
app.include_router(agent_router)