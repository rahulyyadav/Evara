#!/bin/bash

# TaskFlow Agent Local Testing Script
# This script helps you test your agent locally without needing WhatsApp

echo "🧪 TaskFlow Agent Local Testing"
echo "================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if server is running
echo -e "${BLUE}1. Checking if server is running...${NC}"
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Server is running!${NC}"
else
    echo -e "${YELLOW}⚠️  Server is not running. Please start it first:${NC}"
    echo "   cd taskflow && source venv/bin/activate && python3 -m app.main"
    exit 1
fi

echo ""
echo -e "${BLUE}2. Testing Health Endpoint:${NC}"
curl -s http://localhost:8000/health | python3 -m json.tool
echo ""

echo -e "${BLUE}3. Testing Root Endpoint:${NC}"
curl -s http://localhost:8000/ | python3 -m json.tool
echo ""

echo -e "${BLUE}4. Testing Webhook (Simulating WhatsApp Message):${NC}"
echo -e "${YELLOW}   Sending test message: 'Hello TaskFlow!'${NC}"
RESPONSE=$(curl -s -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "From=whatsapp:+1234567890" \
  -d "Body=Hello TaskFlow!" \
  -d "MessageSid=test123" \
  -d "NumMedia=0")

if [ -z "$RESPONSE" ]; then
    echo -e "${GREEN}✅ Webhook responded successfully (empty response is expected)${NC}"
else
    echo "Response: $RESPONSE"
fi

echo ""
echo -e "${BLUE}5. Testing with different messages:${NC}"

# Test message 1
echo -e "${YELLOW}   Test 1: Short message${NC}"
curl -s -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "From=whatsapp:+1234567890" \
  -d "Body=Hi" \
  -d "MessageSid=test001" \
  -d "NumMedia=0" > /dev/null
echo "   ✅ Sent"

# Test message 2
echo -e "${YELLOW}   Test 2: Long message${NC}"
curl -s -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "From=whatsapp:+1234567890" \
  -d "Body=This is a longer test message to see how the agent handles multiple words and sentences." \
  -d "MessageSid=test002" \
  -d "NumMedia=0" > /dev/null
echo "   ✅ Sent"

# Test message 3
echo -e "${YELLOW}   Test 3: Message with emoji${NC}"
curl -s -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "From=whatsapp:+1234567890" \
  -d "Body=Hello! 🚀 How are you?" \
  -d "MessageSid=test003" \
  -d "NumMedia=0" > /dev/null
echo "   ✅ Sent"

echo ""
echo -e "${BLUE}6. Recent logs (last 20 lines):${NC}"
if [ -f "logs/taskflow.log" ]; then
    tail -n 20 logs/taskflow.log
else
    echo "   No log file found"
fi

echo ""
echo -e "${GREEN}✅ Testing complete!${NC}"
echo ""
echo "📝 Next steps:"
echo "   - Check logs: tail -f logs/taskflow.log"
echo "   - View API docs: http://localhost:8000/docs"
echo "   - Test more messages by editing this script"
echo ""

