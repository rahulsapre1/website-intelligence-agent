import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app
from app.config import Settings


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def client():
    """Create a test client for FastAPI app."""
    return TestClient(app)


@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    return Settings(
        gemini_api_key="test_gemini_key",
        supabase_url="https://test.supabase.co",
        supabase_key="test_supabase_key",
        api_secret_key="test_secret_key",
        rate_limit_per_minute=10
    )


@pytest.fixture(autouse=True)
def mock_app_settings():
    """Mock app settings for all tests."""
    with patch('app.config.settings') as mock_settings:
        mock_settings.api_secret_key = "test_secret_key"
        mock_settings.gemini_api_key = "test_gemini_key"
        mock_settings.supabase_url = "https://test.supabase.co"
        mock_settings.supabase_key = "test_supabase_key"
        mock_settings.jina_api_key = "test_jina_key"
        mock_settings.rate_limit_per_minute = 10
        yield mock_settings


@pytest.fixture
def sample_website_content():
    """Sample website content for testing."""
    return """
    # Acme Corporation
    
    Welcome to Acme Corporation, a leading technology company specializing in innovative solutions.
    
    ## About Us
    We are a mid-size company with 150 employees based in San Francisco, CA.
    
    ## Our Products
    - Cloud computing solutions
    - AI-powered analytics
    - Enterprise software
    
    ## Contact
    Email: contact@acme.com
    Phone: +1-555-123-4567
    
    ## Mission
    To revolutionize business operations through cutting-edge technology.
    """


@pytest.fixture
def sample_insights():
    """Sample business insights for testing."""
    return {
        "industry": "Technology",
        "company_size": "Medium (100-200 employees)",
        "location": "San Francisco, CA",
        "usp": "Revolutionizing business operations through cutting-edge technology",
        "products_services": "Cloud computing solutions, AI-powered analytics, Enterprise software",
        "target_audience": "Enterprise businesses seeking technology solutions",
        "contact_info": {
            "emails": ["contact@acme.com"],
            "phones": ["+1-555-123-4567"],
            "social_media": []
        }
    }


@pytest.fixture
def auth_headers():
    """Authorization headers for testing."""
    return {"Authorization": "Bearer test_secret_key"}
