from app import app
from app.dependecies import templates
from app.schemas import base

from fastapi import Request
from fastapi.responses import HTMLResponse


@app.get('/ping', response_model=base.Response)
async def ping():
    return base.Response(status='ok', message='🏓 pong')


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})
