from typing import List
from functools import partial
from fastapi import FastAPI

from domain import usecase
from .event_handler import startup, shutdown
from .schema import OrderDetail


def create_app():
    fast_app = FastAPI(title='Inventory Service')
    fast_app.add_event_handler('startup', func=partial(startup, app=fast_app))
    fast_app.add_event_handler('shutdown', func=partial(shutdown, app=fast_app))
    return fast_app


app = create_app()


@app.get('/pending-orders', response_model=List[OrderDetail])
async def get_pending_order():
    orders = await usecase.get_pending_orders()
    return [OrderDetail.from_order(order) for order in orders]
