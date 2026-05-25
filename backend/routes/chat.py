import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from rag.llm import stream_answer
from pydantic import BaseModel

from rag.retriever import retrieve_documents

from rag.reranker import (
    rerank_documents,
    reranker
)

from rag.compressor import (
    compress_context
)

from rag.llm import generate_answer


router = APIRouter()



class ChatRequest(BaseModel):

    query: str

    filters: dict | None = None



@router.post("/chat")
async def chat(request: ChatRequest):
    print(request.filters)
    # Retrieve
    retrieved_docs = retrieve_documents(
        request.query,
        filters=request.filters
    )

    # Rerank
    ranked_docs = rerank_documents(
        request.query,
        retrieved_docs
    )

    # Compress
    compressed_context = compress_context(
        ranked_docs,
        request.query,
        reranker
    )

    # Generate answer
    answer = generate_answer(
        request.query,
        compressed_context
    )

    if len(compressed_context) == 0:

        return {

            "query": request.query,

            "answer":
            "No relevant documents found. Please upload documents first.",

            "sources": []
        }
    # Source formatting
    sources = []

    for item in compressed_context:

        metadata = item["metadata"]

        sources.append({

            "source": metadata.get("source"),

            "file_type": metadata.get("file_type"),

            "page": metadata.get("page"),

            "slide": metadata.get("slide"),

            "sheet": metadata.get("sheet"),

            "chunk_id": metadata.get("chunk_id")
        })

    # Remove duplicates
    unique_sources = []

    seen = set()

    for source in sources:

        key = (
        source.get("source"),
        source.get("page"),
        source.get("slide"),
        source.get("sheet")
    )

        if key not in seen:

            seen.add(key)

            unique_sources.append(source)

    return {

        "query": request.query,

        "answer": answer,

        "sources": unique_sources
    }

