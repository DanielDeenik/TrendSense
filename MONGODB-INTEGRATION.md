# MongoDB Integration for TrendSense VC Platform

This document outlines the MongoDB integration for the TrendSense VC Platform, which provides a hybrid database approach: PostgreSQL for structured data and MongoDB for unstructured data.

## Architecture

The MongoDB integration follows a layered architecture:

1. **Connection Layer**: `mongodb_connection.ts` handles MongoDB connection, collection setup, and utility functions.
2. **Service Layer**: Service modules in `server/services/` provide CRUD operations for different entity types.
3. **API Layer**: `mongo_routes.ts` exposes REST API endpoints for MongoDB operations.

## Components

### MongoDB Connection Module (`mongodb_connection.ts`)

This module provides:
- Connection management to MongoDB
- Collection management and indexing
- Utility functions for working with MongoDB (ObjectId conversion, document serialization)

### MongoDB Services

1. **Document Service** (`document_service.ts`)
   - Handles sustainability document storage and retrieval
   - Provides search capabilities for documents
   - Manages document metadata and analysis results

2. **Pattern Service** (`pattern_service.ts`)
   - Manages investment patterns detected across portfolio companies
   - Provides federated pattern analysis (anonymized cross-portfolio insights)
   - Handles pattern metadata, confidence scoring, and AI explanations

3. **Story Service** (`story_service.ts`)
   - Manages sustainability storytelling content
   - Provides metrics tracking for stories (views, likes, shares)
   - Supports rich content models for McKinsey framework-based stories

4. **Thesis Service** (`thesis_service.ts`)
   - Handles investment thesis documents for VC/PE funds
   - Provides search and sector-based filtering
   - Supports both structured and unstructured thesis content models

### MongoDB API Routes (`mongo_routes.ts`)

REST API endpoints for MongoDB operations:

#### Document Endpoints
- `GET /api/mongo/documents` - List all documents (with optional filtering)
- `GET /api/mongo/documents/:id` - Get document by ID
- `POST /api/mongo/documents` - Create a new document
- `PUT /api/mongo/documents/:id` - Update an existing document
- `DELETE /api/mongo/documents/:id` - Delete a document
- `GET /api/mongo/documents/search` - Search documents by text

#### Pattern Endpoints
- `GET /api/mongo/patterns` - List patterns (with optional filtering)
- `GET /api/mongo/patterns/:id` - Get pattern by ID
- `POST /api/mongo/patterns` - Create a new pattern
- `PUT /api/mongo/patterns/:id` - Update an existing pattern
- `GET /api/mongo/patterns/:id/similar` - Find similar patterns

#### Story Endpoints
- `GET /api/mongo/stories` - List all stories (with optional filtering)
- `GET /api/mongo/stories/top` - Get top stories by views
- `GET /api/mongo/stories/:id` - Get story by ID
- `POST /api/mongo/stories` - Create a new story
- `PUT /api/mongo/stories/:id` - Update an existing story
- `POST /api/mongo/stories/:id/metrics` - Update story metrics

#### Thesis Endpoints
- `GET /api/mongo/theses` - List theses (with optional filtering)
- `GET /api/mongo/theses/:id` - Get thesis by ID
- `POST /api/mongo/theses` - Create a new thesis
- `PUT /api/mongo/theses/:id` - Update an existing thesis
- `GET /api/mongo/theses/search` - Search theses by text

## Configuration

MongoDB connection settings are configured via environment variables:

- `MONGODB_URI` - MongoDB connection string (defaults to localhost)
- `MONGODB_DB_NAME` - Database name (defaults to "trendsense_vc")

## Python Integration

The MongoDB integration also includes Python client utilities:

1. **MongoDB Client** (`frontend/mongo_client.py`)
   - Provides connection functions for both sync and async MongoDB access
   - Includes collection access helpers and serialization utilities

2. **Benchmark Database** (`frontend/benchmark_db.py`)
   - Handles benchmarking data operations for sustainability metrics
   - Provides peer company comparison functions
   - Supports sector and region-based benchmarking

## Initialization

The MongoDB database and collections are initialized:

1. **Server Initialization** (`server/initialize_mongodb.ts`)
   - Creates collections if they don't exist
   - Sets up text indexes for search functionality
   - Validates MongoDB connection

2. **Python Initialization** (`initialize_mongodb.py`)
   - Provides command-line utility for Python-based MongoDB setup
   - Includes test data creation for development

## Integration with Express Server

The MongoDB integration is integrated with the Express server in `server/index.ts`:

- MongoDB connection is established alongside PostgreSQL
- MongoDB routes are mounted at `/api/mongo`
- The server gracefully handles MongoDB connection failures

## Deployment Considerations

When deploying the application:

1. Ensure MongoDB connection string is properly set in environment variables
2. Run initialization script to verify connection and set up collections
3. MongoDB connection is optional - the application will still function with PostgreSQL only