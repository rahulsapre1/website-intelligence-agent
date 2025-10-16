from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class AnalyzeRequest(BaseModel):
    url: HttpUrl
    questions: Optional[List[str]] = None


class ChatRequest(BaseModel):
    url: HttpUrl
    query: str
    conversation_history: Optional[List[Dict[str, str]]] = None


class BusinessInsights(BaseModel):
    industry: Optional[str] = None
    company_size: Optional[str] = None
    location: Optional[str] = None
    usp: Optional[str] = None  # Unique Selling Proposition
    products_services: Optional[str] = None
    target_audience: Optional[str] = None
    contact_info: Optional[Dict[str, Any]] = None


class AnalyzeResponse(BaseModel):
    url: str
    insights: BusinessInsights
    timestamp: datetime


class ChatResponse(BaseModel):
    response: str
    timestamp: datetime


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
