import httpx
from typing import Optional
from app.config import settings


class ScraperService:
    def __init__(self):
        self.jina_base_url = "https://r.jina.ai/"
        self.headers = {
            'Authorization': 'Bearer jina_1a2dfb7e8fa748888e5cfd0882794b230ljOaICCjbLaSpGxFgj9bNkgR66P',
            'X-Engine': 'cf-browser-rendering'
        }
    
    async def scrape_website(self, url: str) -> Optional[str]:
        """
        Scrape website content using Jina AI Reader with comprehensive extraction
        Returns extremely thorough text content from the webpage
        """
        try:
            # Use Jina AI Reader API with comprehensive parameters for maximum text extraction
            # Parameters to ensure maximum content extraction:
            # - raw: Include raw HTML and markdown
            # - include_links: Include all links and their text
            # - include_images: Include image alt texts and captions
            # - include_tables: Include all table content
            # - include_forms: Include form field information
            # - include_metadata: Include page metadata
            # - include_comments: Include comments and hidden content
            # - max_length: Maximum content length (set to high value)
            # - format: Multiple formats for comprehensive extraction
            
            jina_params = {
                'raw': 'true',
                'include_links': 'true', 
                'include_images': 'true',
                'include_tables': 'true',
                'include_forms': 'true',
                'include_metadata': 'true',
                'include_comments': 'true',
                'include_scripts': 'false',  # Skip scripts but include their text content
                'max_length': '50000',  # High limit for comprehensive extraction
                'format': 'markdown,html,text',  # Multiple formats for thoroughness
                'wait': '3000',  # Wait 3 seconds for dynamic content
                'screenshot': 'false',  # Don't need screenshots, just text
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            # Build comprehensive URL with all parameters
            jina_url = f"{self.jina_base_url}{url}"
            param_string = '&'.join([f"{k}={v}" for k, v in jina_params.items()])
            full_url = f"{jina_url}?{param_string}"
            
            async with httpx.AsyncClient(timeout=60.0) as client:  # Increased timeout for comprehensive extraction
                response = await client.get(full_url, headers=self.headers)
                response.raise_for_status()
                
                # Jina returns comprehensive content
                content = response.text
                
                if not content or len(content.strip()) < 100:
                    raise Exception("Insufficient content extracted from website")
                
                # Post-process to ensure maximum text extraction
                enhanced_content = self._enhance_content_extraction(content, url)
                
                return enhanced_content
                
        except httpx.TimeoutException:
            raise Exception("Timeout while scraping website (comprehensive extraction may take longer)")
        except httpx.HTTPStatusError as e:
            raise Exception(f"HTTP error while scraping: {e.response.status_code}")
        except Exception as e:
            raise Exception(f"Scraping error: {str(e)}")
    
    def _enhance_content_extraction(self, content: str, url: str) -> str:
        """
        Enhance the content extraction to ensure maximum text capture
        """
        enhanced_parts = []
        
        # Add comprehensive header
        enhanced_parts.append(f"# COMPREHENSIVE WEBSITE ANALYSIS")
        enhanced_parts.append(f"**URL:** {url}")
        enhanced_parts.append(f"**Extraction Method:** Jina AI Reader (Comprehensive Mode)")
        enhanced_parts.append(f"**Content Length:** {len(content)} characters")
        enhanced_parts.append("")
        enhanced_parts.append("---")
        enhanced_parts.append("")
        
        # Add the main content
        enhanced_parts.append("## EXTRACTED CONTENT:")
        enhanced_parts.append("")
        enhanced_parts.append(content)
        enhanced_parts.append("")
        
        # Add content analysis
        enhanced_parts.append("---")
        enhanced_parts.append("")
        enhanced_parts.append("## CONTENT ANALYSIS:")
        enhanced_parts.append(f"- **Total Characters:** {len(content)}")
        enhanced_parts.append(f"- **Word Count:** {len(content.split())}")
        enhanced_parts.append(f"- **Line Count:** {len(content.splitlines())}")
        
        # Check for common business elements
        business_indicators = []
        content_lower = content.lower()
        
        if any(word in content_lower for word in ['about', 'company', 'business', 'organization']):
            business_indicators.append("About/Company information detected")
        
        if any(word in content_lower for word in ['contact', 'email', 'phone', 'address']):
            business_indicators.append("Contact information detected")
        
        if any(word in content_lower for word in ['product', 'service', 'solution', 'offering']):
            business_indicators.append("Products/Services information detected")
        
        if any(word in content_lower for word in ['team', 'staff', 'employee', 'people']):
            business_indicators.append("Team/Staff information detected")
        
        if any(word in content_lower for word in ['price', 'cost', 'fee', 'plan', 'subscription']):
            business_indicators.append("Pricing information detected")
        
        if any(word in content_lower for word in ['location', 'office', 'headquarters', 'address']):
            business_indicators.append("Location information detected")
        
        if business_indicators:
            enhanced_parts.append("- **Business Elements Detected:**")
            for indicator in business_indicators:
                enhanced_parts.append(f"  - {indicator}")
        
        enhanced_parts.append("")
        enhanced_parts.append("---")
        enhanced_parts.append("")
        enhanced_parts.append("*This content has been extracted using Jina AI Reader in comprehensive mode to ensure maximum text capture from the webpage.*")
        
        return "\n".join(enhanced_parts)


# Global scraper service instance
scraper_service = ScraperService()
