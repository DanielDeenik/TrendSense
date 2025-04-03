# SustainaTrend™ Intelligence Platform - Architecture Overview

## System Architecture

The SustainaTrend™ platform implements a modular, Flask-based web application architecture designed for sustainability data analysis, document processing, and AI-powered insights generation.

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Browser                          │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                   Flask Web Application                      │
│                                                             │
│  ┌─────────────┐  ┌────────────┐  ┌─────────────────────┐   │
│  │  Templates  │  │   Routes   │  │  Service Modules    │   │
│  └─────────────┘  └────────────┘  └─────────────────────┘   │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                 External Services & Data                     │
│                                                             │
│  ┌─────────────┐  ┌────────────┐  ┌─────────────────────┐   │
│  │ PostgreSQL  │  │ Google AI  │  │    Document         │   │
│  │  Database   │  │  (Gemini)  │  │    Processing       │   │
│  └─────────────┘  └────────────┘  └─────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Core Application Components

### 1. Frontend Layer

The frontend is implemented as a Flask web application with Jinja2 templates, structured around a modular blueprint-based architecture:

**Key Components:**
- **Templates Directory**: Contains all HTML templates organized by feature
- **Static Assets**: CSS, JavaScript, and image resources
- **Layouts**: Base templates with shared structure (finchat_dark_layout.html)
- **Component Templates**: Reusable UI components (cards, metrics, etc.)

### 2. Application Routes

The application is organized into modular blueprint-based routes for different functional areas:

**Primary Route Modules:**
- **Dashboard Routes**: Main dashboard interface and sustainability metrics
- **Document Routes**: Document processing, upload, and analysis
- **Strategy Routes**: AI-powered strategy generation and storytelling
- **Trend Analysis Routes**: Sustainability trend visualization and analysis
- **Performance Routes**: Detailed performance assessment and monitoring

**Key Route Structure:**
```
frontend/
├── routes/
│   ├── __init__.py              # Blueprint registration
│   ├── dashboard.py             # Main dashboard views
│   ├── performance.py           # Performance metrics
│   ├── overview.py              # Platform overview
│   ├── enhanced_strategy.py     # Strategy generation
│   ├── trend.py                 # Trend analysis
│   ├── documents/               # Document-related routes
│   │   ├── __init__.py
│   │   └── document_routes.py   # Document processing & analysis
```

### 3. Service Layer

The service layer contains business logic and integrations with external systems:

**Key Services:**
- **Document Processing**: Extracting and analyzing sustainability data from documents
- **AI Integration**: Connecting to Google Gemini or other LLMs
- **Data Access**: Database interaction and data management
- **Visualization**: Chart generation and data formatting

**Service Structure:**
```
frontend/
├── services/
│   ├── regulatory_ai_service.py     # AI for regulatory analysis
│   ├── ai_connector.py              # Generic AI service connector
│   ├── document_processor.py        # Document parsing and extraction
│   └── visualization_service.py     # Chart and graph generation
```

### 4. Data Layer

Data persistence is handled through various storage mechanisms:

**Storage Components:**
- **PostgreSQL Database**: Core structured data storage for metrics and user data
- **File Storage**: Document storage for uploaded sustainability reports
- **Session Storage**: Temporary data for in-progress analyses

## Core Functional Modules

### Dashboard Module

The dashboard provides real-time visualization of key sustainability metrics and serves as the main entry point to the platform.

**Key Features:**
- Metric cards for key performance indicators
- Comparative charts for ESG scores
- Progress tracking against sustainability targets
- Historical performance trends

**Implementation:**
- `/dashboard/` route in `routes/dashboard.py`
- Template: `templates/dashboard.html`
- Card components for modular organization

### Document Hub Module

The document hub provides a unified interface for uploading, analyzing, and extracting insights from sustainability documents.

**Key Features:**
- Document upload with drag-and-drop functionality
- Tabbed interface (Upload, Regulatory, Analysis)
- Horizontal regulatory timeline visualization
- Document compliance assessment

**Implementation:**
- `/documents/document-hub` route in `routes/documents/document_routes.py`
- Template: `templates/integrated_document_hub.html`
- Tabbed navigation using JavaScript for content switching

### Strategy Hub Module

The strategy hub (formerly "Stories") provides AI-generated strategic recommendations and storytelling for sustainability initiatives.

**Key Features:**
- Framework-based strategy generation
- Monetization and implementation planning
- Competitive benchmarking
- Strategy visualization and export

**Implementation:**
- `/strategy/` routes in `routes/enhanced_strategy.py`
- Integration with AI services for content generation
- Standardized strategy structure and formatting

### Trend Analysis Module

The trend analysis module enables deep exploration of sustainability metrics over time with AI-powered insights.

**Key Features:**
- Time-series analysis of key metrics
- Forecasting and predictive analytics
- Industry benchmarking
- AI-driven question answering

**Implementation:**
- `/trends/` routes in `routes/trend.py`
- Integration with visualization libraries for interactive charts
- Natural language query processing for metric exploration

## Technical Implementation

### UI Framework

The user interface is built with a customized component system:

**Key UI Elements:**
- **Layout System**: CSS Grid-based responsive layout
- **Sidebar Navigation**: Collapsible sidebar with categorized links
- **Card System**: Standardized card components for content organization
- **Data Visualization**: Chart.js integration for metrics and trends
- **Tabbed Interface**: Custom tab switching for document hub

### Integration Points

The platform integrates with external services for enhanced functionality:

**External Integrations:**
- **Google Generative AI (Gemini)**: For document analysis and AI-powered insights
- **PostgreSQL Database**: For structured data storage
- **PDF Processing**: Using PyMuPDF and related libraries
- **Chart Rendering**: Using Chart.js, Plotly, or Bokeh

### Front-End Technologies

- **Template Engine**: Jinja2 for server-side rendering
- **CSS Framework**: Custom CSS with design system variables
- **JavaScript**: Vanilla JS with modern ES6 features
- **Visualization**: Chart.js and custom visualization components

### Back-End Technologies

- **Web Framework**: Flask with blueprint-based architecture
- **Database Access**: Direct PostgreSQL connection
- **Document Processing**: PyMuPDF, BeautifulSoup4, etc.
- **AI Integration**: Google Generative AI SDK

## Application Flow

### Standard Request Flow

1. User navigates to a route (e.g., `/dashboard/`)
2. Flask routes the request to the appropriate blueprint handler
3. Route handler retrieves necessary data from services
4. Template is rendered with the data context
5. Response is returned to the browser

### Document Processing Flow

1. User uploads a document on the document hub
2. Document is saved to the uploads directory
3. Document processor extracts text and structure
4. AI services analyze the content for insights
5. Results are displayed in the appropriate tab

### AI Interaction Flow

1. User submits a query in an AI-enabled interface
2. Request is sent to the appropriate service endpoint
3. Service formats the query and sends to AI provider (e.g., Google Gemini)
4. Response is processed and formatted
5. Results are displayed to the user with visualizations

## Deployment Configuration

The application is configured for Replit deployment:

**Key Configuration Elements:**
- Flask running on `0.0.0.0` host for Replit compatibility
- ProxyFix middleware for proper request handling
- Environment variable configuration
- Port management for service conflicts

## Future Architecture Considerations

**Planned Enhancements:**
- Enhanced microservices architecture for better separation of concerns
- Improved API-driven frontend with more interactive components
- Expanded AI integration for deeper document analysis
- Real-time update capabilities for collaborative analysis
- Comprehensive data pipeline for automated sustainability reporting