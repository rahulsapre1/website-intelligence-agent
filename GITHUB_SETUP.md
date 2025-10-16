# GitHub Repository Setup Guide

This guide will help you create and configure a GitHub repository for the Website Intelligence Agent project.

## 🚀 Step 1: Create GitHub Repository

### Option A: Using GitHub Web Interface (Recommended)

1. **Go to GitHub**
   - Visit [github.com](https://github.com) and sign in
   - Click the "+" icon in the top right corner
   - Select "New repository"

2. **Repository Settings**
   - **Repository name**: `website-intelligence-agent`
   - **Description**: `AI-powered agent for extracting business insights from website homepages using FastAPI, Next.js, and Google Gemini`
   - **Visibility**: Public (recommended for showcasing)
   - **Initialize**: ❌ Do NOT check "Add a README file" (we already have one)
   - **Initialize**: ❌ Do NOT check "Add .gitignore" (we already have one)
   - **Initialize**: ❌ Do NOT check "Choose a license" (optional)

3. **Create Repository**
   - Click "Create repository"
   - GitHub will show you the commands to push existing code

### Option B: Using GitHub CLI

```bash
# Install GitHub CLI if not already installed
# macOS: brew install gh
# Windows: winget install GitHub.cli
# Linux: curl -fsSL https://cli.github.com/packages/github/githubcli-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg

# Authenticate with GitHub
gh auth login

# Create repository
gh repo create website-intelligence-agent --public --description "AI-powered agent for extracting business insights from website homepages using FastAPI, Next.js, and Google Gemini"

# Add remote and push
git remote add origin https://github.com/YOUR_USERNAME/website-intelligence-agent.git
git branch -M main
git push -u origin main
```

## 🔧 Step 2: Connect Local Repository to GitHub

After creating the repository on GitHub, run these commands:

```bash
# Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/website-intelligence-agent.git

# Set main branch
git branch -M main

# Push to GitHub
git push -u origin main
```

## 📋 Step 3: Repository Configuration

### 3.1 Repository Settings
1. Go to your repository on GitHub
2. Click "Settings" tab
3. Configure the following:

**General:**
- **Repository name**: `website-intelligence-agent`
- **Description**: Update with comprehensive description
- **Website**: Add your deployed frontend URL
- **Topics**: Add tags like `ai`, `fastapi`, `nextjs`, `website-analysis`, `gemini`, `supabase`

**Features:**
- ✅ Issues
- ✅ Projects
- ✅ Wiki (optional)
- ✅ Discussions (optional)

### 3.2 Branch Protection
1. Go to Settings → Branches
2. Click "Add rule"
3. Configure:
   - **Branch name pattern**: `main`
   - ✅ Require a pull request before merging
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
   - ✅ Require linear history

### 3.3 GitHub Actions Permissions
1. Go to Settings → Actions → General
2. Set "Workflow permissions" to "Read and write permissions"
3. Allow GitHub Actions to create and approve pull requests

## 🔐 Step 4: Environment Variables and Secrets

### 4.1 GitHub Secrets (for CI/CD)
Go to Settings → Secrets and variables → Actions, add:

```
API_SECRET_KEY=your_secret_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
GEMINI_API_KEY=your_gemini_key
JINA_API_KEY=your_jina_key
```

### 4.2 Environment Variables (for deployment)
These will be set in Render and Vercel during deployment:
- **Render**: Set in dashboard under Environment tab
- **Vercel**: Set in dashboard under Settings → Environment Variables

## 📊 Step 5: Repository Features Setup

### 5.1 Issues and Projects
1. **Create Issues** for:
   - Feature requests
   - Bug reports
   - Documentation improvements
   - Deployment issues

2. **Create Project Board** for:
   - Development roadmap
   - Bug tracking
   - Feature planning

### 5.2 GitHub Pages (Optional)
If you want to host documentation:
1. Go to Settings → Pages
2. Source: Deploy from a branch
3. Branch: `main` / `docs` folder
4. Save

### 5.3 Releases
1. Go to Releases
2. Create a new release
3. Tag: `v1.0.0`
4. Title: `Website Intelligence Agent v1.0.0`
5. Description: Include features, improvements, and deployment info

## 🏷️ Step 6: Repository Tags and Topics

### Topics to Add:
```
ai
artificial-intelligence
fastapi
nextjs
typescript
python
website-analysis
web-scraping
gemini
google-ai
supabase
postgresql
jina-ai
business-intelligence
machine-learning
llm
large-language-model
react
tailwindcss
shadcn
vercel
render
deployment
fullstack
api
rest-api
```

## 📝 Step 7: Documentation Updates

### 7.1 Update README.md
After deployment, update these sections:
- **Live Demo URLs**
- **API Documentation Links**
- **Deployment Status**
- **Contributing Guidelines**

### 7.2 Add Contributing Guidelines
Create `CONTRIBUTING.md`:
```markdown
# Contributing to Website Intelligence Agent

## Development Setup
[Include local setup instructions]

## Pull Request Process
[Include PR guidelines]

## Code Standards
[Include coding standards]
```

### 7.3 Add License
Create `LICENSE` file (MIT recommended):
```markdown
MIT License
[Standard MIT license text]
```

## 🔄 Step 8: Continuous Integration

The repository includes GitHub Actions workflow that will:
- ✅ Run tests on every push
- ✅ Check code quality
- ✅ Build frontend
- ✅ Validate API endpoints

## 🚀 Step 9: Deployment Integration

### 9.1 Render Integration
1. Connect GitHub repository to Render
2. Enable auto-deploy on push to main
3. Set environment variables

### 9.2 Vercel Integration
1. Connect GitHub repository to Vercel
2. Configure build settings
3. Set environment variables

## 📈 Step 10: Repository Analytics

### 10.1 Enable Insights
- Go to Insights tab
- Enable repository insights
- Monitor traffic, clones, and forks

### 10.2 Add Badges
Update README.md with status badges:
```markdown
![CI](https://github.com/YOUR_USERNAME/website-intelligence-agent/workflows/CI/badge.svg)
![Deployment](https://img.shields.io/badge/deployment-render%20%7C%20vercel-blue)
![License](https://img.shields.io/badge/license-MIT-green)
```

## ✅ Final Checklist

- [ ] Repository created on GitHub
- [ ] Local repository connected and pushed
- [ ] Repository settings configured
- [ ] Branch protection rules set
- [ ] GitHub Actions secrets added
- [ ] Topics and tags added
- [ ] README.md updated with live URLs
- [ ] Contributing guidelines added
- [ ] License file added
- [ ] CI/CD pipeline working
- [ ] Deployment configured
- [ ] Documentation complete

## 🆘 Troubleshooting

### Common Issues

**Push Rejected:**
```bash
# If you get "rejected" error
git pull origin main --allow-unrelated-histories
git push origin main
```

**Remote Already Exists:**
```bash
# Remove existing remote
git remote remove origin
# Add correct remote
git remote add origin https://github.com/YOUR_USERNAME/website-intelligence-agent.git
```

**Authentication Issues:**
- Use Personal Access Token instead of password
- Enable 2FA and use token for authentication

## 📞 Support

- GitHub Documentation: https://docs.github.com
- Git Documentation: https://git-scm.com/doc
- GitHub CLI: https://cli.github.com
