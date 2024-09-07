from fastapi import FastAPI
import asyncio

from calmmage_services_registry.service_registry import ServiceRegistry, Service


def main():
    app = FastAPI()
    registry = ServiceRegistry()

    @app.on_event("startup")
    async def startup_event():
        asyncio.create_task(registry.check_inactive_services())
        asyncio.create_task(registry.send_daily_summary())

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

    return app

if __name__ == "__main__":
    import uvicorn
    app = main()
    uvicorn.run(app, host="0.0.0.0", port=8002)
