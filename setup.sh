#!/bin/bash

# TrendSense™ Platform Setup Script
# This script helps set up the TrendSense™ Platform environment

echo "🚀 Setting up TrendSense™ Platform..."
echo "======================================"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
  echo "Creating .env file..."
  cat > .env << EOF
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/trendsense
MONGODB_URI=mongodb://localhost:27017/trendsense

# API Keys
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_google_api_key

# Application Settings
PORT=3000
NODE_ENV=development
EOF
  echo "✅ Created .env file. Please update it with your actual credentials."
else
  echo "ℹ️ .env file already exists."
fi

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

# Check if Python is installed
if command -v python3 &>/dev/null; then
  echo "📦 Installing Python dependencies..."
  pip install -r backend/requirements-sustainability.txt
else
  echo "⚠️ Python 3 not found. Please install Python 3.11+ to use Python backend features."
fi

# Check if PostgreSQL is available
echo "🔍 Checking PostgreSQL connection..."
if ! command -v pg_isready &>/dev/null; then
  echo "⚠️ PostgreSQL CLI tools not found. Please make sure PostgreSQL is installed."
else
  source .env
  PG_CONNECTION_STRING=${DATABASE_URL:-"postgresql://username:password@localhost:5432/trendsense"}
  
  if pg_isready -d "$PG_CONNECTION_STRING" &>/dev/null; then
    echo "✅ PostgreSQL connection successful."
    echo "🗃️ Setting up database..."
    npm run db:push
  else
    echo "⚠️ Could not connect to PostgreSQL. Please update your DATABASE_URL in .env file."
  fi
fi

# Check MongoDB if URI is provided
if [ -n "$MONGODB_URI" ] && [ "$MONGODB_URI" != "mongodb://localhost:27017/trendsense" ]; then
  echo "🔍 Checking MongoDB connection..."
  if ! command -v mongosh &>/dev/null; then
    echo "⚠️ MongoDB tools not found. Please make sure MongoDB is installed."
  else
    if mongosh "$MONGODB_URI" --eval "print('MongoDB connection successful')" &>/dev/null; then
      echo "✅ MongoDB connection successful."
      echo "🗃️ Initializing MongoDB..."
      node server/initialize_mongodb.ts
    else
      echo "⚠️ Could not connect to MongoDB. Please update your MONGODB_URI in .env file."
    fi
  fi
fi

echo ""
echo "🎉 Setup completed!"
echo "To start the application, run: npm run dev"
echo "The application will be available at: http://localhost:3000"
echo ""
echo "For more information, please refer to the SETUP_INSTRUCTIONS.md file."