import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from app.main import app


class TestAPIEndpoints:
    """Integration tests for API endpoints."""

    def setup_method(self):
        """Setup test client."""
        self.client = TestClient(app)
        self.auth_headers = {"Authorization": "Bearer test_secret_key"}

    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = self.client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data

    def test_root_endpoint(self):
        """Test root endpoint."""
        response = self.client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    @patch('app.services.scraper.scraper_service.scrape_website')
    @patch('app.services.llm.llm_service.extract_business_insights')
    @patch('app.services.database.db_service.store_website_analysis')
    def test_analyze_endpoint_success(self, mock_store, mock_extract, mock_scrape, 
                                    sample_website_content, sample_insights, auth_headers):
        """Test successful website analysis."""
        # Setup mocks
        mock_scrape.return_value = sample_website_content
        mock_extract.return_value = sample_insights
        mock_store.return_value = "test-analysis-id"
        
        payload = {"url": "https://example.com"}
        
        response = self.client.post("/api/analyze", json=payload, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["url"] == "https://example.com"
        assert data["insights"]["industry"] == "Technology"
        assert data["insights"]["company_size"] == "Medium (100-200 employees)"

    @patch('app.services.scraper.scraper_service.scrape_website')
    @patch('app.services.llm.llm_service.extract_business_insights')
    @patch('app.services.database.db_service.store_website_analysis')
    def test_analyze_endpoint_custom_questions(self, mock_store, mock_extract, mock_scrape,
                                             sample_website_content, auth_headers):
        """Test analysis with custom questions."""
        # Setup mocks
        mock_scrape.return_value = sample_website_content
        mock_extract.return_value = {"custom_answers": "The main product is cloud computing."}
        mock_store.return_value = "test-analysis-id"
        
        payload = {
            "url": "https://example.com",
            "questions": ["What is the main product?", "Who is the target audience?"]
        }
        
        response = self.client.post("/api/analyze", json=payload, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["url"] == "https://example.com"
        assert "cloud computing" in data["insights"]["products_services"]

    def test_analyze_endpoint_unauthorized(self):
        """Test analysis endpoint without authentication."""
        payload = {"url": "https://example.com"}
        
        response = self.client.post("/api/analyze", json=payload)
        
        assert response.status_code == 401

    def test_analyze_endpoint_invalid_url(self, auth_headers):
        """Test analysis endpoint with invalid URL."""
        payload = {"url": "not-a-valid-url"}
        
        response = self.client.post("/api/analyze", json=payload, headers=auth_headers)
        
        assert response.status_code == 422  # Validation error

    @patch('app.services.scraper.scraper_service.scrape_website')
    def test_analyze_endpoint_scraping_error(self, mock_scrape, auth_headers):
        """Test analysis endpoint with scraping error."""
        mock_scrape.side_effect = Exception("Scraping failed")
        
        payload = {"url": "https://example.com"}
        
        response = self.client.post("/api/analyze", json=payload, headers=auth_headers)
        
        assert response.status_code == 500
        data = response.json()
        assert "Analysis failed" in data["detail"]

    @patch('app.services.database.db_service.get_website_analysis')
    @patch('app.services.llm.llm_service.answer_conversational_query')
    @patch('app.services.database.db_service.store_conversation')
    @patch('app.services.database.db_service.get_conversation_history')
    def test_chat_endpoint_success(self, mock_history, mock_store_conv, mock_answer, 
                                 mock_get_analysis, sample_website_content, auth_headers):
        """Test successful chat endpoint."""
        # Setup mocks
        mock_get_analysis.return_value = {"raw_content": sample_website_content}
        mock_history.return_value = []
        mock_answer.return_value = "The main product is cloud computing solutions."
        mock_store_conv.return_value = "conv-id"
        
        payload = {
            "url": "https://example.com",
            "query": "What is the main product?"
        }
        
        response = self.client.post("/api/chat", json=payload, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "cloud computing solutions" in data["response"]

    @patch('app.services.database.db_service.get_website_analysis')
    def test_chat_endpoint_website_not_found(self, mock_get_analysis, auth_headers):
        """Test chat endpoint when website not analyzed."""
        mock_get_analysis.return_value = None
        
        payload = {
            "url": "https://example.com",
            "query": "What is the main product?"
        }
        
        response = self.client.post("/api/chat", json=payload, headers=auth_headers)
        
        assert response.status_code == 404
        data = response.json()
        assert "Website not found" in data["detail"]

    def test_chat_endpoint_unauthorized(self):
        """Test chat endpoint without authentication."""
        payload = {
            "url": "https://example.com",
            "query": "What is the main product?"
        }
        
        response = self.client.post("/api/chat", json=payload)
        
        assert response.status_code == 401

    @patch('app.services.database.db_service.get_website_analysis')
    @patch('app.services.llm.llm_service.answer_conversational_query')
    def test_chat_endpoint_llm_error(self, mock_answer, mock_get_analysis, 
                                   sample_website_content, auth_headers):
        """Test chat endpoint with LLM error."""
        mock_get_analysis.return_value = {"raw_content": sample_website_content}
        mock_answer.side_effect = Exception("LLM error")
        
        payload = {
            "url": "https://example.com",
            "query": "What is the main product?"
        }
        
        response = self.client.post("/api/chat", json=payload, headers=auth_headers)
        
        assert response.status_code == 500
        data = response.json()
        assert "Chat failed" in data["detail"]

    def test_rate_limiting(self, auth_headers):
        """Test rate limiting functionality."""
        payload = {"url": "https://example.com"}
        
        # Make multiple requests to test rate limiting
        responses = []
        for _ in range(15):  # Exceed the rate limit
            with patch('app.services.scraper.scraper_service.scrape_website'), \
                 patch('app.services.llm.llm_service.extract_business_insights'), \
                 patch('app.services.database.db_service.store_website_analysis'):
                response = self.client.post("/api/analyze", json=payload, headers=auth_headers)
                responses.append(response.status_code)
        
        # Should have some 429 responses due to rate limiting
        assert 429 in responses
