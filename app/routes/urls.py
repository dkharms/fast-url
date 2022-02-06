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
    key = f'{host}-{hashed[len(hashed) // 2:]}'
    if not db_urls.get(key):
        db_urls.put(url, key)

    return key


async def construct_valid_url(url):
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        return f'https://{url}'

    return url


@app.get('/ping', response_model=Response)
async def ping():
    return Response(status='ok', message='pong')


@app.post('/short', response_model=UrlResponse)
async def short_url(url_model: UrlCreate, request: Request):
    valid_url = await construct_valid_url(url_model.url)
    hostname = urlparse(valid_url).hostname
    key = await write_record(hostname, valid_url)

    return UrlResponse(
        message=f'created tiny url for {url_model}',
        status='ok', url=f'https://{request.url.hostname}/{key}'
    )


@app.get("/{shortened_url}")
async def redirect_to(shortened_url: str):
    full_url = db_urls.get(shortened_url)
    if not full_url:
        return HTTPException(404, f'{shortened_url} does not exist!')
    valid_url = await construct_valid_url(full_url['value'])

    return RedirectResponse(valid_url)
