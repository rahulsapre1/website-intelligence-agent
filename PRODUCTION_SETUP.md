# Production Setup Guide

This document provides step-by-step instructions for deploying the Website Intelligence Agent to production using Render (backend) and Vercel (frontend).

## 📋 Prerequisites

- GitHub repository with the code
- Render account (free tier available)
- Vercel account (free tier available)
- API keys for external services:
  - Supabase (database)
  - Google Gemini (AI)
  - Jina AI (web scraping)

## 🚀 Step-by-Step Deployment

### Phase 1: Backend Deployment (Render)

#### 1.1 Prepare Repository
```bash
# Ensure all files are committed and pushed to GitHub
git add .
git commit -m "Ready for production deployment"
git push origin main
```

#### 1.2 Deploy to Render
1. Go to [render.com](https://render.com) and sign in
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Select your repository: `website-intelligence_v1`

#### 1.3 Configure Render Service
- **Name**: `website-intelligence-api`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Instance Type**: `Starter` (free tier)

#### 1.4 Set Environment Variables
In Render dashboard, go to "Environment" tab and add:
```
API_SECRET_KEY=your_secure_secret_key_here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key
GEMINI_API_KEY=your_google_gemini_api_key
JINA_API_KEY=your_jina_api_key
```

#### 1.5 Deploy
- Click "Create Web Service"
- Wait for deployment to complete
- Note the service URL (e.g., `https://website-intelligence-api.onrender.com`)

### Phase 2: Frontend Deployment (Vercel)

#### 2.1 Deploy to Vercel
1. Go to [vercel.com](https://vercel.com) and sign in
2. Click "New Project"
3. Import your GitHub repository
4. Select your repository: `website-intelligence_v1`

#### 2.2 Configure Vercel Project
- **Framework Preset**: `Next.js`
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `.next`

#### 2.3 Set Environment Variables
In Vercel dashboard, go to "Settings" → "Environment Variables":
```
NEXT_PUBLIC_API_URL=https://your-render-backend-url.onrender.com
```

#### 2.4 Deploy
- Click "Deploy"
- Wait for deployment to complete
- Note the frontend URL (e.g., `https://website-intelligence-agent.vercel.app`)

### Phase 3: Post-Deployment Configuration

#### 3.1 Test Backend API
```bash
# Test health endpoint
curl https://your-backend-url.onrender.com/health

# Test with API key
curl -H "Authorization: Bearer your_api_secret_key" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com"}' \
     https://your-backend-url.onrender.com/api/analyze
```

#### 3.2 Test Frontend
1. Visit your Vercel frontend URL
2. Enter your API secret key
3. Test website analysis functionality
4. Test chat functionality

#### 3.3 Update Documentation
Update `README.md` with production URLs:
```markdown
## Live Demo
- **Frontend**: https://your-frontend-url.vercel.app
- **Backend API**: https://your-backend-url.onrender.com
```

## 🔧 Configuration Details

### Backend Configuration (Render)
- **Runtime**: Python 3.11
- **Port**: Automatically assigned by Render
- **Auto-deploy**: Enabled (deploys on git push)
- **Health checks**: `/health` endpoint

### Frontend Configuration (Vercel)
- **Framework**: Next.js 15
- **Build optimization**: Automatic
- **CDN**: Global edge network
- **Custom domain**: Optional

## 🔒 Security Considerations

### API Security
- Use strong, unique API secret keys
- Rotate keys regularly
- Monitor API usage and rate limiting
- Implement CORS properly

### Environment Variables
- Never commit API keys to version control
- Use environment variables for all secrets
- Regularly rotate production keys
- Monitor for exposed credentials

## 📊 Monitoring & Maintenance

### Render Monitoring
- Check deployment logs regularly
- Monitor resource usage
- Set up alerts for downtime
- Review error logs

### Vercel Monitoring
- Monitor build success/failure
- Check deployment performance
- Review analytics
- Monitor Core Web Vitals

### Application Monitoring
- Test API endpoints regularly
- Monitor response times
- Check database connections
- Verify external API integrations

## 🆘 Troubleshooting

### Common Issues

**Backend Issues:**
- **Build failures**: Check requirements.txt and dependencies
- **Start failures**: Verify start command and port configuration
- **Environment errors**: Check all required environment variables are set
- **Database errors**: Verify Supabase connection and credentials

**Frontend Issues:**
- **Build failures**: Check Next.js configuration and dependencies
- **API connection errors**: Verify NEXT_PUBLIC_API_URL is correct
- **CORS errors**: Check backend CORS configuration
- **Environment errors**: Verify all environment variables are set

**API Issues:**
- **Authentication errors**: Verify API secret key matches
- **Rate limiting**: Check external API quotas
- **Timeout errors**: Check external API availability
- **Data errors**: Verify Supabase configuration

### Debugging Steps
1. Check deployment logs in respective platforms
2. Test API endpoints directly
3. Verify environment variables
4. Check external service status
5. Review application logs

## 📞 Support Resources

- **Render Documentation**: https://render.com/docs
- **Vercel Documentation**: https://vercel.com/docs
- **Next.js Documentation**: https://nextjs.org/docs
- **FastAPI Documentation**: https://fastapi.tiangolo.com

## ✅ Deployment Checklist

- [ ] Repository pushed to GitHub
- [ ] Backend deployed to Render
- [ ] Environment variables set in Render
- [ ] Backend health check passing
- [ ] Frontend deployed to Vercel
- [ ] Environment variables set in Vercel
- [ ] Frontend connected to backend
- [ ] Full application testing completed
- [ ] Documentation updated with URLs
- [ ] Monitoring configured
- [ ] Security review completed
