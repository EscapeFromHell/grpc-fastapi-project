from app.core.repository import CustomersRepository
from app.core.schemas import Customer, CustomerCreate, CustomersList, CustomerUpdate
from app.core.service.service import BaseService
from app.core.clients import OrdersClient
from fastapi import HTTPException
from app.utils import get_logger
import logging

logger = get_logger(__file__, log_level=logging.INFO)



class CustomersService(BaseService):
    base_repository = CustomersRepository()

    @classmethod
    async def get_all_customers(cls) -> CustomersList:
        customers = cls.base_repository.get_all_customers()
        return customers

    @classmethod
    async def get_customer(cls, customer_id: str) -> Customer:
        customer = cls.base_repository.get_customer(customer_id=customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail=f"Customer with ID: {customer_id} not found")
        return customer

    @classmethod
    async def create_customer(cls, customer: CustomerCreate) -> Customer:
        customer_data = cls.base_repository.create_customer(customer=customer)
        return customer_data

    @classmethod
    async def update_customer(cls, customer_id: str, customer: CustomerUpdate) -> Customer:
        updated_customer = cls.base_repository.update_customer(customer_id=customer_id, customer=customer)
        if not updated_customer:
            raise HTTPException(status_code=404, detail=f"Customer with ID: {customer_id} not found")
        return updated_customer

    @classmethod
    async def delete_customer(cls, customer_id: str, orders_client: OrdersClient) -> None:
        response_message = await orders_client.delete_orders(customer_id=customer_id)
        logger.info(response_message)
        return cls.base_repository.delete_customer(customer_id=customer_id)
