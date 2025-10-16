#!/bin/bash

# Website Intelligence Agent - Startup Script

echo "🚀 Starting Website Intelligence Agent..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "📋 Please copy .env.example to .env and fill in your API keys:"
    echo "   cp .env.example .env"
    echo ""
    echo "Required environment variables:"
    echo "   - GEMINI_API_KEY: Get from https://makersuite.google.com/app/apikey"
    echo "   - SUPABASE_URL: Your Supabase project URL"
    echo "   - SUPABASE_KEY: Your Supabase anon/public key"
    echo "   - API_SECRET_KEY: A secure secret key for API authentication"
    echo ""
    echo "Also make sure to run the SQL setup script in your Supabase dashboard!"
    exit 1
fi

# Function to find an available port
find_available_port() {
    local port=8000
    while lsof -i :$port > /dev/null 2>&1; do
        echo "⚠️  Port $port is already in use, trying port $((port + 1))..."
        port=$((port + 1))
    done
    echo $port
}

echo "✅ Environment setup complete!"

# Check if port 8000 is available, find alternative if not
PORT=$(find_available_port)
if [ "$PORT" != "8000" ]; then
    echo "⚠️  Port 8000 was in use, using port $PORT instead"
fi

# Export the port as an environment variable
export PORT=$PORT

echo "🌐 Starting FastAPI server on port $PORT..."
echo "📖 API documentation will be available at: http://localhost:$PORT/docs"
echo ""

# Start the application
uvicorn app.main:app --reload --host 0.0.0.0 --port $PORT
