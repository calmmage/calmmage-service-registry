from calmmage_services_registry.fastapi_app import main

if __name__ == "__main__":
    import uvicorn
    app = main()
    uvicorn.run(app, host="0.0.0.0", port=8000)