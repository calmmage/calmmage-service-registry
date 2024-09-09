import asyncio
import os
import threading
import time

import aiohttp
import requests
from loguru import logger
from pydantic_settings import BaseSettings


class HeartbeatSettings(BaseSettings):
    host: str = "localhost"
    port: int = 8002
    https: bool = False
    service_name: str
    heartbeat_interval: int = 60  # seconds

    class Config:
        env_prefix = "heartbeat_"
        extra = "ignore"


def is_heartbeat_env_initialized() -> bool:
    return os.getenv("HEARTBEAT_HOST") is not None


def send_heartbeat(settings: HeartbeatSettings):
    protocol = "https" if settings.https else "http"
    url = f"{protocol}://{settings.host}:{settings.port}/heartbeat/{settings.service_name}"

    try:
        response = requests.post(url)
        if response.status_code == 200:
            logger.info(f"Heartbeat sent for {settings.service_name}")
        else:
            logger.error(f"Failed to send heartbeat for {settings.service_name}")
    except requests.RequestException as e:
        logger.error(f"Error sending heartbeat for {settings.service_name}: {e}")


async def asend_heartbeat(settings: HeartbeatSettings):
    protocol = "https" if settings.https else "http"
    url = f"{protocol}://{settings.host}:{settings.port}/heartbeat/{settings.service_name}"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url) as response:
                if response.status == 200:
                    logger.info(f"Heartbeat sent for {settings.service_name}")
                else:
                    logger.error(f"Failed to send heartbeat for {settings.service_name}")
        except aiohttp.ClientError as e:
            logger.error(f"Error sending heartbeat for {settings.service_name}: {e}")


def run_heartbeat(**kwargs):
    settings = HeartbeatSettings(**kwargs)
    while True:
        send_heartbeat(settings)
        time.sleep(settings.heartbeat_interval)


async def arun_heartbeat(**kwargs):
    settings = HeartbeatSettings(**kwargs)
    while True:
        await asend_heartbeat(settings)
        await asyncio.sleep(settings.heartbeat_interval)


def start_heartbeat_thread(**kwargs):
    thread = threading.Thread(target=run_heartbeat, kwargs=kwargs, daemon=True)
    thread.start()
    return thread


# async def astart_heartbeat(**kwargs):
#     await asyncio.create_task(arun_heartbeat(**kwargs))
