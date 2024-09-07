# Project: calmmage-services-registry
# Path: calmmage_services_registry/dummy_service.py
# Start: 0
# Remove lines: all
import asyncio
import aiohttp
import random

class DummyService:
    def __init__(self, name, registry_url):
        self.name = name
        self.registry_url = registry_url

    async def send_heartbeat(self):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(f"{self.registry_url}/heartbeat/{self.name}") as response:
                    if response.status == 200:
                        print(f"Heartbeat sent for {self.name}")
                    else:
                        print(f"Failed to send heartbeat for {self.name}")
            except aiohttp.ClientError as e:
                print(f"Error sending heartbeat for {self.name}: {e}")

    async def run(self):
        while True:
            await self.send_heartbeat()
            await asyncio.sleep(random.randint(30, 90))  # Random interval between 30 and 90 seconds

async def main():
    services = [
        DummyService("service1", "http://localhost:8000"),
        DummyService("service2", "http://localhost:8000"),
        DummyService("service3", "http://localhost:8000"),
    ]

    tasks = [asyncio.create_task(service.run()) for service in services]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
