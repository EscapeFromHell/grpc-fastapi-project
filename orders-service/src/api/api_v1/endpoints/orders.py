from fastapi import APIRouter, Depends
from pydantic import PositiveInt
from src.core.clients import CustomersClient
from src.core.schemas import Order, OrderCreate, OrdersList, OrderUpdate
from src.core.service.orders import OrdersService

router = APIRouter()


@router.get("", status_code=200, response_model=OrdersList)
async def get_all_orders(order_service: OrdersService = Depends(OrdersService)) -> OrdersList:
    return await order_service.get_all_orders()


@router.get("/{order_id}", status_code=200, response_model=Order)
async def get_order_by_id(order_id: PositiveInt, order_service: OrdersService = Depends(OrdersService)) -> Order:
    return await order_service.get_order_by_id(order_id=order_id)


@router.get("/by_customer/{customer_id}", status_code=200, response_model=OrdersList)
async def get_orders_by_customer_id(
    customer_id: str, order_service: OrdersService = Depends(OrdersService)
) -> OrdersList:
    return await order_service.get_orders_by_customer_id(customer_id=customer_id)


@router.post("", status_code=201, response_model=Order)
async def create_order(
    order: OrderCreate,
    order_service: OrdersService = Depends(OrdersService),
    customers_client: CustomersClient = Depends(CustomersClient),
) -> Order:
    return await order_service.create_order(order=order, customers_client=customers_client)


@router.put("/{order_id}", status_code=201, response_model=Order)
async def update_order(
    order_id: PositiveInt,
    order: OrderUpdate,
    order_service: OrdersService = Depends(OrdersService),
    customers_client: CustomersClient = Depends(CustomersClient),
) -> Order:
    return await order_service.update_order(order_id=order_id, order=order, customers_client=customers_client)


@router.delete("/{order_id}", status_code=204)
async def delete_order(order_id: PositiveInt, order_service: OrdersService = Depends(OrdersService)) -> None:
    return await order_service.delete_order(order_id=order_id)


@router.delete("/by_customer/{customer_id}", status_code=204)
async def delete_orders_by_customer_id(customer_id: str, order_service: OrdersService = Depends(OrdersService)) -> None:
    return await order_service.delete_orders_by_customer_id(customer_id=customer_id)
