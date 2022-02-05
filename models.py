from typing import Optional
from pydantic import BaseModel


class Response(BaseModel):
    status: str
    message: Optional[str]


class UrlCreate(BaseModel):
    url: str


class UrlResponse(Response):
    url: str
