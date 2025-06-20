# Pinecone Vector Database Setup for LensIQ

This guide will help you set up Pinecone vector database for your LensIQ application.

## Prerequisites

1. **Pinecone Account**: Sign up for a free account at [pinecone.io](https://www.pinecone.io/)
2. **Python Environment**: Ensure you have Python 3.8+ installed

## Step 1: Get Pinecone API Key

1. Log in to your Pinecone console at [app.pinecone.io](https://app.pinecone.io/)
2. Navigate to "API Keys" in the left sidebar
3. Copy your API key (it should start with something like `pc-...`)
4. Note your environment (e.g., `us-west1-gcp`, `us-east1-gcp`, etc.)

## Step 2: Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

This will install:
- `pinecone-client>=3.0.0` - Pinecone Python SDK
- `sentence-transformers>=2.2.0` - For generating embeddings
- `openai>=1.0.0` - For OpenAI embeddings (optional)
- Other required dependencies

## Step 3: Configure Environment Variables

Update your `.env` file with your Pinecone credentials:

```env
# AI Service settings
PINECONE_API_KEY=your-actual-pinecone-api-key
PINECONE_ENVIRONMENT=us-west1-gcp
PINECONE_INDEX_NAME=lensiq-vectors
```

Replace:
- `your-actual-pinecone-api-key` with your actual Pinecone API key
- `us-west1-gcp` with your actual Pinecone environment
- `lensiq-vectors` with your preferred index name (optional)

## Step 4: Run Setup Script

Run the Pinecone setup script to initialize and test your vector database:

```bash
python scripts/setup_pinecone.py
```

This script will:
1. ✅ Check that all required environment variables are set
2. ✅ Initialize the Pinecone client
3. ✅ Create the vector index (if it doesn't exist)
4. ✅ Test basic operations (add, get, search, delete)
5. ✅ Verify everything is working correctly

## Step 5: Verify Setup

If the setup script runs successfully, you should see output like:

```
🚀 Starting Pinecone setup for LensIQ...
✅ Pinecone vector store initialized successfully
Testing vector store operations...
✅ add_item test passed
✅ get_item test passed
✅ search test passed
✅ count_items test passed (count: 1)
✅ delete_item test passed
🎉 All vector store tests passed!
🎉 Pinecone setup completed successfully!
Your Pinecone vector database is ready for use.
```

## Troubleshooting

### Common Issues

1. **"Pinecone API key not found"**
   - Make sure your `.env` file contains `PINECONE_API_KEY=your-key`
   - Ensure there are no extra spaces or quotes around the key
   - Verify the key is correct in your Pinecone console

2. **"Failed to initialize Pinecone client"**
   - Check that your API key is valid
   - Verify your environment name is correct
   - Ensure you have internet connectivity

3. **"Index creation failed"**
   - Check that you have permissions to create indexes
   - Verify you haven't exceeded your plan's index limit
   - Try using a different index name

4. **Import errors**
   - Run `pip install -r requirements.txt` to ensure all dependencies are installed
   - Check that you're using the correct Python environment

### Getting Help

If you encounter issues:

1. Check the [Pinecone documentation](https://docs.pinecone.io/)
2. Verify your account status and limits in the Pinecone console
3. Check the application logs for detailed error messages

## Usage

Once set up, you can use the vector store in your application:

```python
from src.data_management.vector_store import VectorStore

# Initialize vector store
vector_store = VectorStore()

# Add a vector
vector_store.add_item(
    item_id="example-001",
    embedding=[0.1, 0.2, 0.3, ...],  # 1536-dimensional vector
    metadata={"type": "company", "name": "Example Corp"},
    text="Example company description"
)

# Search for similar vectors
results = vector_store.search(
    query_embedding=[0.1, 0.2, 0.3, ...],
    top_k=5,
    filter_criteria={"type": "company"}
)
```

## Index Configuration

The default configuration creates an index with:
- **Dimension**: 1536 (compatible with OpenAI embeddings)
- **Metric**: Cosine similarity
- **Spec**: Serverless (AWS, region from PINECONE_ENVIRONMENT)

You can modify these settings in `src/data_management/vector_store.py` if needed.

## Next Steps

After successful setup:

1. **Populate with data**: Use the data population scripts to add your initial dataset
2. **Test search functionality**: Try searching for similar items in your application
3. **Monitor usage**: Check your Pinecone console for usage statistics
4. **Scale as needed**: Upgrade your Pinecone plan if you need more capacity

Your Pinecone vector database is now ready to power LensIQ's AI-driven features!
