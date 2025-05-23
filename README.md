# TrendSense™ Intelligence Platform

A comprehensive platform for sustainability trend analysis and investment intelligence.

## Overview

TrendSense™ is a web-based platform that provides tools and insights for sustainability trend analysis, investment intelligence, and strategy development. The platform includes several modules:

- **TrendSense™**: AI-powered sustainability trend analysis
- **TrendRadar™**: Real-time sustainability trend monitoring
- **VC Lens™**: Venture capital investment analysis for sustainability
- **Strategy Hub**: Tools for developing and analyzing sustainability strategies
- **Lookthrough**: Entity traversal and metrics propagation
- **Data Management**: Tools for managing sustainability data

## Project Structure

```
TrendSense/
├── app.py                  # Main application entry point
├── data/                   # Data files
├── firebase/               # Firebase configuration
├── logs/                   # Application logs
├── src/                    # Source code
│   ├── database/           # Database adapters and services
│   │   ├── adapters/       # Database adapters (Firebase, MongoDB)
│   │   └── ...
│   ├── data_management/    # Data management modules
│   ├── frontend/           # Frontend code
│   │   ├── routes/         # Flask routes
│   │   ├── static/         # Static assets
│   │   └── templates/      # HTML templates
│   └── lookthrough/        # Lookthrough module
├── tests/                  # Test files
├── uploads/                # User uploads
└── vector_db/              # Vector database files
```

## Setup and Installation

1. Clone the repository
2. Create a virtual environment: `python -m venv .venv`
3. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - Unix/MacOS: `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and configure environment variables
6. Run the application: `python app.py`

## Database Configuration

The application supports multiple database backends:

- **Firebase**: Set `DATABASE_ADAPTER=firebase` in `.env`
- **MongoDB**: Set `DATABASE_ADAPTER=mongodb` in `.env`
- **Mock Firebase**: Set `DATABASE_ADAPTER=mock_firebase` in `.env` (for development)
- **Dual Adapter**: Set `DATABASE_ADAPTER=dual` in `.env` (writes to both Firebase and MongoDB)

## Running Tests

Run tests using pytest:

```
pytest tests/
```

## License

Proprietary - All rights reserved.
