from typing import List

from pydantic import BaseModel


class CustomerBase(BaseModel):
    name: str
    surname: str


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerBase):
    pass


class CustomerInDB(CustomerBase):
    id: str

    class Config:
        from_attributes = True


class Customer(CustomerInDB):
    pass


class CustomersList(BaseModel):
    customers: List[Customer]
