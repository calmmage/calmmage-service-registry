from calmmage_services_registry.fastapi_app import main
from calmmage_services_registry.settings import settings

if __name__ == "__main__":
    import uvicorn

    app = main()
    uvicorn.run(app, host=settings.api_host, port=settings.api_port)
