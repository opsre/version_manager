# Version Manager Service

A Flask-based version management service that allows you to manage and track different versions of files.

## Features

- Version management with file upload support
- RESTful API endpoints
- Database integration with SQLAlchemy
- Logging system
- File download functionality

## Project Structure

```
version_service/
├── app/
│   ├── api/          # API routes and endpoints
│   ├── models/       # Database models
│   ├── services/     # Business logic
│   └── utils/        # Utility functions
├── config/           # Configuration files
├── logs/            # Log files
├── tests/           # Test files
└── uploads/         # Uploaded files
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with the following content:
```
SECRET_KEY=your-secret-key
DATABASE_URL=mysql+pymysql://username:password@localhost/version_manager
HOST=0.0.0.0
PORT=5000
LOG_LEVEL=INFO
LOG_PATH=logs
UPLOAD_FOLDER=uploads
```

4. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

5. Run the application:
```bash
python run.py
```

## API Endpoints

- `GET /api/versions` - Get all versions
- `GET /api/versions/<id>` - Get a specific version
- `POST /api/versions` - Create a new version
- `PUT /api/versions/<id>` - Update a version
- `DELETE /api/versions/<id>` - Delete a version
- `GET /api/versions/<id>/download` - Download version file

## Development

- The project uses Flask-SQLAlchemy for database operations
- Loguru for logging
- Flask-Migrate for database migrations
- Python-dotenv for environment variable management

## Testing

Run tests using pytest:
```bash
pytest
```