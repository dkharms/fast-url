import os
from deta import Deta
from fastapi.templating import Jinja2Templates

deta = Deta(os.getenv('DETA_PROJECT_KEY'))
db_urls = deta.Base('urls')
db_history = deta.Base('history')

templates = Jinja2Templates(directory='templates')
