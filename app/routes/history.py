from typing import Dict, List

from fastapi import Request

from app import app
from app.dependecies import db_history
from app.schemas.history import History, HistoryEntry


def parse_history_entries(history_entries: List[Dict]):
    history_entries_array = []
    for entry in history_entries:
        full_url, shortened_url = list(entry.keys())[0], list(entry.values())[0]
        history_entries_array.append(HistoryEntry(full_url=full_url, shortened_url=shortened_url))
    return history_entries_array


@app.get('/user/history', response_model=History)
async def get_user_history(request: Request):
    history_entries = db_history.get(request.cookies.get('user-id', '-'))

    if not history_entries:
        return History(
            status='ok',
            message='empty',
            history_entries=[],
        )

    return History(
        status='ok',
        message='found',
        history_entries=parse_history_entries(history_entries['value'])
    )
