#!/bin/bash

# Next.js Runtime Performance Comparison - Startup Script
# This script builds and starts all containers for the performance comparison

set -e

echo "🚀 Starting Next.js Runtime Performance Comparison"
echo "=================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose > /dev/null 2>&1; then
    echo "❌ Docker Compose not found. Please install Docker Compose."
    exit 1
fi

echo "✅ Docker environment verified"

# Build and start all containers
echo "🏗️  Building and starting containers..."
docker-compose up -d --build

# Wait a moment for containers to start
echo "⏳ Waiting for containers to initialize..."
sleep 10

# Check container status
echo "📊 Container Status:"
docker-compose ps

# Check if all containers are running
RUNNING_CONTAINERS=$(docker-compose ps -q | wc -l)
TOTAL_CONTAINERS=4  # node-nextjs, deno-nextjs, bun-nextjs, monitoring

if [ "$RUNNING_CONTAINERS" -eq "$TOTAL_CONTAINERS" ]; then
    echo "✅ All containers are running successfully!"
    echo ""
    echo "🌐 Access URLs:"
    echo "   Node.js App:  http://localhost:3001"
    echo "   Deno App:     http://localhost:3002"
    echo "   Bun App:      http://localhost:3003"
    echo "   Jupyter Lab:  http://localhost:8888"
    echo ""
    echo "📊 To start performance analysis:"
    echo "   1. Open http://localhost:8888 in your browser"
    echo "   2. Navigate to notebooks/runtime_performance_comparison.ipynb"
    echo "   3. Run all cells to perform the analysis"
    echo ""
    echo "🛑 To stop all containers:"
    echo "   docker-compose down"
else
    echo "⚠️  Some containers may not be running properly."
    echo "Check the logs with: docker-compose logs"
fi