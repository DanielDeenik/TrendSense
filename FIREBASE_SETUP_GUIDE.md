# Comprehensive Firebase Setup Guide for SustainaTrend

This guide provides detailed instructions on how to set up Firebase for your SustainaTrend application.

## Prerequisites

- A Google account
- Access to the [Firebase Console](https://console.firebase.google.com/)

## Step 1: Create a Firebase Project

1. Go to the [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project"
3. Enter "SustainaTrend" as the project name
4. Choose whether to enable Google Analytics (recommended)
5. Accept the terms and click "Create project"
6. Wait for the project to be created, then click "Continue"

## Step 2: Set Up Firestore Database

1. In the Firebase console, click on "Firestore Database" in the left sidebar
2. Click "Create database"
3. Choose "Start in production mode" (recommended for most applications)
4. Select a location close to your users (e.g., "us-central")
5. Click "Enable"
6. Wait for Firestore to be provisioned

## Step 3: Set Up Authentication (Optional)

If your application requires user authentication:

1. In the Firebase console, click on "Authentication" in the left sidebar
2. Click "Get started"
3. Enable the sign-in methods you want to use (e.g., Email/Password, Google, etc.)
4. Configure each sign-in method as needed

## Step 4: Create a Service Account Key

1. In the Firebase console, click on the gear icon (⚙️) next to "Project Overview" and select "Project settings"
2. Click on the "Service accounts" tab
3. Click "Generate new private key" button
4. Click "Generate key" in the dialog
5. Save the JSON file to your project directory as `firebase/service-account-key.json`

## Step 5: Enable Firestore API

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Make sure your Firebase project is selected in the project dropdown
3. In the left sidebar, navigate to "APIs & Services" > "Library"
4. Search for "Firestore API"
5. Click on "Cloud Firestore API"
6. Click "Enable" if it's not already enabled

## Step 6: Configure Your Application

1. Update your `.env` file with the following:

```
# Database Configuration
DATABASE_ADAPTER=firebase

# Firebase Configuration
FIREBASE_CREDENTIALS_PATH=firebase/service-account-key.json
FIREBASE_PROJECT_ID=your-project-id
```

Replace `your-project-id` with your actual Firebase project ID, which you can find in the service account key JSON file or in the Firebase console.

## Step 7: Install Firebase Dependencies

```bash
pip install firebase-admin
```

## Step 8: Test Your Firebase Connection

Run the test script to verify that you can connect to Firebase:

```bash
python test_real_firebase.py
```

If the test is successful, you should see output indicating that the connection was established and a test document was created and deleted.

## Troubleshooting

### Error: "Cloud Firestore API has not been used in project X before or it is disabled"

This means that the Firestore API needs to be enabled for your project. Follow Step 5 above to enable it.

### Error: "Permission denied on resource project X"

This could be due to one of the following issues:

1. The service account key doesn't have the necessary permissions. Make sure you're using a service account key with the "Firebase Admin" role.
2. The project ID in your `.env` file doesn't match the project ID in the service account key. Make sure they match.
3. The Firestore API is not enabled for your project. Follow Step 5 above to enable it.

### Error: "Failed to parse private key"

This could be due to the private key in the service account key file being in an incorrect format. Try generating a new service account key.

## Using the Mock Firebase Adapter

If you're having trouble setting up Firebase, you can use the mock Firebase adapter for development and testing:

1. Update your `.env` file:

```
DATABASE_ADAPTER=mock_firebase
```

2. Run your application as usual. The mock Firebase adapter will simulate a Firebase database in memory.

Note that data stored in the mock Firebase adapter will be lost when your application restarts.

## Additional Resources

- [Firebase Documentation](https://firebase.google.com/docs)
- [Firebase Admin SDK for Python](https://firebase.google.com/docs/admin/setup#python)
- [Firestore Documentation](https://firebase.google.com/docs/firestore)
- [Google Cloud Console](https://console.cloud.google.com/)
