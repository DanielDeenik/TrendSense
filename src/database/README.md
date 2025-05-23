# TrendSense Database Adapter System

This directory contains the database adapter system for TrendSense. The system provides a flexible way to switch between different database backends without changing the application code.

## Overview

The database adapter system uses the adapter pattern to abstract away the details of the underlying database. This allows the application to work with different database backends (MongoDB, Firebase, etc.) without changing the application code.

## Components

- `adapters/`: Contains the database adapters
  - `base_adapter.py`: Defines the interface for database adapters
  - `mongodb_adapter.py`: MongoDB adapter implementation
  - `firebase_adapter.py`: Firebase adapter implementation
- `database_service.py`: Provides a unified database service
- `db_manager.py`: Provides a database manager that uses the database service
- `migration_utils.py`: Utilities for migrating data between database backends
- `db_cli.py`: Command-line interface for database operations

## Usage

### Configuration

The database adapter system is configured using environment variables. The following variables are used:

- `DATABASE_ADAPTER`: The database adapter to use (`mongodb` or `firebase`)
- `MONGODB_URI`: MongoDB connection URI
- `MONGODB_DATABASE`: MongoDB database name
- `MONGODB_USERNAME`: MongoDB username
- `MONGODB_PASSWORD`: MongoDB password
- `FIREBASE_CREDENTIALS_PATH`: Path to Firebase credentials JSON file
- `FIREBASE_PROJECT_ID`: Firebase project ID

### Using the Database Manager

The database manager provides a unified interface for database operations. It can be used as follows:

```python
from src.database.db_manager import db_manager

# Connect to the database
db_manager.connect()

# Get a collection
collection = db_manager.get_collection('users')

# Find documents
users = db_manager.find('users', {'active': True})

# Insert a document
user_id = db_manager.insert_one('users', {'name': 'John Doe', 'email': 'john@example.com'})

# Update a document
db_manager.update_one('users', {'_id': user_id}, {'$set': {'active': True}})

# Delete a document
db_manager.delete_one('users', {'_id': user_id})

# Disconnect from the database
db_manager.disconnect()
```

### Migrating Data

The migration utilities can be used to migrate data between database backends:

```python
from src.database.migration_utils import migrate_mongodb_to_firebase

# Migrate all collections from MongoDB to Firebase
migrate_mongodb_to_firebase()

# Migrate specific collections
migrate_mongodb_to_firebase(['users', 'products'])
```

### Command-Line Interface

The command-line interface provides a way to perform database operations from the command line:

```bash
# Set up Firebase
python -m src.database.db_cli setup --adapter firebase

# Test database connection
python -m src.database.db_cli test --adapter firebase

# Export MongoDB to JSON
python -m src.database.db_cli export --collections users products

# Import JSON to Firebase
python -m src.database.db_cli import --input-dir data_export

# Migrate MongoDB to Firebase
python -m src.database.db_cli migrate --collections users products
```

## Switching Between Database Backends

To switch between database backends, set the `DATABASE_ADAPTER` environment variable to the desired adapter:

```bash
# Use MongoDB
export DATABASE_ADAPTER=mongodb

# Use Firebase
export DATABASE_ADAPTER=firebase
```

Alternatively, you can update the `.env` file:

```
DATABASE_ADAPTER=firebase
```

## Firebase Setup

To use Firebase as a database backend, you need to:

1. Create a Firebase project at https://console.firebase.google.com/
2. Enable Firestore in the project
3. Generate a service account key:
   - Go to Project Settings > Service Accounts
   - Click "Generate new private key"
   - Save the JSON file
4. Set the `FIREBASE_CREDENTIALS_PATH` environment variable to the path of the JSON file
5. Set the `FIREBASE_PROJECT_ID` environment variable to your Firebase project ID
6. Install the Firebase Admin SDK: `pip install firebase-admin`

## MongoDB Setup

To use MongoDB as a database backend, you need to:

1. Install MongoDB: https://www.mongodb.com/try/download/community
2. Start the MongoDB server
3. Set the `MONGODB_URI` environment variable to the MongoDB connection URI
4. Set the `MONGODB_DATABASE` environment variable to the MongoDB database name
5. If using MongoDB Atlas, set the `MONGODB_USERNAME` and `MONGODB_PASSWORD` environment variables
