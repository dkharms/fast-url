from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from deta import Deta
import hashlib
import models
import os

app = FastAPI()
deta = Deta(os.getenv('DETA_PROJECT_KEY'))
db_urls = deta.Base('urls')


async def write_record(url):
    hashed = hashlib.md5(url.encode('utf-8')).hexdigest()
    if not db_urls.get(hashed):
        db_urls.put(url, hashed)
    return hashed


@app.get('/ping', response_model=models.Response)
async def ping():
    return models.Response(status='ok', message='pong')


@app.post('/short', response_model=models.UrlResponse)
async def short_url(url_model: models.UrlCreate, request: Request):
    hashed = await write_record(url_model.url)
    return models.UrlResponse(
        message=f'Created tiny url for {url_model}',
        status='ok', url=f'https://{request.url.hostname}/{hashed}'
    )


@app.get("/{shortened_url}")
async def redirect_to(shortened_url: str):
    full_url = db_urls.get(shortened_url)
    if not full_url:
        return HTTPException(404, f'{shortened_url} does not exist!')
    return RedirectResponse(full_url['value'])
