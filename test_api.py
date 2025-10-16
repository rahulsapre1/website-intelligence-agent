#!/usr/bin/env python3
"""
Simple test script for the Website Intelligence Agent API
Run this after starting the server to test the endpoints
"""

import requests
import json
import time
from typing import Dict, Any


class APITester:
    def __init__(self, base_url: str = "http://localhost:8000", api_key: str = None):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def test_health(self) -> bool:
        """Test health endpoint"""
        try:
            response = requests.get(f"{self.base_url}/health")
            print(f"✅ Health check: {response.status_code}")
            if response.status_code == 200:
                print(f"   Response: {response.json()}")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return False
    
    def test_analyze_website(self, url: str, questions: list = None) -> Dict[str, Any]:
        """Test website analysis endpoint"""
        try:
            data = {"url": url}
            if questions:
                data["questions"] = questions
            
            print(f"🔍 Analyzing website: {url}")
            response = requests.post(
                f"{self.base_url}/api/analyze",
                headers=self.headers,
                json=data
            )
            
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Analysis completed")
                print(f"   Insights: {json.dumps(result['insights'], indent=2)}")
                return result
            else:
                print(f"   ❌ Analysis failed: {response.text}")
                return {}
                
        except Exception as e:
            print(f"❌ Analysis error: {e}")
            return {}
    
    def test_chat(self, url: str, query: str) -> str:
        """Test chat endpoint"""
        try:
            data = {
                "url": url,
                "query": query
            }
            
            print(f"💬 Chat query: {query}")
            response = requests.post(
                f"{self.base_url}/api/chat",
                headers=self.headers,
                json=data
            )
            
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Response: {result['response']}")
                return result['response']
            else:
                print(f"   ❌ Chat failed: {response.text}")
                return ""
                
        except Exception as e:
            print(f"❌ Chat error: {e}")
            return ""


def main():
    print("🧪 Website Intelligence Agent API Tester")
    print("=" * 50)
    
    # Get API key from user
    api_key = input("Enter your API secret key: ").strip()
    if not api_key:
        print("❌ API key is required!")
        return
    
    tester = APITester(api_key=api_key)
    
    # Test health endpoint
    print("\n1. Testing health endpoint...")
    if not tester.test_health():
        print("❌ Health check failed. Make sure the server is running!")
        return
    
    # Test website analysis
    print("\n2. Testing website analysis...")
    test_url = "https://openai.com"  # Example website
    analysis_result = tester.test_analyze_website(test_url)
    
    if not analysis_result:
        print("❌ Website analysis failed!")
        return
    
    # Wait a moment for data to be stored
    print("\n⏳ Waiting for data to be stored...")
    time.sleep(2)
    
    # Test chat functionality
    print("\n3. Testing chat functionality...")
    chat_queries = [
        "What is the main product of this company?",
        "Who is their target audience?",
        "What makes them unique?"
    ]
    
    for query in chat_queries:
        tester.test_chat(test_url, query)
        print()
    
    print("🎉 Testing completed!")


if __name__ == "__main__":
    main()
