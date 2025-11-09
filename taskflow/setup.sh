#!/bin/bash

# TaskFlow Setup Script
# Quick setup for development environment

echo "🚀 Setting up TaskFlow..."
echo ""

# Check Python version
echo "📍 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then 
    echo "❌ Error: Python 3.11+ required. Found: $python_version"
    exit 1
fi
echo "✅ Python version: $python_version"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists"
else
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data logs
touch data/.gitkeep
echo "✅ Directories created"
echo ""

# Setup environment file
echo "⚙️  Setting up environment file..."
if [ -f ".env" ]; then
    echo "⚠️  .env file already exists - skipping"
else
    cp .env.example .env
    echo "✅ .env file created - please edit with your credentials"
fi
echo ""

# Summary
echo "============================================"
echo "✅ TaskFlow setup complete!"
echo "============================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Twilio credentials"
echo "2. Activate the virtual environment: source venv/bin/activate"
echo "3. Run the application: python -m app.main"
echo ""
echo "For more information, see README.md"
echo ""

