import os
import pytest
from src.data_management.vector_store import VectorStore
import random
import string

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
PINECONE_ENV = os.environ.get('PINECONE_ENVIRONMENT')

pytestmark = pytest.mark.skipif(
    not (PINECONE_API_KEY and PINECONE_ENV),
    reason='Pinecone environment variables not set.'
)

def random_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

def random_embedding(dim=1536):
    return [random.random() for _ in range(dim)]

def test_add_and_get_item():
    store = VectorStore()
    item_id = random_id()
    embedding = random_embedding()
    metadata = {'type': 'test', 'foo': 'bar'}
    text = 'Test vector'
    store.add_item(item_id, embedding, metadata, text)
    item = store.get_item(item_id)
    assert item is not None
    assert item['metadata']['type'] == 'test'
    store.delete_item(item_id)

def test_search():
    store = VectorStore()
    item_id = random_id()
    embedding = random_embedding()
    metadata = {'type': 'search', 'foo': 'bar'}
    text = 'Searchable vector'
    store.add_item(item_id, embedding, metadata, text)
    results = store.search(embedding, top_k=1)
    assert results
    assert results[0]['id'] == item_id
    store.delete_item(item_id)

def test_metadata_filter():
    store = VectorStore()
    item_id = random_id()
    embedding = random_embedding()
    metadata = {'type': 'filtertest', 'foo': 'baz'}
    text = 'Filter vector'
    store.add_item(item_id, embedding, metadata, text)
    results = store.search(embedding, top_k=5, filter_criteria={'type': {'$eq': 'filtertest'}})
    assert any(r['id'] == item_id for r in results)
    store.delete_item(item_id)

def test_delete_and_clear():
    store = VectorStore()
    item_id = random_id()
    embedding = random_embedding()
    metadata = {'type': 'delete', 'foo': 'zap'}
    text = 'Delete vector'
    store.add_item(item_id, embedding, metadata, text)
    store.delete_item(item_id)
    assert store.get_item(item_id) is None
    # Optionally test clear (dangerous if sharing index)
    # store.clear()
