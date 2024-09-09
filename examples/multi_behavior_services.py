import asyncio
import os
import random
from enum import Enum

from dotenv import load_dotenv
from loguru import logger
from pydantic_settings import BaseSettings

from calmmage_services_registry.heartbeat import asend_heartbeat, is_heartbeat_env_initialized

load_dotenv()

DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"


class Settings(BaseSettings):
    host: str = "localhost"
    port: int = 8002
    https: bool = False

    class Config:
        env_prefix = "heartbeat_"
        env_file = ".env"
        extra = "ignore"


class ServiceBehavior(Enum):
    ALWAYS_ALIVE = 1
    PING_ONCE_THEN_DIE = 2
    PING_GO_SILENT_REVIVE = 3


class DummyService:
    def __init__(self, name, behavior):
        self.name = name
        self.behavior = behavior
        self.is_alive = True
        self.ping_count = 0
        if not is_heartbeat_env_initialized():
            # logger.warning(f"Heartbeat environment is not initialized for {self.name}. Skipping heartbeat.")
            raise ValueError(f"Heartbeat environment is not initialized for {self.name}")

    async def send_heartbeat(self):
        if not self.is_alive:
            return

        await asend_heartbeat(service_name=self.name)

        self.ping_count += 1

    async def run(self):
        while True:
            if self.behavior == ServiceBehavior.ALWAYS_ALIVE:
                await self.send_heartbeat()
                await asyncio.sleep(random.randint(5, 15) if DEBUG_MODE else random.randint(30, 90))

            elif self.behavior == ServiceBehavior.PING_ONCE_THEN_DIE:
                if self.ping_count == 0:
                    await self.send_heartbeat()
                self.is_alive = False
                break
            elif self.behavior == ServiceBehavior.PING_GO_SILENT_REVIVE:
                if self.ping_count < 3:
                    await self.send_heartbeat()
                    await asyncio.sleep(random.randint(5, 15) if DEBUG_MODE else random.randint(30, 90))
                elif self.ping_count < 10:
                    await asyncio.sleep(10 if DEBUG_MODE else 60)  # Silent period
                else:
                    self.ping_count = 0  # Reset and revive
            else:
                raise ValueError(f"Unknown behavior: {self.behavior}")


async def main():
    settings = Settings()
    if settings.https:
        registry_url = f"https://{settings.host}"
        if settings.port and settings.port != 443:
            registry_url += f":{settings.port}"
    else:
        registry_url = f"http://{settings.host}"
        if settings.port:
            registry_url += f":{settings.port}"
    logger.info("Launching with Registry URL: {}", registry_url)

    services = [
        DummyService("always_alive", ServiceBehavior.ALWAYS_ALIVE),
        DummyService("ping_once_die", ServiceBehavior.PING_ONCE_THEN_DIE),
        DummyService("ping_silent_revive", ServiceBehavior.PING_GO_SILENT_REVIVE),
    ]

    tasks = [asyncio.create_task(service.run()) for service in services]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
