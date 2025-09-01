from fastapi import FastAPI
from app.routers.records import router as records_router
from app.settings import getSettings


def createApp() -> FastAPI:
    settings = getSettings()
    application = FastAPI(title="REST FastAPI MongoDB Service")
    application.include_router(records_router, prefix="/api/v1", tags=["records"])
    return application


app = createApp()


