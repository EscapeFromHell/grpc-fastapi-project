import logging

import httpx
from fastapi import HTTPException

from app.config import settings
from app.utils import get_logger

logger = get_logger(__file__, logging.DEBUG)


class OrdersClient:
    async def delete_orders(self, customer_id: str) -> str:
        try:
            async with httpx.AsyncClient() as client:
                url = f"{settings.URL}{settings.API_V1_STR}/orders/by_customer/{customer_id}"
                response = await client.delete(
                    url=url,
                    params={"customer_id": customer_id, "format": "json"},
                    headers={"Content-Type": "application/json"},
                    timeout=10,
                )

        except (httpx.ConnectError, httpx.ConnectTimeout) as error:
            logger.error(f"Failed to connect to the server at {settings.URL}. Error: {error}")
            raise HTTPException(status_code=400, detail=f"Unable to delete orders. Connection error: {error}")

        else:
            if response.is_error:
                logger.error(
                    f"Received error response from server: {response.status_code}. Content: {response.content.decode()}"
                )
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Failed to delete orders. Server returned status {response.status_code}",
                )
            return f"Orders of customer with ID: {customer_id} deleted successfully"
