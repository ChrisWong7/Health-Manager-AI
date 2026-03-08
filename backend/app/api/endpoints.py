from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.models.schemas import QueryRequest, QueryResponse
from app.services.rag_service import rag_service

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def query_health_info(request: QueryRequest):
    """
    智能健康查询接口 (Standard JSON)
    """
    try:
        response = await rag_service.process_query(request.query)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stream_query")
async def stream_health_info(request: QueryRequest):
    """
    智能健康查询接口 (Streaming SSE)
    """
    return StreamingResponse(
        rag_service.process_query_stream(request.query),
        media_type="text/event-stream"
    )
