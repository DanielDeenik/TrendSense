# TrendSense™ Platform Export Summary

## Archive Details

- **Latest Archive**: `TrendSense_complete_20250403.tar.gz` (295KB)
- **Created On**: April 3, 2025
- **Contents**: Complete source code including frontend, backend, and setup files

## Components Included

### Core Code
- **Frontend**: React/SvelteKit client application with components and pages
- **Backend**: Node.js and Python dual backend architecture
- **Database**: PostgreSQL schema definitions and MongoDB integration options
- **AI Services**: Pattern recognition engine and document analysis capabilities

### Documentation
- `README.md` - Project overview and introduction
- `ARCHITECTURE.md` - Technical architecture details
- `VC_PE_ENGINE.md` - Pattern engine specifications
- `AI-DRIVEN-ARCHITECTURE.md` - AI integration documentation
- `SETUP_INSTRUCTIONS.md` - Deployment and installation guide

### Setup Scripts
- `setup-project.sh` - Environment setup automation
- `check_database.sh` - Database connection verification

## Deployment Instructions

1. Extract the archive: `tar -xzvf TrendSense_complete_20250403.tar.gz`
2. Run the setup script: `./setup-project.sh`
3. Configure the database connection in `.env`
4. Install dependencies: `npm install`
5. Initialize the database: `npm run db:push`
6. Start the application: `npm run dev`

## Key Features

- Multi-tenant sustainability data analytics
- Cross-portfolio pattern detection with privacy preservation
- AI-powered document analysis and storytelling
- Interactive dashboards for ESG metrics visualization
- Federated insights with temporal correlation

## Technical Stack

- **Frontend**: React, TypeScript, Tailwind CSS
- **Backend**: Node.js, Express, FastAPI, Flask
- **Database**: PostgreSQL with Drizzle ORM, MongoDB (optional)
- **AI Integration**: Google Gemini, OpenAI
- **Vector Database**: Pinecone (optional)

For detailed instructions, refer to the `SETUP_INSTRUCTIONS.md` file included in the archive.