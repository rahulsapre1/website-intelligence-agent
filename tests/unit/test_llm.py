import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.llm import LLMService


class TestLLMService:
    """Unit tests for LLMService."""

    def setup_method(self):
        """Setup test instance."""
        self.llm = LLMService()

    @pytest.mark.asyncio
    async def test_extract_business_insights_default(self, sample_website_content, sample_insights):
        """Test extracting default business insights."""
        mock_response = MagicMock()
        mock_response.text = """
        {
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
        """
        
        with patch.object(self.llm.model, 'generate_content', return_value=mock_response):
            result = await self.llm.extract_business_insights(sample_website_content)
            
            assert result["industry"] == "Technology"
            assert result["company_size"] == "Medium (100-200 employees)"
            assert result["location"] == "San Francisco, CA"
            assert "contact@acme.com" in result["contact_info"]["emails"]

    @pytest.mark.asyncio
    async def test_extract_business_insights_custom_questions(self, sample_website_content):
        """Test extracting insights for custom questions."""
        custom_questions = ["What is the main product?", "Who is the target audience?"]
        
        mock_response = MagicMock()
        mock_response.text = "The main product is cloud computing solutions. The target audience is enterprise businesses."
        
        with patch.object(self.llm.model, 'generate_content', return_value=mock_response):
            result = await self.llm.extract_business_insights(sample_website_content, custom_questions)
            
            assert "custom_answers" in result
            assert "cloud computing solutions" in result["custom_answers"]

    @pytest.mark.asyncio
    async def test_extract_business_insights_json_parse_error(self, sample_website_content):
        """Test handling of JSON parse error."""
        mock_response = MagicMock()
        mock_response.text = "Invalid JSON response"
        
        with patch.object(self.llm.model, 'generate_content', return_value=mock_response):
            result = await self.llm.extract_business_insights(sample_website_content)
            
            assert "raw_analysis" in result
            assert result["raw_analysis"] == "Invalid JSON response"

    @pytest.mark.asyncio
    async def test_answer_conversational_query(self, sample_website_content):
        """Test conversational query answering."""
        query = "What is the main product?"
        conversation_history = [
            {"query": "What industry is this company in?", "response": "Technology industry."}
        ]
        
        mock_response = MagicMock()
        mock_response.text = "The main product is cloud computing solutions."
        
        with patch.object(self.llm.model, 'generate_content', return_value=mock_response):
            result = await self.llm.answer_conversational_query(
                sample_website_content, query, conversation_history
            )
            
            assert "cloud computing solutions" in result

    @pytest.mark.asyncio
    async def test_answer_conversational_query_no_history(self, sample_website_content):
        """Test conversational query without history."""
        query = "What is the company size?"
        
        mock_response = MagicMock()
        mock_response.text = "The company has 150 employees."
        
        with patch.object(self.llm.model, 'generate_content', return_value=mock_response):
            result = await self.llm.answer_conversational_query(sample_website_content, query)
            
            assert "150 employees" in result

    @pytest.mark.asyncio
    async def test_extract_business_insights_error(self, sample_website_content):
        """Test error handling in insight extraction."""
        with patch.object(self.llm.model, 'generate_content', side_effect=Exception("API Error")):
            with pytest.raises(Exception, match="Analysis error"):
                await self.llm.extract_business_insights(sample_website_content)

    @pytest.mark.asyncio
    async def test_answer_conversational_query_error(self, sample_website_content):
        """Test error handling in conversational query."""
        with patch.object(self.llm.model, 'generate_content', side_effect=Exception("API Error")):
            with pytest.raises(Exception, match="Conversation error"):
                await self.llm.answer_conversational_query(sample_website_content, "Test query")
