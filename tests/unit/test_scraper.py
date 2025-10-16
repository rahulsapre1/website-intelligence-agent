import pytest
from unittest.mock import AsyncMock, patch
from app.services.scraper import ScraperService


class TestScraperService:
    """Unit tests for ScraperService."""

    def setup_method(self):
        """Setup test instance."""
        self.scraper = ScraperService()

    @pytest.mark.asyncio
    async def test_scrape_website_success(self, sample_website_content):
        """Test successful website scraping."""
        url = "https://example.com"
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.text = sample_website_content
            mock_response.raise_for_status = AsyncMock()
            
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            result = await self.scraper.scrape_website(url)
            
            assert result == sample_website_content
            mock_client.return_value.__aenter__.return_value.get.assert_called_once_with(
                f"https://r.jina.ai/{url}"
            )
            mock_response.raise_for_status.assert_called_once()

    @pytest.mark.asyncio
    async def test_scrape_website_timeout(self):
        """Test scraping timeout error."""
        url = "https://example.com"
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.side_effect = Exception("Timeout")
            
            with pytest.raises(Exception, match="Scraping error"):
                await self.scraper.scrape_website(url)

    @pytest.mark.asyncio
    async def test_scrape_website_insufficient_content(self):
        """Test scraping with insufficient content."""
        url = "https://example.com"
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.text = "Short content"  # Less than 100 characters
            mock_response.raise_for_status = AsyncMock()
            
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            with pytest.raises(Exception, match="Insufficient content"):
                await self.scraper.scrape_website(url)
            mock_response.raise_for_status.assert_called_once()

    @pytest.mark.asyncio
    async def test_scrape_website_http_error(self):
        """Test scraping with HTTP error."""
        url = "https://example.com"
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.raise_for_status.side_effect = Exception("HTTP 404")
            
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            with pytest.raises(Exception, match="Scraping error"):
                await self.scraper.scrape_website(url)
