from functools import partial
from fastapi import FastAPI

from .event_handler import startup, shutdown

from . import endpoint


def create_app():
    fast_app = FastAPI(title='Ordering Service')
    fast_app.add_event_handler('startup', func=partial(startup, app=fast_app))
    fast_app.add_event_handler('shutdown', func=partial(shutdown, app=fast_app))
    fast_app.include_router(endpoint.router, prefix='/orders', tags=['order'])
    return fast_app


app = create_app()
