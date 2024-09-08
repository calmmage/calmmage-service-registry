import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastui import prebuilt_html
from httpx import AsyncClient
from pydantic import BaseModel
from pydantic_settings import BaseSettings

from calmmage_services_registry.dashboard import router
from calmmage_services_registry.service_registry import ServiceRegistry, Service


class FastAPISettings(BaseSettings):
    api_host: str = "0.0.0.0"
    api_port: int = 8002

    class Config:
        env_prefix = "fastapi_"
        env_file = ".env"
        extra = "ignore"


fastapi_settings = FastAPISettings()


class ServiceStatusDisplay(BaseModel):
    name: str
    status: str
    last_heartbeat: str
    duration: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tasks for checking inactive services and sending daily summaries
    registry = ServiceRegistry()
    inactive_task = asyncio.create_task(registry.check_inactive_services())
    summary_task = asyncio.create_task(registry.send_daily_summary())

    async with AsyncClient() as client:
        app.state.httpx_client = client
        yield

    # Shutdown: cancel the tasks
    inactive_task.cancel()
    summary_task.cancel()
    try:
        await inactive_task
        await summary_task
    except asyncio.CancelledError:
        pass


def main():
    app = FastAPI(lifespan=lifespan)
    registry = ServiceRegistry()

    @app.post("/heartbeat/{service_name}")
    async def heartbeat(service_name: str):
        await registry.handle_heartbeat(service_name)
        return {"status": "ok"}

    @app.post("/service")
    async def create_service(service: Service):
        await registry.add_service(service)
        return {"status": "ok"}

    @app.get("/service/{service_name}")
    async def get_service(service_name: str):
        service = await registry.get_service(service_name)
        if service:
            return service
        return {"status": "not found"}

    @app.put("/service/{service_name}")
    async def update_service(service_name: str, service: Service):
        if service_name != service.name:
            return {"status": "error", "message": "Service name mismatch"}
        await registry.update_service(service)
        return {"status": "ok"}

    @app.delete("/service/{service_name}")
    async def delete_service(service_name: str):
        await registry.delete_service(service_name)
        return {"status": "ok"}

    app.include_router(router, prefix="/api")

    @app.get("/{path:path}")
    async def html_landing() -> HTMLResponse:
        """
        # this part is essential for the frontend to work!!!
        :return:
        """
        return HTMLResponse(prebuilt_html(title="FastUI Demo"))

    return app


if __name__ == "__main__":
    import uvicorn

    app = main()
    uvicorn.run(app, host=fastapi_settings.api_host, port=fastapi_settings.api_port)
