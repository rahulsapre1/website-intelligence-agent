#!/bin/bash

# Website Intelligence Agent - Deployment Script
# This script helps deploy the application to Render (backend) and Vercel (frontend)

set -e

echo "🚀 Website Intelligence Agent - Deployment Helper"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required tools are installed
check_dependencies() {
    print_status "Checking dependencies..."
    
    # Check for git
    if ! command -v git &> /dev/null; then
        print_error "Git is not installed. Please install Git first."
        exit 1
    fi
    
    # Check for Node.js (for frontend)
    if ! command -v node &> /dev/null; then
        print_warning "Node.js is not installed. Frontend deployment may require manual setup."
    fi
    
    # Check for Python (for backend)
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3 first."
        exit 1
    fi
    
    print_success "Dependencies check completed"
}

# Test the application locally
test_local() {
    print_status "Testing application locally..."
    
    # Test backend
    print_status "Testing backend..."
    cd "$(dirname "$0")/.."
    
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        print_success "Backend dependencies installed"
    else
        print_error "requirements.txt not found"
        exit 1
    fi
    
    # Test frontend build
    print_status "Testing frontend build..."
    if [ -d "frontend" ]; then
        cd frontend
        if [ -f "package.json" ]; then
            npm install
            npm run build
            print_success "Frontend build successful"
        else
            print_error "Frontend package.json not found"
            exit 1
        fi
        cd ..
    else
        print_error "Frontend directory not found"
        exit 1
    fi
    
    print_success "Local tests completed successfully"
}

# Deploy backend to Render
deploy_backend() {
    print_status "Preparing backend deployment to Render..."
    
    # Check if render.yaml exists
    if [ ! -f "render.yaml" ]; then
        print_error "render.yaml not found. Please ensure it exists in the root directory."
        exit 1
    fi
    
    # Check if Dockerfile exists
    if [ ! -f "Dockerfile" ]; then
        print_error "Dockerfile not found. Please ensure it exists in the root directory."
        exit 1
    fi
    
    print_success "Backend deployment files ready"
    print_warning "Manual steps required for Render deployment:"
    echo "1. Go to https://render.com"
    echo "2. Connect your GitHub repository"
    echo "3. Create a new Web Service"
    echo "4. Set the following environment variables:"
    echo "   - API_SECRET_KEY"
    echo "   - SUPABASE_URL"
    echo "   - SUPABASE_KEY"
    echo "   - GEMINI_API_KEY"
    echo "   - JINA_API_KEY"
    echo "5. Deploy the service"
}

# Deploy frontend to Vercel
deploy_frontend() {
    print_status "Preparing frontend deployment to Vercel..."
    
    # Check if frontend directory exists
    if [ ! -d "frontend" ]; then
        print_error "Frontend directory not found"
        exit 1
    fi
    
    # Check if vercel.json exists
    if [ ! -f "frontend/vercel.json" ]; then
        print_warning "vercel.json not found in frontend directory"
    fi
    
    print_success "Frontend deployment files ready"
    print_warning "Manual steps required for Vercel deployment:"
    echo "1. Go to https://vercel.com"
    echo "2. Import your GitHub repository"
    echo "3. Set the Root Directory to 'frontend'"
    echo "4. Add environment variable:"
    echo "   - NEXT_PUBLIC_API_URL (set to your Render backend URL)"
    echo "5. Deploy"
}

# Main deployment function
main() {
    echo ""
    print_status "Starting deployment process..."
    echo ""
    
    # Check dependencies
    check_dependencies
    echo ""
    
    # Test locally first
    test_local
    echo ""
    
    # Prepare backend deployment
    deploy_backend
    echo ""
    
    # Prepare frontend deployment
    deploy_frontend
    echo ""
    
    print_success "Deployment preparation completed!"
    echo ""
    print_status "Next steps:"
    echo "1. Follow the manual deployment steps above"
    echo "2. Update frontend environment variables with backend URL"
    echo "3. Test the deployed application"
    echo "4. Update README.md with production URLs"
    echo ""
    print_warning "Remember to keep your API keys secure and never commit them to version control!"
}

# Run main function
main "$@"
