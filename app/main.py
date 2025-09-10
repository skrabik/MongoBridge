from fastapi import FastAPI, Depends, HTTPException
from app.routers.users import router as users_router
from app.settings import getSettings
from fastapi.security import APIKeyHeader


api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def apiKeyDep(api_key: str | None = Depends(api_key_header)) -> None:
    settings = getSettings()
    if settings.api_key is None:
        return
    if api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")


def createApp() -> FastAPI:
    settings = getSettings()
    application = FastAPI(title="REST FastAPI MongoDB Service")
    application.include_router(
        users_router,
        prefix="/api/v1",
        tags=["users"],
        dependencies=[Depends(apiKeyDep)],
    )
    return application


app = createApp()


