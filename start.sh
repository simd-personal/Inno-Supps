#!/bin/bash

# Inno Supps - Clean Build Startup Script
echo "🚀 Starting Inno Supps - AI-Powered B2B Growth System"
echo "=================================================="

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Set environment variables
export OPENAI_API_KEY="${OPENAI_API_KEY:-your-openai-api-key-here}"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down services..."
    pkill -f "python main.py" 2>/dev/null
    pkill -f "npm run dev" 2>/dev/null
    pkill -f "uvicorn" 2>/dev/null
    echo "✅ Cleanup complete"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Start Backend
echo "🔧 Starting Backend (Port 8000)..."
cd backend
python main.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "⏳ Waiting for backend to initialize..."
sleep 5

# Check if backend is running
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend is running at http://localhost:8000"
else
    echo "❌ Backend failed to start"
    cleanup
fi

# Start Frontend
echo "🎨 Starting Frontend (Port 3000)..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
echo "⏳ Waiting for frontend to initialize..."
sleep 8

# Check if frontend is running
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Frontend is running at http://localhost:3000"
else
    echo "⚠️  Frontend may still be starting up..."
fi

echo ""
echo "🎉 Inno Supps is now running!"
echo "=================================================="
echo "📊 Backend API:  http://localhost:8000"
echo "🎨 Frontend UI:  http://localhost:3000"
echo "📚 API Docs:     http://localhost:8000/docs"
echo "🔍 Health Check: http://localhost:8000/health"
echo ""
echo "🧠 NEW: AI Input Cleaning Active!"
echo "   - Automatically fixes spelling & grammar"
echo "   - Improves professional formatting"
echo "   - Enhances value propositions"
echo "   - Standardizes business terminology"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Keep script running
wait