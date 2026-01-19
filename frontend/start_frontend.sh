#!/bin/bash
# Start React Frontend

echo "🌐 Starting Face Attendance System - FRONTEND"
echo "================================================"

# Check if dependencies installed
if [ ! -d "node_modules" ]; then
    echo "📥 Installing frontend dependencies..."
    npm install
    echo "✅ Frontend dependencies ready"
fi

# Start Vite dev server
echo ""
echo "🔧 Starting React Dev Server"
echo "Open your browser: http://localhost:5173 or http://localhost:5174"
echo "================================================"
npm run dev -- --host
