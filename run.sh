#!/bin/bash
# Face Attendance System - One-command runner
set -e

echo "🚀 Starting Face Attendance System..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
source .venv/bin/activate

# Install/upgrade dependencies
echo "📥 Installing Python dependencies..."
pip install --quiet --upgrade pip setuptools wheel
pip install -r requirements.txt
echo "✅ Python dependencies ready"

# Check if frontend dependencies are installed
if [ ! -d "frontend/node_modules" ]; then
    echo "📥 Installing frontend dependencies..."
    cd frontend && npm install && cd ..
    echo "✅ Frontend dependencies ready"
fi

# Start backend in background
echo "🔧 Starting Flask backend..."
FRONTEND_ORIGIN=http://localhost:5173 python3 app.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 2

# Start frontend
echo "🌐 Starting React frontend..."
cd frontend
npm run dev -- --host

# Cleanup: kill backend when frontend stops
kill $BACKEND_PID 2>/dev/null
