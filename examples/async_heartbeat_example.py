import asyncio

from dotenv import load_dotenv
from loguru import logger

from calmmage_services_registry.heartbeat import is_heartbeat_env_initialized, arun_heartbeat

load_dotenv()


class AsyncApp:
    async def run(self):
        # await self.setup()
        print("AsyncApp is running...")
        while True:
            # Simulating some work
            await asyncio.sleep(5)
            print("AsyncApp is still running...")


async def main():
    app = AsyncApp()
    if is_heartbeat_env_initialized():
        await asyncio.gather(arun_heartbeat(), app.run())
    else:
        logger.warning("Heartbeat environment is not initialized. Skipping heartbeat.")
        # asyncio.run(app.run())
        await app.run()


if __name__ == "__main__":
    asyncio.run(main())
