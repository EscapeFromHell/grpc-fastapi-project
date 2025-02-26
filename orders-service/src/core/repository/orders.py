from typing import Sequence

from pydantic import PositiveInt
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from src.core.models import Order
from src.core.repository.repository import SqlAlchemyRepository
from src.core.schemas import OrderCreate, OrderUpdate


class OrdersRepository(SqlAlchemyRepository):
    model = Order

    async def get_orders(self) -> Sequence[Order]:
        query = await self.session.execute(select(Order))
        return query.scalars().all()

    async def get_order_by_id(self, order_id: PositiveInt) -> Order | None:
        query = await self.session.execute(select(Order).filter_by(order_id=order_id))
        try:
            order = query.scalars().one()
            return order
        except NoResultFound:
            return None

    async def create_order(self, order: OrderCreate) -> Order:
        order_model = Order(
            customer_id=order.customer_id,
            amount=order.amount,
        )
        async with self.session.begin():
            self.session.add(order_model)
        return order_model

    async def update_order(self, order_id: PositiveInt, order: OrderUpdate) -> Order | None:
        async with self.session.begin():
            query = await self.session.execute(select(Order).filter_by(order_id=order_id))
            try:
                db_order = query.scalars().one()
                for field, value in order.dict(exclude_unset=True).items():
                    setattr(db_order, field, value)
            except NoResultFound:
                return None
        return db_order

    async def delete_order(self, order_id: PositiveInt) -> None:
        async with self.session.begin():
            query = await self.session.execute(select(Order).filter_by(order_id=order_id))
            db_order = query.scalars().one()
            await self.session.delete(db_order)
