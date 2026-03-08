import time
from app.models.schemas import QueryResponse, ReferenceSource
from app.core.vector_store import vector_store
from app.core.llm import llm_service

import json

class RAGService:
    def __init__(self):
        pass

    async def process_query(self, query: str) -> QueryResponse:
        """
        Real RAG process with LLM:
        1. Retrieve documents from ChromaDB
        2. Generate answer using LLM
        """
        # ... existing implementation ...
        # 1. Retrieve
        results = vector_store.search(query, n_results=3)
        
        # Parse results
        documents = results['documents'][0]
        metadatas = results['metadatas'][0]
        
        sources = []
        context_text = ""
        
        for doc, meta in zip(documents, metadatas):
            sources.append(ReferenceSource(
                title=meta.get('title', 'Unknown Source'),
                snippet=doc[:100] + "..." # Snippet for UI
            ))
            context_text += f"来源 [{meta.get('title')}]: {doc}\n\n"

        # 2. Generate (Real LLM)
        if not documents:
             # Fallback to General Knowledge if no documents found
             context_text = "（本地知识库未找到相关文档，请基于您的通用医学知识回答，并明确告知用户这一点。）"
        
        # Call LLM Service
        llm_result = await llm_service.generate_response(query, context_text)

        return QueryResponse(
            answer=llm_result.get("answer", "无法生成回答"),
            sources=sources, # Empty list if no docs
            suggested_actions=llm_result.get("suggested_actions", []),
            related_conditions=llm_result.get("related_conditions", [])
        )

    async def process_query_stream(self, query: str):
        """
        Stream RAG process:
        Yields SSE events: "sources" (JSON) -> "answer" (text chunks)
        """
        # 1. Retrieve
        results = vector_store.search(query, n_results=3)
        documents = results['documents'][0]
        metadatas = results['metadatas'][0]
        
        sources = []
        context_text = ""
        
        for doc, meta in zip(documents, metadatas):
            sources.append({
                "title": meta.get('title', 'Unknown Source'),
                "snippet": doc[:100] + "..."
            })
            context_text += f"来源 [{meta.get('title')}]: {doc}\n\n"

        # Yield sources immediately
        yield f"event: sources\ndata: {json.dumps(sources, ensure_ascii=False)}\n\n"

        if not documents:
            # Fallback to General Knowledge
            context_text = "（本地知识库未找到相关文档，请基于您的通用医学知识回答，并明确告知用户这一点。）"

        # 2. Generate Stream
        async for chunk in llm_service.stream_response(query, context_text):
            # SSE format requires "data: ..."
            # We replace newlines to keep it valid SSE or handle on client
            safe_chunk = chunk.replace("\n", "\\n") 
            yield f"event: answer\ndata: {safe_chunk}\n\n"

rag_service = RAGService()
