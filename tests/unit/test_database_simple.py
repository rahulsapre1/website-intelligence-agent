import pytest
from unittest.mock import patch, MagicMock
from app.services.database import DatabaseService


@pytest.fixture
def mock_db():
    """Create a mocked database service."""
    with patch('app.services.database.create_client') as mock_create:
        mock_supabase = MagicMock()
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_create.return_value = mock_supabase
        
        db = DatabaseService()
        db.mock_table = mock_table
        return db


class TestDatabaseService:
    """Unit tests for DatabaseService."""

    @pytest.mark.asyncio
    async def test_store_website_analysis_new(self, mock_db, sample_website_content, sample_insights):
        """Test storing new website analysis."""
        url = "https://example.com"
        
        # Mock no existing record
        mock_db.mock_table.select.return_value.eq.return_value.execute.return_value.data = []
        
        # Mock insert response
        mock_db.mock_table.insert.return_value.execute.return_value.data = [{"id": "test-id-123"}]
        
        result = await mock_db.store_website_analysis(url, sample_website_content, sample_insights)
        
        assert result == "test-id-123"
        mock_db.mock_table.insert.assert_called_once()

    @pytest.mark.asyncio
    async def test_store_website_analysis_update(self, mock_db, sample_website_content, sample_insights):
        """Test updating existing website analysis."""
        url = "https://example.com"
        
        # Mock existing record
        mock_db.mock_table.select.return_value.eq.return_value.execute.return_value.data = [{"id": "existing-id"}]
        
        result = await mock_db.store_website_analysis(url, sample_website_content, sample_insights)
        
        assert result == "existing-id"
        mock_db.mock_table.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_website_analysis_success(self, mock_db):
        """Test successful website analysis retrieval."""
        url = "https://example.com"
        mock_data = {"id": "test-id", "url": url, "raw_content": "test content"}
        
        mock_db.mock_table.select.return_value.eq.return_value.execute.return_value.data = [mock_data]
        
        result = await mock_db.get_website_analysis(url)
        
        assert result == mock_data

    @pytest.mark.asyncio
    async def test_get_website_analysis_not_found(self, mock_db):
        """Test website analysis not found."""
        url = "https://example.com"
        
        mock_db.mock_table.select.return_value.eq.return_value.execute.return_value.data = []
        
        result = await mock_db.get_website_analysis(url)
        
        assert result is None

    @pytest.mark.asyncio
    async def test_store_conversation(self, mock_db):
        """Test storing conversation."""
        url = "https://example.com"
        query = "What is the main product?"
        response = "Cloud computing solutions."
        
        mock_db.mock_table.insert.return_value.execute.return_value.data = [{"id": "conv-id-123"}]
        
        result = await mock_db.store_conversation(url, query, response)
        
        assert result == "conv-id-123"
        mock_db.mock_table.insert.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_conversation_history(self, mock_db):
        """Test getting conversation history."""
        url = "https://example.com"
        mock_conversations = [
            {"id": "1", "query": "What is the main product?", "response": "Cloud computing."},
            {"id": "2", "query": "Who is the target audience?", "response": "Enterprise businesses."}
        ]
        
        mock_db.mock_table.select.return_value.eq.return_value.order.return_value.limit.return_value.execute.return_value.data = mock_conversations
        
        result = await mock_db.get_conversation_history(url, limit=10)
        
        assert len(result) == 2
        assert result[0]["query"] == "What is the main product?"
