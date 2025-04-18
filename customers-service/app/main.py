import uvicorn
from app.api.api_v1 import api_router
from app.config import settings
from app.core.db import dynamo_db
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

root_router = APIRouter()


def get_application() -> FastAPI:
    app = FastAPI(title="Customer Service FastAPI")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router, prefix=settings.API_V1_STR)
    app.include_router(root_router)
    return app


dynamo_db.create_table()
app = get_application()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=False, log_level="info")
