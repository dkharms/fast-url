import os

from deta import Deta
from fastapi import FastAPI

app = FastAPI()
deta = Deta(os.getenv('DETA_PROJECT_KEY'))
db_urls = deta.Base('urls')

import api.handlers
