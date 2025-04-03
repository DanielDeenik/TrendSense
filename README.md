# SustainaTrend™ Platform

An advanced AI-powered sustainability intelligence platform that transforms complex environmental data into engaging, interactive insights through cutting-edge technology and immersive document analysis.

## Overview

SustainaTrend™ is an AI-first sustainability analytics platform specialized for venture capital and private equity firms. The system analyzes portfolio companies, tracks deal flow, and detects investment patterns using both structured and unstructured data. It features multi-tenant data isolation while enabling anonymized cross-portfolio pattern recognition to identify investment trends, founder archetypes, and market opportunities.

## Core Features

- **AI-Driven Analysis**: Leverage advanced AI models to extract insights from sustainability data
- **Pattern Recognition**: Identify trends across portfolio companies while maintaining data privacy
- **Interactive Dashboards**: Visualize key sustainability metrics and ESG performance
- **Document Processing**: Analyze sustainability reports and environmental documents 
- **Portfolio Tracking**: Monitor sustainability performance across investments
- **Temporal Analysis**: Track changes in sustainability metrics over time
- **Sentiment Analysis**: Combine quantitative data with sentiment trends

## Technical Stack

- **Frontend**: SvelteKit with Tailwind CSS for responsive design
- **Backend**: Node.js/Express + Python FastAPI microservices architecture
- **Database**: PostgreSQL (structured data) + optional MongoDB (document data)
- **AI Integration**: OpenAI API for advanced text analysis
- **Data Visualization**: Interactive charts and dashboards

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL database

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/sustainatrend.git
   cd sustainatrend
   ```

2. Run the setup script:
   ```
   bash setup.sh
   ```

3. Configure your database connection in `.env`

4. Start the application:
   ```
   bash start.sh
   ```

5. Access the application at http://localhost:5000

## Configuration

Create a `.env` file with the following environment variables:

```
DATABASE_URL=postgresql://username:password@localhost:5432/sustainatrend
OPENAI_API_KEY=your_openai_api_key
PORT=5000
```

## Architecture

The SustainaTrend™ platform follows a hybrid microservices architecture:

1. **Data Capture Layer**: Multi-tenant data collection from various sources
2. **Analytics Layer**: AI-powered analysis of sustainability metrics
3. **Pattern Recognition Engine**: Federated pattern identification across portfolios
4. **Presentation Layer**: Interactive dashboards and visualization tools

## Documentation

- [API Documentation](./ROUTE-DOCUMENTATION.md)
- [Architecture Overview](./ARCHITECTURE.md)
- [AI Integration](./AI-DRIVEN-ARCHITECTURE.md)

## License

This project is proprietary and confidential.

© 2025 SustainaTrend. All rights reserved.