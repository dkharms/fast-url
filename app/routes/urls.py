import hashlib
import logging
import uuid

from urllib.parse import urlparse

from fastapi import HTTPException, Request, Response
from fastapi.responses import RedirectResponse

from app import app
from app.dependecies import db_urls, db_history
from app.schemas.url import UrlCreate, UrlResponse

letter_to_digit = {
    'a': '4', 'b': '8', 'e': '3',
    'i': '1', 'j': '9', 'l': '1',
    'o': '0', 'r': '2', 's': '5',
    't': '7',
}


def create_hash(host, url):
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
    key = create_hash(host, url)
    if not db_urls.get(key):
        db_urls.put(url, key)

    return key


def construct_valid_url(url):
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        return f'https://{url}'

    return url


async def short_url(url: str, request: Request):
    valid_url = construct_valid_url(url)
    hostname = urlparse(valid_url).hostname
    key = await write_record(hostname, valid_url)

    return f'https://{request.url.hostname}/{key}'


async def put_history_entry(user_id: str, full_url: str, shortened_url: str):
    user_entry = db_history.get(user_id) or []
    if user_entry:
        user_entry = user_entry['value']

    user_entry.append({full_url: shortened_url})
    db_history.put(user_entry, user_id)


@app.post('/short', response_model=UrlResponse)
async def short_url_api(url_model: UrlCreate, request: Request, response: Response):
    url = await short_url(url_model.url, request)

    user_id = request.cookies.get('user-id', str(uuid.uuid4()))
    await put_history_entry(user_id, url_model.url, url)
    response.set_cookie('user-id', user_id)

    return UrlResponse(
        message='🚀 created tiny url',
        status='ok', url=url
    )


@app.get("/{shortened_url}")
async def redirect_to(shortened_url: str):
    full_url = db_urls.get(shortened_url)
    if not full_url:
        return HTTPException(404, f'🔴 {shortened_url} does not exist!')
    valid_url = construct_valid_url(full_url['value'])

    return RedirectResponse(valid_url)
