#!/bin/bash

# Function to kill background processes on exit
cleanup() {
    echo "Stopping servers..."
    kill $BACKEND_PID
    kill $FRONTEND_PID
    exit
}

trap cleanup SIGINT

# Start Backend
echo "🚀 Starting Backend..."
cd codespace/backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000 > ../../server.log 2>&1 &
BACKEND_PID=$!

# Start Frontend
echo "✨ Starting Frontend..."
cd ../frontend
npm run dev -- --port 5173 &
FRONTEND_PID=$!

echo "✅ FlirtNet is running!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo "Press Ctrl+C to stop"

wait
