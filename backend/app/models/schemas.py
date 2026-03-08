from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    query: str
    history: Optional[List[dict]] = []  # [{"role": "user", "content": "..."}, ...]

class ReferenceSource(BaseModel):
    title: str
    url: Optional[str] = None
    snippet: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[ReferenceSource]
    suggested_actions: List[str]
    related_conditions: List[str]
