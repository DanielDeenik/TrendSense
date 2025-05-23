# How to Set Up Firestore Database for Your Firebase Project

The Firebase adapter is now correctly connecting to your Firebase project, but the Firestore database doesn't exist yet. Follow these steps to set up the Firestore database:

## Step 1: Open the Firebase Console

1. Go to the Firebase Console: https://console.firebase.google.com/
2. Make sure you're signed in with the same Google account that you used to create the Firebase project.
3. Select your Firebase project: `sustainatrend-b443a`.

## Step 2: Create a Firestore Database

1. In the left sidebar, click on "Firestore Database".
2. Click "Create database".
3. Choose "Start in production mode" (recommended for most applications).
4. Select a location close to your users (e.g., "us-central").
5. Click "Enable".

## Step 3: Wait for the Database to be Created

1. After clicking "Enable", wait a few minutes for the database to be fully created.
2. You'll see the Firestore Database console when the database is ready.

## Step 4: Test the Connection Again

1. After creating the Firestore database, run the sample data generation script again:

```bash
python generate_sample_data.py
```

2. Choose option 1 to generate and upload sample data to Firebase.
3. If everything is set up correctly, you should see a successful upload of sample data.

## Alternative: Use the Direct URL

You can also directly visit the following URL to create the Firestore database:

[https://console.cloud.google.com/datastore/setup?project=sustainatrend-b443a](https://console.cloud.google.com/datastore/setup?project=sustainatrend-b443a)

Follow the prompts to create the database.

## Need Help?

If you're still having issues after following these steps, please let me know, and I'll help you troubleshoot further.
