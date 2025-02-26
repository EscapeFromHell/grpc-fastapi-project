from app.core.schemas import Customer, CustomerCreate, CustomersList, CustomerUpdate
from app.core.service.customers import CustomersService
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/get_all_customers", status_code=200, response_model=CustomersList)
async def get_all_customers() -> CustomersList:
    return await CustomersService.get_all_customers()


@router.get("/get_customer", status_code=200, response_model=Customer)
async def get_customer(customer_id: str) -> Customer:
    return await CustomersService.get_customer(customer_id=customer_id)


@router.post("/create_customer", status_code=201, response_model=Customer)
async def create_customer(customer: CustomerCreate) -> Customer:
    return await CustomersService.create_customer(customer=customer)
