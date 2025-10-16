# System Architecture

## Overview

The Website Intelligence Agent is a modern, AI-powered system that extracts business insights from website homepages using cutting-edge web scraping and large language models.

## Architecture Diagram

```mermaid
graph TB
    %% User Interface Layer
    subgraph "Frontend Layer"
        UI[Next.js Web App<br/>shadcn/ui Components]
        USER[User]
    end
    
    %% API Gateway Layer
    subgraph "API Layer"
        API[FastAPI Backend<br/>Authentication & Rate Limiting]
        AUTH[Bearer Token Auth]
        RATE[Rate Limiting<br/>10 req/min per IP]
    end
    
    %% Core Services Layer
    subgraph "Core Services"
        SCRAPER[Jina AI Reader Service<br/>Web Scraping]
        LLM[Gemini 2.5 Flash<br/>AI Analysis & Chat]
        DB[Supabase Database<br/>PostgreSQL]
    end
    
    %% External Services
    subgraph "External Services"
        JINA[Jina AI Reader API<br/>https://r.jina.ai/]
        GEMINI[Google Gemini API<br/>AI Processing]
        SUPABASE[Supabase Cloud<br/>Database Hosting]
    end
    
    %% Data Flow
    USER -->|1. Input URL| UI
    UI -->|2. POST /api/analyze| API
    API --> AUTH
    API --> RATE
    API -->|3. Scrape Content| SCRAPER
    SCRAPER -->|4. GET Content| JINA
    JINA -->|5. Clean HTML/Text| SCRAPER
    SCRAPER -->|6. Store Raw Content| DB
    SCRAPER -->|7. Analyze Content| LLM
    LLM -->|8. AI Processing| GEMINI
    GEMINI -->|9. Insights JSON| LLM
    LLM -->|10. Update Insights| DB
    API -->|11. Return Insights| UI
    
    %% Chat Flow
    USER -->|12. Ask Question| UI
    UI -->|13. POST /api/chat| API
    API -->|14. Get Website Data| DB
    DB -->|15. Raw Content| API
    API -->|16. Chat Query| LLM
    LLM -->|17. AI Response| GEMINI
    GEMINI -->|18. Answer| LLM
    LLM -->|19. Store Chat| DB
    API -->|20. Return Answer| UI
    
    %% Database Tables
    subgraph "Database Schema"
        WA[website_analyses<br/>url, raw_content, insights, timestamp]
        CONV[conversations<br/>url, query, response, timestamp]
    end
    
    DB --> WA
    DB --> CONV
    SUPABASE --> DB
    
    %% Styling
    classDef frontend fill:#e1f5fe
    classDef api fill:#f3e5f5
    classDef services fill:#e8f5e8
    classDef external fill:#fff3e0
    classDef database fill:#fce4ec
    
    class UI,USER frontend
    class API,AUTH,RATE api
    class SCRAPER,LLM,DB services
    class JINA,GEMINI,SUPABASE external
    class WA,CONV database
```

## Data Flow Architecture

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant A as FastAPI
    participant S as Scraper Service
    participant J as Jina AI
    participant L as LLM Service
    participant G as Gemini API
    participant D as Supabase DB
    
    %% Analysis Flow
    U->>F: 1. Enter Website URL
    F->>A: 2. POST /api/analyze
    A->>A: 3. Validate Auth & Rate Limit
    A->>S: 4. Scrape Website
    S->>J: 5. GET https://r.jina.ai/{url}
    J->>S: 6. Return Clean Content
    S->>D: 7. Store Raw Content
    A->>L: 8. Extract Insights
    L->>G: 9. Process with AI
    G->>L: 10. Return Structured Insights
    L->>D: 11. Update with Insights
    A->>F: 12. Return Analysis JSON
    F->>U: 13. Display Insights
    
    %% Chat Flow
    U->>F: 14. Ask Question
    F->>A: 15. POST /api/chat
    A->>A: 16. Validate Auth & Rate Limit
    A->>D: 17. Get Website Data
    D->>A: 18. Return Raw Content
    A->>L: 19. Answer Question
    L->>G: 20. Process Query
    G->>L: 21. Return Answer
    L->>D: 22. Store Conversation
    A->>F: 23. Return Answer
    F->>U: 24. Display Response
```

## Component Architecture

```mermaid
graph LR
    subgraph "FastAPI Application"
        MAIN[app/main.py<br/>FastAPI App]
        CONFIG[app/config.py<br/>Settings]
        AUTH[app/utils/auth.py<br/>Authentication]
        SCHEMAS[app/models/schemas.py<br/>Pydantic Models]
    end
    
    subgraph "Service Layer"
        SCRAPER[app/services/scraper.py<br/>Web Scraping]
        LLM[app/services/llm.py<br/>AI Processing]
        DATABASE[app/services/database.py<br/>Data Persistence]
    end
    
    subgraph "Testing"
        UNIT[tests/unit/<br/>Unit Tests]
        INTEGRATION[tests/integration/<br/>Integration Tests]
    end
    
    MAIN --> CONFIG
    MAIN --> AUTH
    MAIN --> SCHEMAS
    MAIN --> SCRAPER
    MAIN --> LLM
    MAIN --> DATABASE
    
    UNIT --> SCRAPER
    UNIT --> LLM
    UNIT --> DATABASE
    INTEGRATION --> MAIN
    
    %% External Dependencies
    SCRAPER -.->|HTTP| JINA[Jina AI Reader]
    LLM -.->|API| GEMINI[Google Gemini]
    DATABASE -.->|Client| SUPABASE[Supabase]
```

## Technology Stack Justification

### Backend Framework: FastAPI
- **Async Performance**: Non-blocking I/O for high concurrency
- **Auto Documentation**: Built-in OpenAPI/Swagger docs
- **Type Safety**: Pydantic integration for request/response validation
- **Modern Python**: Built for Python 3.7+ with async/await support
- **Easy Testing**: TestClient for integration testing

### Web Scraping: Jina AI Reader
- **Free Service**: No cost for reasonable usage limits
- **JavaScript Support**: Handles SPA and dynamic content
- **Clean Output**: Returns LLM-friendly markdown/text
- **Reliability**: No complex scraping infrastructure needed
- **Simple Integration**: Just prepend URL with `https://r.jina.ai/`

### AI Model: Google Gemini 2.5 Flash
- **Speed**: Optimized for fast response times
- **Cost-Effective**: Generous free tier, affordable pricing
- **Quality**: State-of-the-art language understanding
- **Structured Output**: JSON mode for consistent responses
- **Multimodal**: Can handle text, images, and documents

### Database: Supabase
- **PostgreSQL**: Robust, ACID-compliant database
- **Real-time**: Built-in real-time subscriptions
- **Easy Setup**: Managed service with simple configuration
- **REST API**: Auto-generated REST endpoints
- **Authentication**: Built-in auth system (not used in this project)

### Frontend: Next.js + shadcn/ui
- **React Framework**: Server-side rendering and static generation
- **Modern UI**: shadcn/ui provides beautiful, accessible components
- **TypeScript**: Type safety and better developer experience
- **Vercel Deployment**: Seamless deployment and hosting
- **Responsive**: Mobile-first, responsive design
