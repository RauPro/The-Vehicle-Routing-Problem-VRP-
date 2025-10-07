#!/bin/bash

# Frontend Quick Start Script
# This script starts a simple HTTP server for the VRP frontend

echo "=========================================="
echo "  VRP Frontend Visualization"
echo "=========================================="
echo ""

# Check if Python is available
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Error: Python is not installed"
    echo "Please install Python to run the HTTP server"
    exit 1
fi

echo "✅ Python found: $PYTHON_CMD"
echo ""

# Check if backend is running
echo "🔍 Checking backend API..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend API is running on port 8000"
else
    echo "⚠️  Warning: Backend API is not running on port 8000"
    echo ""
    echo "To start the backend, run in another terminal:"
    echo "  cd .."
    echo "  uvicorn api.main:app --reload"
    echo ""
    read -p "Press Enter to continue anyway..."
fi

echo ""
echo "🚀 Starting frontend server..."
echo ""
echo "📍 Frontend will be available at:"
echo "   http://localhost:8080"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=========================================="
echo ""

# Start HTTP server
cd "$(dirname "$0")"
$PYTHON_CMD -m http.server 8080
