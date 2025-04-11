from app.core.schemas import Customer, CustomerCreate, CustomersList, CustomerUpdate
from app.core.service.customers import CustomersService
from app.core.clients import OrdersClient
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("", status_code=200, response_model=CustomersList)
async def get_all_customers() -> CustomersList:
    return await CustomersService.get_all_customers()


@router.get("/{customer_id}", status_code=200, response_model=Customer)
async def get_customer(customer_id: str) -> Customer:
    return await CustomersService.get_customer(customer_id=customer_id)


@router.post("", status_code=201, response_model=Customer)
async def create_customer(customer: CustomerCreate) -> Customer:
    return await CustomersService.create_customer(customer=customer)


@router.put("/{customer_id}", status_code=200, response_model=Customer)
async def update_customer(customer_id: str, customer: CustomerUpdate) -> Customer:
    return await CustomersService.update_customer(customer_id=customer_id, customer=customer)


@router.delete("/{customer_id}", status_code=204)
async def delete_customer(customer_id: str, orders_client: OrdersClient = Depends(OrdersClient)) -> None:
    return await CustomersService.delete_customer(customer_id=customer_id, orders_client=orders_client)
