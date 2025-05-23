# MongoDB Setup Guide for SustainaTrend

This guide provides detailed instructions on how to set up MongoDB for your SustainaTrend application.

## Option 1: Use MongoDB Atlas (Recommended)

MongoDB Atlas is a fully-managed cloud database service that makes it easy to set up, operate, and scale MongoDB deployments.

### Step 1: Create a MongoDB Atlas Account

1. Go to the [MongoDB Atlas website](https://www.mongodb.com/cloud/atlas/register)
2. Sign up for a free account or log in if you already have one

### Step 2: Create a New Cluster

1. Click "Build a Database"
2. Choose the "FREE" tier
3. Select your preferred cloud provider (AWS, Google Cloud, or Azure) and region
4. Click "Create Cluster"
5. Wait for the cluster to be created (this may take a few minutes)

### Step 3: Set Up Database Access

1. In the left sidebar, click on "Database Access" under "Security"
2. Click "Add New Database User"
3. Choose "Password" as the authentication method
4. Enter a username and password
5. Set "Database User Privileges" to "Atlas admin"
6. Click "Add User"

### Step 4: Set Up Network Access

1. In the left sidebar, click on "Network Access" under "Security"
2. Click "Add IP Address"
3. To allow access from anywhere, click "Allow Access from Anywhere" (not recommended for production)
4. For better security, add your specific IP address
5. Click "Confirm"

### Step 5: Get Connection String

1. In the left sidebar, click on "Database" under "Deployments"
2. Click "Connect" on your cluster
3. Click "Connect your application"
4. Copy the connection string
5. Replace `<password>` with your database user's password
6. Replace `<dbname>` with `sustainatrend`

### Step 6: Update Your .env File

Update your `.env` file with the MongoDB connection information:

```
# MongoDB Configuration
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster-url>/sustainatrend?retryWrites=true&w=majority
MONGODB_DB=sustainatrend
MONGODB_USERNAME=<username>
MONGODB_PASSWORD=<password>
```

Replace `<username>`, `<password>`, and `<cluster-url>` with your actual values.

## Option 2: Use Local MongoDB

If you prefer to run MongoDB locally, follow these steps:

### Step 1: Install MongoDB Community Edition

#### Windows

1. Download the MongoDB Community Edition installer from the [MongoDB Download Center](https://www.mongodb.com/try/download/community)
2. Run the installer and follow the instructions
3. Choose "Complete" installation
4. Install MongoDB Compass (optional but recommended)

#### macOS

Using Homebrew:

```bash
brew tap mongodb/brew
brew install mongodb-community
```

#### Linux (Ubuntu)

```bash
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
```

### Step 2: Start MongoDB Service

#### Windows

MongoDB should be running as a service. If not, you can start it from the Services console.

#### macOS

```bash
brew services start mongodb-community
```

#### Linux (Ubuntu)

```bash
sudo systemctl start mongod
```

### Step 3: Create a Database and User

1. Open a terminal or command prompt
2. Connect to MongoDB:

```bash
mongo
```

3. Create a database:

```javascript
use sustainatrend
```

4. Create a user:

```javascript
db.createUser({
  user: "your_username",
  pwd: "your_password",
  roles: [{ role: "readWrite", db: "sustainatrend" }]
})
```

### Step 4: Update Your .env File

Update your `.env` file with the MongoDB connection information:

```
# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/sustainatrend
MONGODB_DB=sustainatrend
MONGODB_USERNAME=your_username
MONGODB_PASSWORD=your_password
```

## Testing Your MongoDB Connection

Run the following script to test your MongoDB connection:

```bash
python test_mongodb.py
```

If the connection is successful, you should see output indicating that the connection was established and a test document was created and deleted.

## Using the Dual Database Adapter

The dual database adapter allows you to write to both Firebase and MongoDB simultaneously. To use it, set the following in your `.env` file:

```
# Database Configuration
DATABASE_ADAPTER=dual

# Dual Database Configuration
PRIMARY_DATABASE_ADAPTER=firebase
SECONDARY_DATABASE_ADAPTER=mongodb
```

This will use Firebase as the primary database for reads and write to both Firebase and MongoDB for writes.

## Migrating Data Between Databases

To migrate data between Firebase and MongoDB, use the migration utility:

```bash
python migrate_data.py
```

This will prompt you to choose one of the following options:

1. Migrate data from Firebase to MongoDB
2. Migrate data from MongoDB to Firebase
3. Sync data from Firebase to MongoDB
4. Sync data from MongoDB to Firebase

Choose the option that best suits your needs.

## Need Help?

If you're still having issues after following these steps, please let me know, and I'll help you troubleshoot further.
