# TrendSense™

TrendSense™ is a comprehensive platform for managing and analyzing portfolio companies' sustainability metrics and ESG data. It provides a robust data ingestion system, powerful analytics, and an intuitive user interface for VC and PE workflows.

## Features

- **Data Ingestion**
  - Support for multiple data formats (Excel, CSV, JSON)
  - Adapter-based architecture for easy extension
  - Automatic data normalization and validation
  - Detailed ingestion logging

- **Portfolio Management**
  - Comprehensive company profiles
  - Financial metrics tracking
  - Sustainability metrics monitoring
  - Team and board member management

- **Sustainability Analytics**
  - ESG score tracking
  - Carbon emissions monitoring
  - Water usage analysis
  - Waste management metrics
  - SDG alignment tracking

- **User Interface**
  - Modern, responsive design
  - Dark/light theme support
  - Interactive dashboards
  - Real-time notifications

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/trendsense.git
   cd trendsense
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Initialize the database:
   ```bash
   python scripts/init_db.py
   ```

## Configuration

The application can be configured through environment variables:

- `MONGODB_URI`: MongoDB connection URI
- `MONGODB_DATABASE`: Database name
- `FLASK_ENV`: Application environment (development/production)
- `FLASK_SECRET_KEY`: Secret key for session management
- `UPLOAD_FOLDER`: Directory for file uploads
- `MAX_CONTENT_LENGTH`: Maximum file upload size

## Usage

1. Start the development server:
   ```bash
   flask run
   ```

2. Access the application at `http://localhost:5000`

3. Import data:
   - Navigate to the Data Import page
   - Select your data file
   - Choose the appropriate adapter
   - Review and confirm the import

4. View and analyze data:
   - Use the dashboard for overview
   - Explore company profiles
   - Analyze sustainability metrics
   - Generate reports

## Development

### Project Structure

```
trendsense/
├── backend/
│   ├── config/
│   ├── database/
│   ├── ingest/
│   │   └── adapters/
│   └── schemas/
├── frontend/
│   ├── static/
│   └── templates/
├── scripts/
├── tests/
├── uploads/
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── app.py
```

### Running Tests

```bash
pytest
```

### Code Style

The project uses:
- Black for code formatting
- Flake8 for linting
- MyPy for type checking

Run the checks:
```bash
black .
flake8
mypy .
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the development team.