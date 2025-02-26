from fastapi import HTTPException
from pydantic import PositiveInt
from src.clients import CustomersClient
from src.core.schemas import Order as OrderSchema
from src.core.schemas import OrderCreate, OrdersList, OrderUpdate
from src.core.service.service import BaseService
from src.core.uow import UnitOfWork


class OrdersService(BaseService):
    base_repository: str = "orders"

    @classmethod
    async def get_all_orders(cls, uow: UnitOfWork) -> OrdersList:
        async with uow:
            result = await uow.__dict__[cls.base_repository].get_orders()
        orders = [order.to_pydantic_schema() for order in result]
        orders_list = OrdersList(orders=orders)
        return orders_list

    @classmethod
    async def get_order_by_id(cls, order_id: PositiveInt, uow: UnitOfWork) -> OrderSchema:
        async with uow:
            result = await uow.__dict__[cls.base_repository].get_order_by_id(order_id=order_id)
            if not result:
                raise HTTPException(status_code=404, detail=f"Order with order_id {order_id} not found!")
        order = result.to_pydantic_schema()
        return order

    @classmethod
    async def create_order(cls, order: OrderCreate, customers_client: CustomersClient, uow: UnitOfWork) -> OrderSchema:
        if not customers_client.check_customer_exists(customer_id=order.customer_id):
            raise HTTPException(status_code=404, detail=f"Customer with ID {order.customer_id} does not exist!")
        async with uow:
            result = await uow.__dict__[cls.base_repository].create_order(order=order)
        created_order = result.to_pydantic_schema()
        return created_order

    @classmethod
    async def update_order(cls, order_id: PositiveInt, order: OrderUpdate, uow: UnitOfWork) -> OrderSchema:
        async with uow:
            result = await uow.__dict__[cls.base_repository].update_order(order_id=order_id, order=order)
            if not result:
                raise HTTPException(status_code=404, detail=f"Order with order_id {order_id} not found!")
        updated_event = result.to_pydantic_schema()
        return updated_event

    @classmethod
    async def delete_order(cls, order_id: PositiveInt, uow: UnitOfWork) -> None:
        async with uow:
            result = await uow.__dict__[cls.base_repository].get_order_by_id(order_id=order_id)
            if not result:
                raise HTTPException(status_code=404, detail=f"Order with order_id {order_id} not found!")
            await uow.__dict__[cls.base_repository].delete_order(order_id=order_id)
