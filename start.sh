#!/bin/bash
set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting Investment App Infrastructure...${NC}"

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed and is required."
    exit 1
fi

# 1. Start Docker Containers
echo -e "\n${BLUE}🐳 Starting Backend, Database, Redis, and Celery Worker...${NC}"
docker-compose up -d --build

# Wait for backend to be somewhat ready (optional, but good for UX)
echo -e "${BLUE}⏳ Waiting a moment for services to initialize...${NC}"
sleep 5

# 2. Frontend Setup
echo -e "\n${BLUE}💻 Setting up Frontend...${NC}"
cd frontend

if [ ! -d "node_modules" ]; then
    echo -e "${BLUE}📦 Installing frontend dependencies...${NC}"
    npm install
else
    echo -e "${GREEN}✓ Node modules already installed.${NC}"
fi

echo -e "\n${GREEN}✅ Infrastructure is UP!${NC}"
echo -e "   - Backend API: http://localhost:8000"
echo -e "   - Swagger Doc: http://localhost:8000/docs"
echo -e "   - Frontend URL: http://localhost:3000"

# 3. Start Frontend
echo -e "\n${BLUE}🚀 Starting Frontend Development Server...${NC}"
npm run dev
