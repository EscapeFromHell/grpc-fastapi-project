import logging

from fastapi import HTTPException
from pydantic import PositiveInt
from src.core.clients import CustomersClient
from src.core.schemas import Order as OrderSchema
from src.core.schemas import OrderCreate, OrdersList, OrderUpdate
from src.core.service.service import BaseService
from src.utils import get_logger

logger = get_logger(__file__, log_level=logging.INFO)


class OrdersService(BaseService):
    base_repository: str = "orders"

    async def get_all_orders(self) -> OrdersList:
        result = await self.get_by_query_all()
        orders = [order.to_pydantic_schema() for order in result]
        orders_list = OrdersList(orders=orders)
        return orders_list

    async def get_orders_by_customer_id(self, customer_id: str) -> OrdersList:
        result = await self.get_by_query_all(customer_id=customer_id)
        if not result:
            raise HTTPException(status_code=404, detail=f"Orders with customer_id {customer_id} not found!")
        orders = [order.to_pydantic_schema() for order in result]
        orders_list = OrdersList(orders=orders)
        return orders_list

    async def get_order_by_id(self, order_id: PositiveInt) -> OrderSchema:
        result = await self.get_by_query_one_or_none(id=order_id)
        if not result:
            raise HTTPException(status_code=404, detail=f"Order with order_id {order_id} not found!")
        order = result.to_pydantic_schema()
        return order

    async def create_order(self, order: OrderCreate, customers_client: CustomersClient) -> OrderSchema:
        if not customers_client.check_customer_exists(customer_id=order.customer_id):
            raise HTTPException(status_code=404, detail=f"Customer with ID {order.customer_id} does not exist!")
        result = await self.add_one_and_get_obj(**order.model_dump())
        created_order = result.to_pydantic_schema()
        return created_order

    async def update_order(
        self, order_id: PositiveInt, order: OrderUpdate, customers_client: CustomersClient
    ) -> OrderSchema:
        if not customers_client.check_customer_exists(customer_id=order.customer_id):
            raise HTTPException(status_code=404, detail=f"Customer with ID {order.customer_id} does not exist!")
        result = await self.update_one_by_id(obj_id=order_id, **order.model_dump())
        if not result:
            raise HTTPException(status_code=404, detail=f"Order with order_id {order_id} not found!")
        updated_event = result.to_pydantic_schema()
        return updated_event

    async def delete_order(self, order_id: PositiveInt) -> None:
        result = await self.get_by_query_one_or_none(id=order_id)
        if not result:
            raise HTTPException(status_code=404, detail=f"Order with order_id {order_id} not found!")
        await self.delete_by_query(id=order_id)
        logger.info(f"Order with order_id {order_id} deleted!")

    async def delete_orders_by_customer_id(self, customer_id: PositiveInt) -> None:
        result = await self.get_by_query_all(customer_id=customer_id)
        if not result:
            raise HTTPException(status_code=404, detail=f"Orders with customer_id {customer_id} not found!")
        await self.delete_by_query(customer_id=customer_id)
        logger.info(f"{len(result)} orders with customer_id {customer_id} deleted!")
