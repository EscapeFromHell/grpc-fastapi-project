import logging
from uuid import uuid4

from app.core.repository.repository import RepositoryDynamoDB
from app.core.schemas import Customer, CustomerCreate, CustomersList, CustomerUpdate
from app.utils import get_logger
from botocore.exceptions import ClientError

logger = get_logger(log_level=logging.INFO)


class CustomersRepository(RepositoryDynamoDB):
    def get_all_customers(self) -> CustomersList:
        response = self.ddb.customers_table.scan()
        customers = response.get("Items", [])
        return CustomersList(customers=customers)

    def get_customer(self, customer_id: str) -> Customer | None:
        response = self.ddb.customers_table.get_item(Key={"id": customer_id})
        if "Item" not in response:
            return None
        customer = response.get("Item")
        return Customer(**customer)

    def create_customer(self, customer: CustomerCreate) -> Customer:
        customer_data = customer.model_dump()
        customer_data["id"] = str(uuid4())
        self.ddb.customers_table.put_item(Item=customer_data)
        return Customer(**customer_data)

    def update_customer(self, customer_id: str, customer: CustomerUpdate) -> Customer | None:
        try:
            updated_customer = self.ddb.customers_table.update_item(
                Key={"id": customer_id},
                ConditionExpression="attribute_exists(id)",
                UpdateExpression="SET #name = :name, #surname = :surname",
                ExpressionAttributeNames={"#name": "name", "#surname": "surname"},
                ExpressionAttributeValues={":name": customer.name, ":surname": customer.surname},
                ReturnValues="ALL_NEW",
            )

        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                logger.error(f"Error: Customer with ID {customer_id} not found")
                return None
            else:
                logger.error(f"Error: {e.response['Error']['Message']}")

        else:
            return Customer(**updated_customer.get("Attributes"))

    def delete_customer(self, customer_id: str) -> None:
        self.ddb.customers_table.delete_item(Key={"id": customer_id})
        logger.info(f"Customer with ID: {customer_id} deleted successfully")
