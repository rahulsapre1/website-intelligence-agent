import google.generativeai as genai
from typing import Dict, Any, Optional, List
from app.config import settings
import json
import logging

logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self):
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
    
    async def extract_business_insights(self, content: str, custom_questions: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Extract business insights from website content using Gemini 2.5 Flash
        """
        try:
            if custom_questions:
                # Handle custom questions
                questions_text = "\n".join([f"- {q}" for q in custom_questions])
                prompt = f"""
                You are a business intelligence analyst. Analyze the following website content and answer the specific questions provided.

                Website Content:
                {content}

                Questions to answer:
                {questions_text}

                Please provide detailed, accurate answers based on the content. If information is not available, state "Not specified" or "Cannot be determined from the content".
                """
            else:
                # Extract default 7 core insights
                prompt = f"""
                You are a business intelligence analyst. Analyze the following website content and extract key business insights.

                Website Content:
                {content}

                Please extract and provide the following information in JSON format:
                {{
                    "industry": "Primary industry/sector (infer if not explicitly stated)",
                    "company_size": "Approximate size (small/medium/large or employee count range if mentioned)",
                    "location": "Headquarters or primary location (if mentioned)",
                    "usp": "Unique Selling Proposition - what makes this company stand out",
                    "products_services": "Concise summary of main offerings",
                    "target_audience": "Primary customer demographic (infer from content)",
                    "contact_info": {{
                        "emails": ["list of email addresses found"],
                        "phones": ["list of phone numbers found"],
                        "social_media": ["list of social media links found"]
                    }}
                }}

                Rules:
                - Use "Not specified" if information is not available
                - Make reasonable inferences based on content context
                - Keep answers concise but informative
                - Extract contact information accurately
                - Return valid JSON only
                """
            
            response = self.model.generate_content(prompt)
            
            if custom_questions:
                # Return custom Q&A format
                return {"custom_answers": response.text}
            else:
                # Parse JSON response for default insights
                try:
                    # Clean the response text to extract JSON
                    response_text = response.text.strip()
                    if response_text.startswith('```json'):
                        response_text = response_text[7:]
                    if response_text.endswith('```'):
                        response_text = response_text[:-3]
                    
                    insights = json.loads(response_text)
                    return insights
                except json.JSONDecodeError:
                    logger.warning("Failed to parse JSON response, returning raw text")
                    return {"raw_analysis": response.text}
                    
        except Exception as e:
            logger.error(f"LLM analysis error: {str(e)}")
            raise Exception(f"Analysis error: {str(e)}")
    
    async def answer_conversational_query(
        self, 
        content: str, 
        query: str, 
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Answer conversational questions about website content
        """
        try:
            # Build conversation context
            context = f"Website Content:\n{content}\n\n"
            
            if conversation_history:
                context += "Previous Conversation:\n"
                for msg in conversation_history:
                    context += f"User: {msg.get('query', '')}\n"
                    context += f"Assistant: {msg.get('response', '')}\n"
                context += "\n"
            
            context += f"Current Question: {query}\n\n"
            
            prompt = f"""
            You are a helpful assistant that answers questions about websites based on their content.
            
            {context}
            
            Please provide a helpful, accurate answer based on the website content and conversation history.
            If the information is not available in the content, clearly state that.
            Be conversational and informative in your response.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"LLM conversation error: {str(e)}")
            raise Exception(f"Conversation error: {str(e)}")


# Global LLM service instance
llm_service = LLMService()
