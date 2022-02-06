import app.schemas.base as base

from app import app
from app.dependecies import templates

from fastapi import Request


@app.get('/', response_model=base.Response)
async def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})
