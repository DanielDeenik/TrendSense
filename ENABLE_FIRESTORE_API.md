# How to Enable Firestore API for Your Firebase Project

The Firebase adapter is now correctly connecting to your Firebase project, but the Firestore API is not enabled. Follow these steps to enable it:

## Step 1: Open the Google Cloud Console

1. Go to the Google Cloud Console: https://console.cloud.google.com/
2. Make sure you're signed in with the same Google account that you used to create the Firebase project.

## Step 2: Select Your Project

1. In the top navigation bar, click on the project dropdown.
2. Select your Firebase project: `sustainatrend-b443a`.

## Step 3: Enable the Firestore API

1. Navigate to the API Library by clicking on "APIs & Services" > "Library" in the left sidebar.
2. Search for "Firestore API" or "Cloud Firestore API".
3. Click on "Cloud Firestore API" in the search results.
4. Click the "Enable" button.

## Step 4: Wait for the API to be Enabled

1. After clicking "Enable", wait a few minutes for the API to be fully enabled.
2. You'll see a confirmation message when the API is enabled.

## Step 5: Create a Firestore Database

1. Go to the Firebase Console: https://console.firebase.google.com/
2. Select your project: `sustainatrend-b443a`.
3. In the left sidebar, click on "Firestore Database".
4. Click "Create database".
5. Choose "Start in production mode" (recommended for most applications).
6. Select a location close to your users (e.g., "us-central").
7. Click "Enable".

## Step 6: Test the Connection Again

1. After enabling the Firestore API and creating a Firestore database, run the adapter test again:

```bash
python adapter_test.py
```

2. If everything is set up correctly, you should see a successful connection and document insertion.

## Alternative: Use the Direct URL

You can also directly visit the following URL to enable the Firestore API:

[https://console.developers.google.com/apis/api/firestore.googleapis.com/overview?project=sustainatrend-b443a](https://console.developers.google.com/apis/api/firestore.googleapis.com/overview?project=sustainatrend-b443a)

Click the "Enable" button on that page.

## Need Help?

If you're still having issues after following these steps, please let me know, and I'll help you troubleshoot further.
