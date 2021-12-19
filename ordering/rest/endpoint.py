from fastapi import APIRouter, HTTPException

from domain import usecase
from domain.model.order.exception import OrderSubmittedException, InvalidOrderItemAmountException
from domain.model.order.repository.exception import InvalidOrderIdException, OrderNotFoundException

from .schema import (
    CreateOrder, UpdateOrderItem, CreationSuccess, OrderItemUpdateSuccess,
    OrderDetail, OrderSubmissionSuccess,
)


router = APIRouter()


@router.post('', response_model=CreationSuccess)
async def create_order(order: CreateOrder):
    items = [(t.product_id, t.amount) for t in order.items]
    order_id = await usecase.create_new_order(customer_id=order.customer_id, items=items)
    return CreationSuccess(id=order_id, message='order created')


@router.get('/{orderId}', response_model=OrderDetail)
async def get_order(order_id: str):
    try:
        order = await usecase.get_order(order_id=order_id)
    except (InvalidOrderIdException, OrderNotFoundException):
        raise HTTPException(404, 'Order not found')

    return OrderDetail.from_order(order)


@router.put('/{orderId}/items/{productId}', response_model=OrderItemUpdateSuccess)
async def update_item_amount_to_order(order_id: str, product_id: str, order_item: UpdateOrderItem):
    try:
        result = await usecase.update_order_item_amount(order_id=order_id, product_id=product_id,
                                                        amount=order_item.amount)
    except OrderSubmittedException:
        raise HTTPException(405, 'Submitted Order cannot be updated')
    except InvalidOrderItemAmountException as e:
        raise HTTPException(403, str(e))

    return OrderItemUpdateSuccess(orderId=result.order_id, productId=result.product_id, amount=result.amount,
                                  message='order item updated')


@router.put('/{orderId}/submission', response_model=OrderSubmissionSuccess)
async def submit_order(order_id: str):
    try:
        await usecase.submit_order(order_id=order_id)
    except OrderSubmittedException:
        raise HTTPException(405, 'Submitted Order cannot be updated')

    return OrderSubmissionSuccess(id=order_id, message='order submitted')
