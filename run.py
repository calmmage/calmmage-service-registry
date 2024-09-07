from calmmage_services_registry.fastapi_app import main, fastapi_settings

if __name__ == "__main__":
    import uvicorn

    app = main()
    uvicorn.run(app, host=fastapi_settings.api_host, port=fastapi_settings.api_port)
