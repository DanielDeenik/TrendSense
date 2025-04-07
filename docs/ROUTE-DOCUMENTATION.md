# SustainaTrend™ Route Documentation

This document outlines the standardized route structure for the SustainaTrend™ Intelligence Platform. The platform follows a consistent, intuitive route naming pattern for improved navigation and user experience.

## Core Pages

| Route | Description | Purpose |
|-------|-------------|---------|
| `/` | Home / AI Trends Feed | Entry point with AI-curated sustainability trends |
| `/risk-tracker` | Risk Tracker | Real-time sustainability risk monitoring dashboard |
| `/story-cards` | Story Cards | AI-generated sustainability narratives and insights |

## Tools

| Route | Description | Purpose |
|-------|-------------|---------|
| `/pdf-analyzer` | PDF Analyzer | Intelligent document processing for sustainability reports |
| `/data-terminal` | Data Terminal | Minimal API interface for programmatic data access |
| `/co-pilot` | Sustainability Co-Pilot | Contextual AI assistant for sustainability intelligence |

## Special Pages

| Route | Description | Purpose |
|-------|-------------|---------|
| `/analytics-dashboard` | Analytics Dashboard | Advanced visualization of sustainability metrics |
| `/monetization-opportunities` | Monetization Opportunities | Strategic insights for sustainable business models |
| `/sustainability` | Sustainability | Corporate sustainability intelligence dashboard |

## API Endpoints

| Route | Method | Description |
|-------|--------|-------------|
| `/api/metrics` | GET | Get sustainability metrics data |
| `/api/trends` | GET | Get sustainability trend data |
| `/api/storytelling` | POST | Generate AI storytelling content |
| `/api/search` | GET/POST | Unified search functionality |
| `/api/copilot` | POST | Co-Pilot AI assistant functionality |
| `/api/summarize` | POST | Summarize sustainability text using AI |
| `/api/predictive-analytics` | POST | Get predictive analytics for sustainability metrics |
| `/api/sustainability-analysis` | POST | Get sustainability analysis of business data |
| `/api/monetization-strategy` | POST | Get monetization strategy based on sustainability initiatives |
| `/api/apa-strategy` | POST | Get Assess-Plan-Act (APA) sustainability strategy |

## Legacy Redirects

The following legacy routes are maintained for backward compatibility but redirect to the new standardized routes:

| Legacy Route | Redirects To | Description |
|--------------|--------------|-------------|
| `/dashboard` | `/risk-tracker` | Legacy dashboard redirect |
| `/trend-analysis` | `/` | Legacy trend analysis redirect |
| `/search` | `/co-pilot` | Legacy search redirect |
| `/document-upload` | `/pdf-analyzer` | Legacy document upload redirect |
| `/sustainability-stories` | `/story-cards` | Legacy stories redirect |

## Debug Routes

| Route | Description | Purpose |
|-------|-------------|---------|
| `/debug` | Debug Route | Check registered routes and app status |

## Navigation Structure

The platform's navigation is organized into three main sections:

1. **Core** - Essential sustainability intelligence features
2. **Tools** - Specialized sustainability analysis tools
3. **Settings** - User and system configuration

This navigation structure is defined in `navigation_config.py` and should be maintained consistently across the application.