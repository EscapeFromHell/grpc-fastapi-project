import logging

import boto3
from app.config import settings
from app.utils import get_logger

logger = get_logger(__file__, log_level=logging.INFO)
boto3.set_stream_logger(name="boto3", level=logging.DEBUG)


class DynamoDB:
    def __init__(self):
        self.ddb = boto3.resource(
            settings.DB,
            endpoint_url=settings.ENDPOINT_URL,
            region_name=settings.REGION_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        self.customers_table = self.ddb.Table("customers")

    def create_table(self):
        existing_tables = self.ddb.meta.client.list_tables()["TableNames"]
        if "customers" not in existing_tables:
            table = self.ddb.create_table(
                TableName="customers",
                KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
                AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
                ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
            )
            table.wait_until_exists()
            logger.info(f"Table 'customers' created")
        else:
            logger.info("Table 'customers' already exists")


dynamo_db = DynamoDB()
