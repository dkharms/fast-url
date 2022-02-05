import hashlib

from urllib.parse import urlparse

from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse

from app import app
from app.dependecies import db_urls
from app.schemas.base import Response
from app.schemas.url import UrlCreate, UrlResponse


async def write_record(host, url):
    hashed = hashlib.md5(url.encode('utf-8')).hexdigest()
    key = f'{host}-{hashed}'

    if not db_urls.get(key):
        db_urls.put(url, key)

    return key


@app.get('/ping', response_model=Response)
async def ping():
    return Response(status='ok', message='pong')


@app.post('/short', response_model=UrlResponse)
async def short_url(url_model: UrlCreate, request: Request):
    hostname = urlparse(url_model.url).hostname
    key = await write_record(hostname, url_model.url)

    return UrlResponse(
        message=f'created tiny url for {url_model}',
        status='ok', url=f'https://{request.url.hostname}/{key}'
    )


@app.get("/{shortened_url}")
async def redirect_to(shortened_url: str):
    full_url = db_urls.get(shortened_url)

    if not full_url:
        return HTTPException(404, f'{shortened_url} does not exist!')

    return RedirectResponse(full_url['value'])
