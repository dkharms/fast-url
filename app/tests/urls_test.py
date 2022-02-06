from app import app
from app.schemas import base
from urllib.parse import urlparse

from fastapi.testclient import TestClient

client = TestClient(app)


def test_ping():
    response = client.request('GET', '/ping')

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "pong"}


def test_short_url():
    url = 'https://google.com'
    response = client.request('POST', '/short', json={'url': url})
    assert response.status_code == 200

    shorten_url = urlparse(response.json()['url']).path
    response_shorten = client.request('GET', shorten_url)
    assert response_shorten.status_code == 307
