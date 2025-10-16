from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from datetime import datetime
import logging

from app.config import settings
from app.models.schemas import (
    AnalyzeRequest, AnalyzeResponse, ChatRequest, ChatResponse, 
    BusinessInsights, ErrorResponse
)
from app.utils.auth import verify_token
from app.services.database import db_service
from app.services.scraper import scraper_service
from app.services.llm import llm_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="AI-powered agent for extracting business insights from websites",
    version="1.0.0"
)

# Setup rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Website Intelligence Agent API", "status": "healthy"}


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }


@app.post(
    "/api/analyze",
    response_model=AnalyzeResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
@limiter.limit(f"{settings.rate_limit_per_minute}/minute")
async def analyze_website(
    request: Request,
    analyze_request: AnalyzeRequest,
    token: str = Depends(verify_token)
):
    """
    Analyze a website and extract business insights
    """
    try:
        logger.info(f"Analyzing website: {analyze_request.url}")
        
        # Step 1: Scrape website content
        content = await scraper_service.scrape_website(str(analyze_request.url))
        
        # Step 2: Store scraped content in database
        analysis_id = await db_service.store_website_analysis(
            url=str(analyze_request.url),
            raw_content=content
        )
        
        # Step 3: Extract insights using LLM
        insights_data = await llm_service.extract_business_insights(
            content=content,
            custom_questions=analyze_request.questions
        )
        
        # Step 4: Update database with insights
        await db_service.store_website_analysis(
            url=str(analyze_request.url),
            raw_content=content,
            insights=insights_data
        )
        
        # Step 5: Prepare response
        if analyze_request.questions:
            # Custom questions format
            insights = BusinessInsights()
            insights.products_services = insights_data.get("custom_answers", "Analysis completed")
        else:
            # Default insights format
            insights = BusinessInsights(**insights_data)
        
        return AnalyzeResponse(
            url=str(analyze_request.url),
            insights=insights,
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@app.post(
    "/api/chat",
    response_model=ChatResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Website not analyzed"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
@limiter.limit(f"{settings.rate_limit_per_minute}/minute")
async def chat_about_website(
    request: Request,
    chat_request: ChatRequest,
    token: str = Depends(verify_token)
):
    """
    Ask conversational questions about a previously analyzed website
    """
    try:
        logger.info(f"Chat query for website: {chat_request.url}")
        
        # Step 1: Retrieve website data from database
        website_data = await db_service.get_website_analysis(str(chat_request.url))
        
        if not website_data:
            raise HTTPException(
                status_code=404,
                detail="Website not found. Please analyze the website first using /api/analyze"
            )
        
        # Step 2: Get conversation history
        conversation_history = await db_service.get_conversation_history(
            url=str(chat_request.url),
            limit=10
        )
        
        # Step 3: Generate response using LLM
        response_text = await llm_service.answer_conversational_query(
            content=website_data["raw_content"],
            query=chat_request.query,
            conversation_history=conversation_history
        )
        
        # Step 4: Store conversation in database
        await db_service.store_conversation(
            url=str(chat_request.url),
            query=chat_request.query,
            response=response_text
        )
        
        return ChatResponse(
            response=response_text,
            timestamp=datetime.utcnow()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Chat failed: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.port)
