# Deployment Guide - Website Intelligence Agent

This guide covers deploying the Website Intelligence Agent to production using **Render** (backend) and **Vercel** (frontend).

## 🚀 Backend Deployment (Render)

### 1. Prepare for Render Deployment

The project includes:
- `render.yaml` - Render configuration
- `Dockerfile` - Container configuration
- Environment variables setup

### 2. Deploy to Render

#### Option A: Using Render Dashboard
1. Go to [render.com](https://render.com) and sign in
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `website-intelligence-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Starter (free tier) or higher

#### Option B: Using render.yaml
1. Push `render.yaml` to your repository
2. Render will automatically detect and deploy

### 3. Environment Variables (Render)

Set these in Render dashboard under "Environment":
```
API_SECRET_KEY=your_secret_key_here
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
GEMINI_API_KEY=your_gemini_api_key
JINA_API_KEY=your_jina_api_key
```

### 4. Get Backend URL
After deployment, Render provides a URL like:
```
https://website-intelligence-api.onrender.com
```

---

## 🌐 Frontend Deployment (Vercel)

### 1. Prepare Frontend

The frontend is ready with:
- Next.js configuration
- Environment variables setup
- Production build optimization

### 2. Deploy to Vercel

#### Option A: Using Vercel CLI
```bash
cd frontend
npm install -g vercel
vercel --prod
```

#### Option B: Using Vercel Dashboard
1. Go to [vercel.com](https://vercel.com) and sign in
2. Click "New Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

### 3. Environment Variables (Vercel)

Set these in Vercel dashboard:
```
NEXT_PUBLIC_API_URL=https://website-intelligence-api.onrender.com
```

### 4. Get Frontend URL
After deployment, Vercel provides a URL like:
```
https://website-intelligence-agent.vercel.app
```

---

## 🔧 Post-Deployment Configuration

### 1. Update Frontend API URL
Update the frontend environment variable to point to your deployed backend:
```env
NEXT_PUBLIC_API_URL=https://your-backend-url.onrender.com
```

### 2. Test the Deployment
1. Visit your Vercel frontend URL
2. Enter your API secret key
3. Test website analysis functionality
4. Test chat functionality

### 3. CORS Configuration
If you encounter CORS issues, ensure your backend allows your frontend domain.

---

## 📊 Monitoring & Maintenance

### Render (Backend)
- Monitor logs in Render dashboard
- Set up alerts for downtime
- Monitor resource usage

### Vercel (Frontend)
- Monitor deployments in Vercel dashboard
- Set up custom domain if needed
- Monitor performance metrics

---

## 🔄 CI/CD Integration

The project includes GitHub Actions for:
- Automated testing
- Code quality checks
- Automatic deployments (optional)

To enable automatic deployments:
1. Set up secrets in GitHub repository
2. Update workflow files with deployment steps
3. Configure branch protection rules

---

## 🆘 Troubleshooting

### Common Issues

**Backend Issues:**
- Check environment variables are set correctly
- Verify all dependencies are in requirements.txt
- Check Render logs for error messages

**Frontend Issues:**
- Verify NEXT_PUBLIC_API_URL points to correct backend
- Check Vercel build logs
- Ensure all dependencies are in package.json

**API Issues:**
- Verify API secret key matches between frontend and backend
- Check CORS configuration
- Verify all external API keys are valid

### Support
- Check Render documentation: https://render.com/docs
- Check Vercel documentation: https://vercel.com/docs
- Review project README.md for additional setup details
