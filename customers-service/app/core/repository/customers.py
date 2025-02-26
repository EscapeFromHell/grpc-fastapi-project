from uuid import uuid4

from app.core.repository.repository import RepositoryDynamoDB
from app.core.schemas import Customer, CustomerCreate, CustomersList, CustomerUpdate


class CustomersRepository(RepositoryDynamoDB):
    def get_all_customers(self) -> CustomersList:
        response = self.ddb.customers_table.scan()
        customers = response.get("Items", [])
        return CustomersList(customers=customers)

    def get_customer(self, customer_id: str) -> Customer | None:
        response = self.ddb.customers_table.get_item(Key={"id": customer_id})
        if "Item" not in response:
            return None
        customer = response["Item"]
        return Customer(**customer)

    def create_customer(self, customer: CustomerCreate) -> Customer:
        customer_data = customer.dict()
        customer_data["id"] = str(uuid4())
        self.ddb.customers_table.put_item(Item=customer_data)
        return Customer(**customer_data)


customers_repo = CustomersRepository()
