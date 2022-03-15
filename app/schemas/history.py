from pydantic import BaseModel
from typing import List

from app.schemas.base import Response


class HistoryEntry(BaseModel):
    full_url: str
    shortened_url: str


class History(Response):
    history_entries: List[HistoryEntry]
