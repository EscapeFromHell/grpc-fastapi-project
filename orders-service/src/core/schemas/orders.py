from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, PositiveInt, condecimal


class OrderBase(BaseModel):
    customer_id: str
    amount: condecimal(gt=0, decimal_places=2) = Field(
        description="Amount must be a positive number with two decimal places"
    )


class OrderCreate(OrderBase):
    pass


class OrderUpdate(OrderBase):
    pass


class OrderInDB(OrderBase):
    id: PositiveInt
    created_at: datetime

    class Config:
        from_attributes = True


class Order(OrderInDB):
    pass


class OrdersList(BaseModel):
    orders: List[Order]
