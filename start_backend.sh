#!/bin/bash
# Start Flask Backend Server

echo "🚀 Starting Face Attendance System - BACKEND"
echo "================================================"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install --quiet --upgrade pip setuptools wheel 2>/dev/null
pip install -r requirements.txt 2>/dev/null
echo "✅ Python dependencies ready"

# Start Flask
echo ""
echo "🔧 Starting Flask Backend on http://localhost:5000"
echo "================================================"
FRONTEND_ORIGIN=http://localhost:5173 python3 app.py
