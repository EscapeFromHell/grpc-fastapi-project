from src.core.models import Order
from src.core.repository.repository import SqlAlchemyRepository


class OrdersRepository(SqlAlchemyRepository):
    model = Order
