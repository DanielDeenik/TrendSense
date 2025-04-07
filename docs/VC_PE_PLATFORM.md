# TrendSense™ VC/PE Intelligence Platform

## Overview

TrendSense™ has been optimized as a specialized AI-first sustainability analytics platform exclusively for venture capital and private equity firms. The system analyzes portfolio companies, tracks deal flow, and detects investment patterns using both structured and unstructured data.

## Key Features

- **Multi-Tenant Data Isolation**: Secure data separation for different funds
- **Federated Pattern Recognition**: Cross-portfolio pattern detection with data anonymization
- **AI-Powered Pattern Explanations**: Intelligent analysis of detected patterns
- **Real-time Sentiment Analysis**: News, social media, and investor sentiment tracking
- **Benchmarking & Peer Comparison**: Compare companies against anonymized peer groups

## Architecture

The platform uses a modern stack:

- **Backend**: Python (Flask + FastAPI) with PostgreSQL database
- **Frontend**: Responsive web interface with Chart.js visualizations
- **AI**: Google Gemini (primary) and OpenAI (fallback) for analysis
- **Analytics**: Real-time pattern detection engine

## VC/PE-Specific Workflows

1. **Portfolio Monitoring**
   - KPI tracking with sector-specific metrics
   - Sentiment and virality trend detection
   - Risk identification and alerts

2. **Pattern Detection**
   - Identify emerging trends across portfolio companies
   - Detect sector-specific investment opportunities
   - Analyze success factors in high-performing investments

3. **Benchmarking**
   - Compare portfolio companies to sector peers
   - Track sentiment and performance relative to market
   - Identify outperformers and underperformers

4. **Federated Insights**
   - Cross-fund pattern detection with anonymization
   - Sector-specific trend analysis
   - Success factor identification across funds

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL database
- Google Gemini API key (primary)
- OpenAI API key (fallback)

### Environment Setup

1. Ensure your environment has the following variables:
   - `DATABASE_URL`: PostgreSQL connection string
   - `GOOGLE_API_KEY`: Google Gemini API key
   - `OPENAI_API_KEY`: OpenAI API key (optional fallback)

2. Run the setup check script:
   ```bash
   python ./scripts/setup_check.py
   ```

3. Start the platform:
   ```bash
   ./start-vc-platform.sh
   ```

## Cleaning Up Legacy Components

If you're upgrading from a previous version of TrendSense™, run the cleanup script to remove legacy components:

```bash
./scripts/clean.sh
```

This will:
- Remove storytelling and general-purpose templates
- Clean up redundant routes and APIs
- Streamline the database schema for VC/PE workflows
- Back up removed components to `./backup_deleted_files/`

## Modules Overview

### Core Modules

- **Pattern Engine** (`frontend/trendsense/pattern_engine.py`): Detects investment patterns across portfolios
- **AI Connector** (`frontend/utils/ai_connector.py`): Interfaces with Google Gemini and OpenAI
- **Storage Interface** (`server/storage.ts`): Database operations and data access layer
- **Schema** (`shared/schema.ts`): Database schema and entity definitions

### Key Interfaces

- **VC Dashboard** (`frontend/templates/trendsense/vc_dashboard.html`): Main dashboard for fund managers
- **Federated Patterns** (`frontend/templates/trendsense/federated_patterns.html`): Cross-fund pattern analysis
- **Company Analysis** (`frontend/templates/trendsense/vc_company_analysis.html`): Detailed company insights

## Extending the Platform

To add new VC/PE-specific metrics or analyses:

1. Update the schema in `shared/schema.ts`
2. Add corresponding storage operations in `server/storage.ts`
3. Create or modify routes in the relevant module
4. Update or create templates in `frontend/templates/trendsense/`

## Roadmap

- **Advanced Portfolio Optimization**: Recommendation engine for portfolio balancing
- **Deal Flow Automation**: AI-powered deal screening and prioritization
- **Real-time Market Correlation**: Connect company performance to broader market indicators
- **ESG Impact Analysis**: Detailed sustainability impact measurement for portfolio companies