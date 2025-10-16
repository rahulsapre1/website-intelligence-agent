from supabase import create_client, Client
from app.config import settings
from typing import Optional, Dict, Any
import json


class DatabaseService:
    def __init__(self):
        self.supabase: Client = create_client(
            settings.supabase_url, 
            settings.supabase_key
        )
    
    async def store_website_analysis(
        self, 
        url: str, 
        raw_content: str, 
        insights: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Store website analysis data in Supabase
        Returns the record ID
        """
        try:
            # Check if URL already exists
            existing = self.supabase.table("website_analyses").select("id").eq("url", url).execute()
            
            data = {
                "url": url,
                "raw_content": raw_content,
                "insights": insights
            }
            
            if existing.data:
                # Update existing record
                result = self.supabase.table("website_analyses").update(data).eq("url", url).execute()
                return existing.data[0]["id"]
            else:
                # Insert new record
                result = self.supabase.table("website_analyses").insert(data).execute()
                return result.data[0]["id"]
                
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")
    
    async def get_website_analysis(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve website analysis data from Supabase
        """
        try:
            result = self.supabase.table("website_analyses").select("*").eq("url", url).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")
    
    async def store_conversation(
        self, 
        url: str, 
        query: str, 
        response: str
    ) -> str:
        """
        Store conversation data in Supabase
        Returns the record ID
        """
        try:
            data = {
                "url": url,
                "query": query,
                "response": response
            }
            
            result = self.supabase.table("conversations").insert(data).execute()
            return result.data[0]["id"]
            
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")
    
    async def get_conversation_history(self, url: str, limit: int = 10) -> list:
        """
        Get recent conversation history for a URL
        """
        try:
            result = self.supabase.table("conversations").select("*").eq("url", url).order("created_at", desc=True).limit(limit).execute()
            return result.data if result.data else []
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")


# Global database service instance
db_service = DatabaseService()
