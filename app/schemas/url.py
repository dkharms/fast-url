from app.schemas.base import Response
from pydantic import BaseModel


class UrlCreate(BaseModel):
    url: str


class UrlResponse(Response):
    url: str
