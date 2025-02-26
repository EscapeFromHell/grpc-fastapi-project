from fastapi import APIRouter, Depends
from pydantic import PositiveInt
from src.clients import CustomersClient
from src.core.schemas import Order, OrderCreate, OrdersList, OrderUpdate
from src.core.service.orders import OrdersService
from src.core.uow import UnitOfWork

router = APIRouter()


@router.get("/get_orders", status_code=200, response_model=OrdersList)
async def get_all_orders(uow: UnitOfWork = Depends(UnitOfWork)) -> OrdersList:
    return await OrdersService.get_all_orders(uow=uow)


@router.get("/get_order_by_id/{order_id}", status_code=200, response_model=Order)
async def get_event_by_id(order_id: PositiveInt, uow: UnitOfWork = Depends(UnitOfWork)) -> Order:
    return await OrdersService.get_order_by_id(uow=uow, order_id=order_id)


@router.post("/create_order", status_code=201, response_model=Order)
async def create_order(
    order: OrderCreate,
    customers_client: CustomersClient = Depends(CustomersClient),
    uow: UnitOfWork = Depends(UnitOfWork),
) -> Order:
    return await OrdersService.create_order(order=order, customers_client=customers_client, uow=uow)


@router.put("/update_order/{order_id}", status_code=201, response_model=Order)
async def update_order(order_id: PositiveInt, order: OrderUpdate, uow: UnitOfWork = Depends(UnitOfWork)) -> Order:
    return await OrdersService.update_order(order_id=order_id, order=order, uow=uow)


@router.delete("/delete_order/{order_id}", status_code=204)
async def delete_order(order_id: PositiveInt, uow: UnitOfWork = Depends(UnitOfWork)) -> None:
    return await OrdersService.delete_order(order_id=order_id, uow=uow)
