# Vercel Deployment Troubleshooting Guide

## Current Issue
Vercel is not detecting the Next.js app directory correctly, showing:
```
Error: > Couldn't find any `pages` or `app` directory. Please create one under the project root
```

## Solutions Applied

### Solution 1: Root Directory Configuration
- Added root `vercel.json` to explicitly specify frontend directory
- Updated `.vercelignore` to include only frontend directory
- Enhanced frontend `vercel.json` with proper Next.js configuration

### Solution 2: Alternative Approach (if Solution 1 fails)

If the current approach doesn't work, try this:

1. **In Vercel Dashboard:**
   - Go to Project Settings → General
   - Set Root Directory to `frontend`
   - Save changes

2. **Alternative Configuration:**
   - Remove root `vercel.json`
   - Keep only `frontend/vercel.json`
   - Ensure `.vercelignore` excludes all non-frontend files

### Solution 3: Manual Project Structure (if needed)

If Vercel still doesn't detect the app correctly:

1. **Create a new Vercel project:**
   - Import from GitHub
   - Select the repository
   - **Manually set Root Directory to `frontend`**
   - **Override Build Command:** `cd frontend && npm run build`
   - **Override Output Directory:** `frontend/.next`

2. **Environment Variables:**
   - Add any required environment variables
   - Ensure `NEXT_PUBLIC_API_URL` is set if needed

## Verification Steps

1. **Check Build Logs:**
   - Look for "Installing dependencies" from frontend directory
   - Verify "Building Next.js app" message
   - Check for successful build completion

2. **Test Deployment:**
   - Visit the deployed URL
   - Verify the frontend loads correctly
   - Test API connectivity if applicable

## Common Issues and Fixes

### Issue: Still getting "Couldn't find pages or app directory"
**Fix:** Ensure the root directory is correctly set in Vercel dashboard

### Issue: Build fails with module not found errors
**Fix:** Check that `node_modules` is properly excluded from git

### Issue: Deployment succeeds but app doesn't load
**Fix:** Check environment variables and API URLs

## Current Configuration Files

### Root `vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/next"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "frontend/$1"
    }
  ]
}
```

### Frontend `vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/next"
    }
  ]
}
```

### `.vercelignore`:
```
# Backend files - not needed for frontend deployment
app/
tests/
sql/
requirements.txt
Dockerfile
render.yaml
start.sh
run_tests.py
pytest.ini
.env
.env.example
.gitignore
README.md
DEPLOYMENT_GUIDE.md
PRODUCTION_SETUP.md
GITHUB_SETUP.md
CONTRIBUTING.md
LICENSE
website-intelligence-agent.plan.md
docs/
.github/
scripts/
example_usage.py
test_api.py

# Only include frontend directory
*
!frontend/
!frontend/**
```
