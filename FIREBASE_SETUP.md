# Firebase Setup for SustainaTrend

This guide will help you set up Firebase as a database backend for SustainaTrend.

## Prerequisites

- A Google account
- Node.js and npm installed (for Firebase CLI)
- Python 3.7+ with pip

## Step 1: Create a Firebase Project

1. Go to the [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project" and follow the steps to create a new project named "SustainaTrend"
3. Once the project is created, you'll need to set up Firestore

## Step 2: Set Up Firestore Database

1. In the Firebase console, go to "Firestore Database"
2. Click "Create database"
3. Choose "Start in production mode" and select a location close to your users
4. Click "Enable"

## Step 3: Get Firebase Credentials

1. In the Firebase console, go to Project Settings > Service Accounts
2. Click "Generate new private key" to download a JSON file with your credentials
3. Save this file in your project directory as `firebase/service-account-key.json`

## Step 4: Install Firebase Dependencies

```bash
pip install -r firebase_requirements.txt
```

## Step 5: Configure Environment Variables

Update your `.env` file with the following:

```
# Database Configuration
DATABASE_ADAPTER=firebase

# Firebase Configuration
FIREBASE_CREDENTIALS_PATH=firebase/service-account-key.json
FIREBASE_PROJECT_ID=your-project-id
```

Replace `your-project-id` with your actual Firebase project ID.

## Step 6: Test Firebase Connection

Run the test script to verify that you can connect to Firebase:

```bash
python test_real_firebase.py
```

If the test is successful, you should see output indicating that the connection was established and a test document was created and deleted.

## Step 7: Generate Sample Data (Optional)

If you want to populate your Firebase database with sample data, run:

```bash
python generate_sample_data.py
```

Follow the prompts to generate and upload sample data to Firebase.

## Step 8: Migrate Data from MongoDB (Optional)

If you have existing data in MongoDB that you want to migrate to Firebase, run:

```bash
python migrate_to_firebase.py
```

Follow the prompts to migrate your data from MongoDB to Firebase.

## Switching Between Database Adapters

You can switch between database adapters by changing the `DATABASE_ADAPTER` environment variable in your `.env` file:

- `firebase`: Use the real Firebase adapter
- `mongodb`: Use the MongoDB adapter
- `mock_firebase`: Use the mock Firebase adapter (for testing without Firebase credentials)

## Troubleshooting

### Firebase Connection Issues

If you're having trouble connecting to Firebase, check the following:

1. Make sure your `firebase/service-account-key.json` file exists and contains valid credentials
2. Make sure your `FIREBASE_PROJECT_ID` environment variable matches your Firebase project ID
3. Make sure you have the Firebase Admin SDK installed: `pip install firebase-admin`

### Data Migration Issues

If you're having trouble migrating data from MongoDB to Firebase, check the following:

1. Make sure your MongoDB server is running and accessible
2. Make sure your MongoDB connection string is correct
3. Make sure your MongoDB database and collections exist

## Additional Resources

- [Firebase Documentation](https://firebase.google.com/docs)
- [Firebase Admin SDK for Python](https://firebase.google.com/docs/admin/setup#python)
- [Firestore Documentation](https://firebase.google.com/docs/firestore)
