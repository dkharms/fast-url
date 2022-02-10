import hashlib

from urllib.parse import urlparse

from fastapi import HTTPException, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse

from app import app
from app.dependecies import db_urls, templates
from app.schemas.url import UrlCreate, UrlResponse

letter_to_digit = {
    'a': '4', 'b': '8', 'e': '3',
    'i': '1', 'j': '9', 'l': '1',
    'o': '0', 'r': '2', 's': '5',
    't': '7',
}


async def create_hash(host, url):
    host_letters = list(host)
    hash_letters = list(hashlib.md5(url.encode('utf-8')).hexdigest())

    for index, letter in enumerate(host_letters):
        if letter in hash_letters:
            hash_letters.remove(letter)
        elif letter in letter_to_digit and letter_to_digit[letter] in hash_letters:
            host_letters[index] = letter_to_digit[letter]
            hash_letters.remove(letter_to_digit[letter])

    return f'{"".join(host_letters)}{"".join(hash_letters[:len(hash_letters) // 4])}'


async def write_record(host, url):
    key = await create_hash(host, url)
    if not db_urls.get(key):
        db_urls.put(url, key)

    return key


async def construct_valid_url(url):
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        return f'https://{url}'

    return url


async def short_url(url: str, request: Request):
    valid_url = await construct_valid_url(url)
    hostname = urlparse(valid_url).hostname
    key = await write_record(hostname, valid_url)

    return f'https://{request.url.hostname}/{key}'


@app.post('/short', response_model=UrlResponse)
async def short_url_api(url_model: UrlCreate, request: Request):
    url = await short_url(url_model.url, request)

    return UrlResponse(
        message='🚀 created tiny url',
        status='ok', url=url
    )


@app.get("/{shortened_url}")
async def redirect_to(shortened_url: str):
    full_url = db_urls.get(shortened_url)
    if not full_url:
        return HTTPException(404, f'🔴 {shortened_url} does not exist!')
    valid_url = await construct_valid_url(full_url['value'])

    return RedirectResponse(valid_url)
