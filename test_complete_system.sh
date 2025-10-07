#!/bin/bash

# Complete Frontend + Backend Test Script
# This script starts both backend and frontend and runs a quick test

echo "=========================================="
echo "  VRP Complete System Test"
echo "=========================================="
echo ""

# Navigate to project root
cd "$(dirname "$0")"
PROJECT_ROOT="/mnt/c/Users/paypa/OneDrive/Desktop/Project/The Vehicle Routing Problem (VRP)"
cd "$PROJECT_ROOT"

echo "📁 Project root: $PROJECT_ROOT"
echo ""

# Step 1: Check Python
echo "🔍 Step 1: Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    echo "✅ Python found: $PYTHON_CMD"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    echo "✅ Python found: $PYTHON_CMD"
else
    echo "❌ Error: Python is not installed"
    exit 1
fi
echo ""

# Step 2: Check virtual environment
echo "🔍 Step 2: Checking virtual environment..."
if [ -d ".venv" ]; then
    echo "✅ Virtual environment exists"
    source .venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "❌ Error: Virtual environment not found"
    echo "Please create it first: python3 -m venv .venv"
    exit 1
fi
echo ""

# Step 3: Start backend
echo "🚀 Step 3: Starting backend API..."
pkill -f uvicorn || true
sleep 1

uvicorn api.main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
BACKEND_PID=$!
echo "✅ Backend started (PID: $BACKEND_PID)"
echo "📝 Logs: backend.log"
echo ""

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Step 4: Test backend
echo "🔍 Step 4: Testing backend health..."
HEALTH_RESPONSE=$(curl -s http://localhost:8000/health)
if echo "$HEALTH_RESPONSE" | grep -q "healthy"; then
    echo "✅ Backend is healthy"
    echo "$HEALTH_RESPONSE" | python3 -m json.tool
else
    echo "❌ Backend health check failed"
    echo "Response: $HEALTH_RESPONSE"
    cat backend.log
    exit 1
fi
echo ""

# Step 5: Test solve endpoint
echo "🔍 Step 5: Testing solve endpoint..."
SOLVE_RESPONSE=$(curl -s -X POST http://localhost:8000/solve \
    -H "Content-Type: application/json" \
    -d '{
        "vehicles": [
            {"id": "VEH001", "current_lat": 37.7749, "current_lon": -122.4194}
        ],
        "orders": [
            {"id": "ORD001", "pickup_lat": 37.7849, "pickup_lon": -122.4094, "dropoff_lat": 37.7949, "dropoff_lon": -122.3994}
        ],
        "algorithm": "greedy"
    }')

if echo "$SOLVE_RESPONSE" | grep -q "success"; then
    echo "✅ Solve endpoint working"
    echo "$SOLVE_RESPONSE" | python3 -m json.tool | head -20
else
    echo "❌ Solve endpoint failed"
    echo "Response: $SOLVE_RESPONSE"
    exit 1
fi
echo ""

# Step 6: Start frontend
echo "🚀 Step 6: Starting frontend server..."
cd frontend

# Kill any existing HTTP servers on port 8080
pkill -f "http.server 8080" || true
sleep 1

$PYTHON_CMD -m http.server 8080 > ../frontend.log 2>&1 &
FRONTEND_PID=$!
echo "✅ Frontend started (PID: $FRONTEND_PID)"
echo "📝 Logs: frontend.log"
echo ""

# Wait for frontend to start
echo "⏳ Waiting for frontend to start..."
sleep 3

# Step 7: Test frontend
echo "🔍 Step 7: Testing frontend access..."
if curl -s http://localhost:8080 > /dev/null 2>&1; then
    echo "✅ Frontend is accessible"
else
    echo "❌ Frontend is not accessible"
    exit 1
fi
echo ""

# Display results
echo "=========================================="
echo "  ✅ All Tests Passed!"
echo "=========================================="
echo ""
echo "🌐 Frontend: http://localhost:8080"
echo "🔌 Backend:  http://localhost:8000"
echo ""
echo "📊 Backend Docs: http://localhost:8000/docs"
echo "🗺️  Open the frontend in your browser to test the visualization!"
echo ""
echo "📝 Logs:"
echo "   Backend: $PROJECT_ROOT/backend.log"
echo "   Frontend: $PROJECT_ROOT/frontend.log"
echo ""
echo "🛑 To stop the servers:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo "   Or press Ctrl+C"
echo ""
echo "=========================================="

# Keep script running to show logs
tail -f backend.log frontend.log
