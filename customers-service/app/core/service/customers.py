from app.core.repository import customers_repo
from app.core.schemas import Customer, CustomerCreate, CustomersList, CustomerUpdate
from app.core.service.service import BaseService
from fastapi import HTTPException


class CustomersService(BaseService):
    @classmethod
    async def get_all_customers(cls) -> CustomersList:
        customers = customers_repo.get_all_customers()
        return customers

    @classmethod
    async def get_customer(cls, customer_id: str) -> Customer:
        customer = customers_repo.get_customer(customer_id=customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer

    @classmethod
    async def create_customer(cls, customer: CustomerCreate) -> Customer:
        customer_data = customers_repo.create_customer(customer=customer)
        return customer_data
