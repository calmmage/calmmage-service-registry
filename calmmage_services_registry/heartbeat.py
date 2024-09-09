import threading
import time

import requests
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


def send_heartbeat(settings: HeartbeatSettings):
    protocol = "https" if settings.https else "http"
    url = f"{protocol}://{settings.host}:{settings.port}/heartbeat/{settings.service_name}"

    try:
        response = requests.post(url)
        if response.status_code == 200:
            print(f"Heartbeat sent for {settings.service_name}")
        else:
            print(f"Failed to send heartbeat for {settings.service_name}")
    except requests.RequestException as e:
        print(f"Error sending heartbeat for {settings.service_name}: {e}")


def run_heartbeat(settings: HeartbeatSettings):
    while True:
        send_heartbeat(settings)
        time.sleep(settings.heartbeat_interval)


def start_heartbeat_thread(**kwargs):
    settings = HeartbeatSettings(**kwargs)
    thread = threading.Thread(target=run_heartbeat, args=(settings,), daemon=True)
    thread.start()
    return thread


# async def start_heartbeat(settings: HeartbeatSettings):
#     while True:
#         await send_heartbeat(settings)
#         await asyncio.sleep(settings.heartbeat_interval)


# def run_heartbeat(**kwargs):
#     settings = HeartbeatSettings(**kwargs)
#     asyncio.run(start_heartbeat(settings))
#
#
# def start_heartbeat_thread(**kwargs):
#     thread = threading.Thread(target=run_heartbeat, kwargs=kwargs, daemon=True)
#     thread.start()
#     return thread
