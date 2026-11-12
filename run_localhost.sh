#!/bin/bash
# Startup script for localhost development

echo "🚀 Setting up Hey-Big-Proppa localhost environment..."

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Please run this script from the Hey-Big-Proppa root directory"
    exit 1
fi

# Set up Python environment
echo "📦 Setting up Python environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

source .venv/bin/activate
pip install -r requirements.txt

# Set up Node.js environment
echo "📦 Setting up Node.js environment..."
export PATH="$HOME/Downloads/node-v26.13.1-linux-x64/bin:$PATH"
cd frontend
if [ ! -d "node_modules" ]; then
    npm ci
fi
cd ..

# Build the frontend first (this will be served by the backend)
echo "🏗️ Building frontend..."
export PATH="$HOME/Downloads/node-v26.13.1-linux-x64/bin:$PATH"
cd frontend
npm run build
cd ..

# Create the .env file with default values if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOF
# ESPN API
ESPN_API_KEY=place_holder_key
ESPN_SEASON=2026
DEBUG=True
EOF
fi

# Start the backend server
echo "🌟 Starting backend server (serving frontend build)..."
source .venv/bin/activate
export PATH="$HOME/Downloads/node-v26.13.1-linux-x64/bin:$PATH"
python backend/main.py