# TrendSense™ Platform Setup Instructions

This document provides step-by-step instructions for setting up the TrendSense™ Platform (also branded as SustainaTrend™ in the UI). The platform is an AI-first sustainability analytics platform specialized for venture capital and private equity firms.

## System Requirements

- Node.js v18+ 
- Python 3.11+
- PostgreSQL 14+
- MongoDB 6.0+ (optional for document storage)
- OpenAI API key (for AI-powered features)
- Google API key (for searching)

## Quick Start

1. **Extract the archived project**:
   ```bash
   tar -xzvf TrendSense_export_20250403_185505.tar.gz -C /your/destination/folder
   cd /your/destination/folder
   ```

2. **Install dependencies**:
   ```bash
   # Install Node.js dependencies
   npm install
   
   # Install Python dependencies (if using Python backend)
   pip install -r backend/requirements-sustainability.txt
   ```

3. **Configure environment variables**:
   Create a `.env` file in the root directory with the following variables:
   ```
   # Database Configuration
   DATABASE_URL=postgresql://username:password@localhost:5432/trendsense
   MONGODB_URI=mongodb://localhost:27017/trendsense
   
   # API Keys
   OPENAI_API_KEY=your_openai_api_key
   GOOGLE_API_KEY=your_google_api_key
   
   # Application Settings
   PORT=3000
   NODE_ENV=development
   ```

4. **Setup the database**:
   ```bash
   # Initialize the PostgreSQL database
   npm run db:push
   
   # Initialize MongoDB (if using document storage)
   node server/initialize_mongodb.ts
   ```

5. **Run the application**:
   ```bash
   # Start the full stack application
   npm run dev
   ```

The application should now be running at http://localhost:3000.

## Architecture Overview

TrendSense™ consists of multiple components:

1. **Frontend (SvelteKit/React with Tailwind CSS)**
   - Dashboard for visualizing sustainability metrics
   - Company and fund management interfaces
   - Document analysis and pattern detection UI

2. **Node.js Backend**
   - API routes for data access
   - Integration with storage layer
   - Pattern recognition engine

3. **PostgreSQL Database**
   - Structured data storage for funds, companies, metrics
   - Temporal analysis and cross-portfolio analytics

4. **MongoDB (Optional)**
   - Document storage for unstructured data
   - Vector embeddings for semantic search

5. **Python Services (Optional)**
   - AI-powered sustainability analysis
   - Document processing and storytelling

## Additional Documentation

For more information, please refer to these documents included in the archive:

- `README.md` - General project overview
- `ARCHITECTURE.md` - Detailed architecture of the application
- `VC_PE_ENGINE.md` - Description of the pattern engine
- `AI-DRIVEN-ARCHITECTURE.md` - Overview of AI capabilities

## Troubleshooting

**Database Connection Issues**
- Verify your PostgreSQL connection string in the `.env` file
- Run `npm run db:check` to verify database connectivity

**API Key Issues**
- Ensure your OpenAI and Google API keys are correctly set in the `.env` file
- Check usage limits on your API accounts

**Server Won't Start**
- Check for port conflicts and adjust the `PORT` variable in `.env`
- Verify all dependencies are installed with `npm install`

## Contact

For additional support or questions, please contact support@trendsense.ai