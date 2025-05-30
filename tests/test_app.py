import pytest
from app import app as flask_app

def test_health_check():
    with flask_app.test_client() as client:
        resp = client.get('/api/health')
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['status'] == 'ok'

def test_home_page():
    with flask_app.test_client() as client:
        resp = client.get('/')
        assert resp.status_code in (200, 302)  # allow redirect for login

def test_404():
    with flask_app.test_client() as client:
        resp = client.get('/nonexistent')
        assert resp.status_code == 404
        assert b'Not Found' in resp.data or b'404' in resp.data

def test_blueprints_registered():
    # Check that expected blueprints are registered
    blueprints = flask_app.blueprints
    assert 'api' in blueprints
    assert 'strategy' in blueprints
    assert 'data_management' in blueprints
    assert 'lookthrough' in blueprints
    assert 'graph_analytics' in blueprints
