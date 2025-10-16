#!/usr/bin/env python3
"""
Example usage of the Website Intelligence Agent API
This script demonstrates how to use the API programmatically
"""

import requests
import json
from typing import Dict, Any


def analyze_website(api_url: str, api_key: str, website_url: str, custom_questions: list = None) -> Dict[str, Any]:
    """
    Analyze a website and extract business insights
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {"url": website_url}
    if custom_questions:
        data["questions"] = custom_questions
    
    response = requests.post(f"{api_url}/api/analyze", headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Analysis failed: {response.status_code} - {response.text}")


def chat_about_website(api_url: str, api_key: str, website_url: str, query: str) -> str:
    """
    Ask a conversational question about a website
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "url": website_url,
        "query": query
    }
    
    response = requests.post(f"{api_url}/api/chat", headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()["response"]
    else:
        raise Exception(f"Chat failed: {response.status_code} - {response.text}")


def main():
    # Configuration
    API_URL = "http://localhost:8000"  # Change this to your deployed URL
    API_KEY = "your_secret_key_here"   # Change this to your actual API key
    
    # Example website to analyze
    website_url = "https://openai.com"
    
    print("🚀 Website Intelligence Agent - Example Usage")
    print("=" * 50)
    
    try:
        # Step 1: Analyze the website (default insights)
        print(f"\n📊 Analyzing {website_url}...")
        analysis = analyze_website(API_URL, API_KEY, website_url)
        
        print("✅ Analysis completed!")
        print(f"Industry: {analysis['insights'].get('industry', 'N/A')}")
        print(f"Company Size: {analysis['insights'].get('company_size', 'N/A')}")
        print(f"Location: {analysis['insights'].get('location', 'N/A')}")
        print(f"USP: {analysis['insights'].get('usp', 'N/A')}")
        
        # Step 2: Ask custom questions
        print(f"\n❓ Asking custom questions...")
        custom_analysis = analyze_website(
            API_URL, 
            API_KEY, 
            website_url, 
            custom_questions=[
                "What is their main product or service?",
                "What is their pricing model?",
                "Who are their main competitors?"
            ]
        )
        
        print("✅ Custom analysis completed!")
        print(f"Custom Answers: {custom_analysis['insights'].get('products_services', 'N/A')}")
        
        # Step 3: Chat about the website
        print(f"\n💬 Chatting about the website...")
        
        chat_questions = [
            "What makes this company unique?",
            "What is their target market?",
            "How do they make money?",
            "What are their key features?"
        ]
        
        for question in chat_questions:
            print(f"\nQ: {question}")
            answer = chat_about_website(API_URL, API_KEY, website_url, question)
            print(f"A: {answer}")
        
        print("\n🎉 Example completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure:")
        print("1. The server is running (./start.sh)")
        print("2. Your API key is correct")
        print("3. Your environment variables are set")


if __name__ == "__main__":
    main()
