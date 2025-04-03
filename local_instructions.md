# Instructions for pushing code to GitHub locally

Since we're having issues pushing directly from Replit to GitHub, follow these steps to push the code from your local machine:

## Step 1: Clone the repository on your local machine

```bash
git clone https://github.com/DanielDeenik/TrendSense.git
cd TrendSense
```

## Step 2: Add Replit as a remote

```bash
git remote add replit https://replit.com/github/DanielDeenik/TrendSense
```

## Step 3: Pull changes from Replit

```bash
git pull replit main
```

## Step 4: Push to GitHub

```bash
git push origin main
```

This way, you'll be using your local GitHub credentials which are already set up correctly on your machine.

## Alternative: Export code as ZIP

If you prefer, you can:

1. Download all the code from Replit as a ZIP file
2. Extract it on your local machine
3. Copy the files to your local git repository
4. Commit and push from your local machine

This approach bypasses the need for complex remote configurations.