# Deployment Guide

## Quick Start (Development)

1. **Setup Environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

2. **Setup Database:**
   - Run `sql/setup_tables.sql` in your Supabase SQL editor

3. **Start Application:**
   ```bash
   ./start.sh
   ```

## Production Deployment

### Option 1: Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t website-intelligence-agent .
docker run -p 8000:8000 --env-file .env website-intelligence-agent
```

### Option 2: Railway Deployment

1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Railway will auto-deploy on push

### Option 3: Heroku Deployment

1. Create `Procfile`:
   ```
   web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

2. Deploy:
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

## Environment Variables (Production)

Required environment variables:
- `GEMINI_API_KEY`: Your Google Gemini API key
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase anon key
- `API_SECRET_KEY`: Secure secret for API authentication
- `RATE_LIMIT_PER_MINUTE`: Rate limit (default: 10)

## Security Considerations

1. **API Secret Key**: Use a strong, random secret key
2. **CORS**: Configure `allow_origins` in production
3. **Rate Limiting**: Adjust limits based on your needs
4. **Environment Variables**: Never commit `.env` files

## Monitoring

- Health check endpoint: `GET /health`
- API documentation: `GET /docs`
- Logs are configured for production monitoring

## Scaling

- Use a proper database connection pool for Supabase
- Consider implementing Redis for rate limiting at scale
- Use a reverse proxy (nginx) for production
- Monitor API usage and adjust rate limits accordingly
