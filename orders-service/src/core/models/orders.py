from datetime import datetime
from decimal import Decimal

import sqlalchemy.orm as so
from sqlalchemy import func
from src.core.models import Base
from src.core.schemas import Order as OrderSchema


class Order(Base):
    __tablename__ = "orders"
    id: so.Mapped[int] = so.mapped_column(primary_key=True, index=True)
    customer_id: so.Mapped[str] = so.mapped_column(nullable=False)
    amount: so.Mapped[Decimal] = so.mapped_column(nullable=False)
    created_at: so.Mapped[datetime] = so.mapped_column(server_default=func.now(), nullable=False)

    def to_pydantic_schema(self) -> OrderSchema:
        return OrderSchema(
            id=self.id,
            customer_id=self.customer_id,
            amount=self.amount.quantize(Decimal("1.00")),
            created_at=self.created_at,
        )
