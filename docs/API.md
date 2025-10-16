# API Documentation

## Overview

The Website Intelligence Agent API provides two main endpoints for analyzing websites and having conversational interactions about them.

**Base URL**: `https://your-api-domain.com` (or `http://localhost:8000` for local development)

## Authentication

All API endpoints require authentication using a Bearer token in the Authorization header:

```
Authorization: Bearer YOUR_SECRET_KEY
```

## Rate Limiting

- **Limit**: 10 requests per minute per IP address
- **Headers**: Rate limit information is included in response headers
- **Exceeded**: Returns `429 Too Many Requests` when limit is exceeded

## Endpoints

### 1. Analyze Website

**Endpoint**: `POST /api/analyze`

**Description**: Analyze a website homepage and extract business insights.

**Request Body**:
```json
{
  "url": "https://example.com",
  "questions": ["What industry?", "Company size?"]  // Optional
}
```

**Parameters**:
- `url` (string, required): The website URL to analyze
- `questions` (array, optional): Custom questions to ask about the website

**Response**:
```json
{
  "url": "https://example.com",
  "insights": {
    "industry": "Technology",
    "company_size": "Medium (50-200 employees)",
    "location": "San Francisco, CA",
    "usp": "Revolutionizing business operations through cutting-edge technology",
    "products_services": "Cloud computing solutions, AI-powered analytics",
    "target_audience": "Enterprise businesses seeking technology solutions",
    "contact_info": {
      "emails": ["contact@example.com"],
      "phones": ["+1-555-123-4567"],
      "social_media": ["https://twitter.com/example"]
    }
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Default Insights** (when no custom questions provided):
- Industry classification
- Company size estimation
- Business location
- Unique selling proposition
- Core products/services
- Target audience
- Contact information

### 2. Chat About Website

**Endpoint**: `POST /api/chat`

**Description**: Ask conversational questions about a previously analyzed website.

**Request Body**:
```json
{
  "url": "https://example.com",
  "query": "What is their pricing model?",
  "conversation_history": [  // Optional
    {
      "query": "What industry are they in?",
      "response": "They are in the technology industry."
    }
  ]
}
```

**Parameters**:
- `url` (string, required): The previously analyzed website URL
- `query` (string, required): The question to ask
- `conversation_history` (array, optional): Previous conversation context

**Response**:
```json
{
  "response": "Based on the website content, their pricing model appears to be subscription-based with tiered plans for different business sizes. They offer a free tier for small teams and enterprise plans for larger organizations.",
  "timestamp": "2024-01-15T10:35:00Z"
}
```

### 3. Health Check

**Endpoint**: `GET /health`

**Description**: Check API health and status.

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0"
}
```

## Error Responses

### 401 Unauthorized
```json
{
  "error": "Invalid authentication credentials",
  "detail": "Invalid authentication credentials"
}
```

### 404 Not Found
```json
{
  "error": "Website not found",
  "detail": "Website not found. Please analyze the website first using /api/analyze"
}
```

### 429 Too Many Requests
```json
{
  "error": "Rate limit exceeded",
  "detail": "Rate limit exceeded. Try again later."
}
```

### 422 Validation Error
```json
{
  "error": "Validation error",
  "detail": [
    {
      "loc": ["body", "url"],
      "msg": "invalid or missing URL scheme",
      "type": "value_error.url.scheme"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "detail": "Analysis failed: Unable to scrape website"
}
```

## Usage Examples

### Python Example

```python
import requests
import json

# Configuration
API_URL = "https://your-api-domain.com"
API_KEY = "your_secret_key_here"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Analyze a website
def analyze_website(url, questions=None):
    data = {"url": url}
    if questions:
        data["questions"] = questions
    
    response = requests.post(f"{API_URL}/api/analyze", headers=headers, json=data)
    return response.json()

# Chat about a website
def chat_about_website(url, query, history=None):
    data = {
        "url": url,
        "query": query
    }
    if history:
        data["conversation_history"] = history
    
    response = requests.post(f"{API_URL}/api/chat", headers=headers, json=data)
    return response.json()

# Example usage
website_url = "https://openai.com"

# Analyze the website
analysis = analyze_website(website_url)
print("Industry:", analysis["insights"]["industry"])
print("Company Size:", analysis["insights"]["company_size"])

# Ask a follow-up question
chat_response = chat_about_website(website_url, "What is their main product?")
print("Answer:", chat_response["response"])
```

### JavaScript Example

```javascript
const API_URL = 'https://your-api-domain.com';
const API_KEY = 'your_secret_key_here';

const headers = {
  'Authorization': `Bearer ${API_KEY}`,
  'Content-Type': 'application/json'
};

// Analyze a website
async function analyzeWebsite(url, questions = null) {
  const data = { url };
  if (questions) data.questions = questions;
  
  const response = await fetch(`${API_URL}/api/analyze`, {
    method: 'POST',
    headers,
    body: JSON.stringify(data)
  });
  
  return await response.json();
}

// Chat about a website
async function chatAboutWebsite(url, query, history = null) {
  const data = { url, query };
  if (history) data.conversation_history = history;
  
  const response = await fetch(`${API_URL}/api/chat`, {
    method: 'POST',
    headers,
    body: JSON.stringify(data)
  });
  
  return await response.json();
}

// Example usage
const websiteUrl = 'https://openai.com';

analyzeWebsite(websiteUrl)
  .then(analysis => {
    console.log('Industry:', analysis.insights.industry);
    console.log('Company Size:', analysis.insights.company_size);
    
    return chatAboutWebsite(websiteUrl, 'What is their main product?');
  })
  .then(chatResponse => {
    console.log('Answer:', chatResponse.response);
  })
  .catch(error => {
    console.error('Error:', error);
  });
```

### cURL Examples

```bash
# Analyze a website
curl -X POST https://your-api-domain.com/api/analyze \
  -H "Authorization: Bearer YOUR_SECRET_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

# Analyze with custom questions
curl -X POST https://your-api-domain.com/api/analyze \
  -H "Authorization: Bearer YOUR_SECRET_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "questions": ["What is their pricing model?", "Who are their competitors?"]
  }'

# Chat about a website
curl -X POST https://your-api-domain.com/api/chat \
  -H "Authorization: Bearer YOUR_SECRET_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "query": "What makes them unique?"
  }'

# Health check
curl https://your-api-domain.com/health
```

## Interactive Documentation

When running the API locally, visit `http://localhost:8000/docs` for interactive Swagger/OpenAPI documentation where you can test endpoints directly in the browser.
