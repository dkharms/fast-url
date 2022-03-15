from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:39613'],
    allow_credentials=True,
    allow_methods='*',
    allow_headers='*',
)

from app import routes
from app import middlewares
