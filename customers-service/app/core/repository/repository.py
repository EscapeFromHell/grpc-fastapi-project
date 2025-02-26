from app.core.db import dynamo_db


class RepositoryDynamoDB:
    def __init__(self):
        self.ddb = dynamo_db
