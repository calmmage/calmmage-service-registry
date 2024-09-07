import asyncio
from datetime import datetime, timedelta
from enum import Enum

import pytz
from pydantic import BaseModel
from pymongo import MongoClient
from telegram import Bot

from calmmage_services_registry.settings import Settings


class ServiceStatus(str, Enum):
    UNKNOWN = "unknown"
    ALIVE = "alive"
    SILENT = "silent"
    DOWN = "down"
    DEAD = "dead"


class Service(BaseModel):
    name: str
    last_heartbeat: datetime = None
    status: ServiceStatus = ServiceStatus.UNKNOWN
    silent_since: datetime = None
    down_since: datetime = None


class ServiceRegistry:
    def __init__(self):
        self.settings = Settings()
        self.client = MongoClient(self.settings.mongodb_url)
        self.db = self.client[self.settings.database_name]
        self.services = self.db["services"]
        self.telegram_bot = Bot(self.settings.telegram_bot_token)
        self.chat_id = self.settings.telegram_chat_id

    async def add_service(self, service: Service):
        self.services.update_one({"name": service.name}, {"$set": service.model_dump()}, upsert=True)

    async def get_service(self, name: str):
        service_data = self.services.find_one({"name": name})
        return Service(**service_data) if service_data else None

    async def update_service(self, service: Service):
        self.services.update_one({"name": service.name}, {"$set": service.model_dump()}, upsert=True)

    async def delete_service(self, name: str):
        self.services.delete_one({"name": name})

    async def handle_heartbeat(self, name: str):
        service = await self.get_service(name)
        if not service:
            service = Service(name=name)

        service.last_heartbeat = datetime.now()

        if service.status != ServiceStatus.ALIVE:
            await self.send_telegram_notification(f"Service {service.name} is now ALIVE!")

        service.status = ServiceStatus.ALIVE
        service.silent_since = None
        service.down_since = None

        await self.update_service(service)

    async def check_inactive_services(self):
        while True:
            all_services = self.services.find()
            for service_data in all_services:
                service = Service(**service_data)
                if service.status == ServiceStatus.DEAD:
                    continue

                time_since_last_heartbeat = datetime.now() - service.last_heartbeat

                if self.settings.debug_mode:
                    inactive_threshold = timedelta(seconds=self.settings.debug_inactive_threshold_seconds)
                    silent_to_down_threshold = timedelta(seconds=self.settings.debug_silent_to_down_seconds)
                    down_to_dead_threshold = timedelta(seconds=self.settings.debug_down_to_dead_seconds)
                else:
                    inactive_threshold = timedelta(minutes=self.settings.service_inactive_threshold_minutes)
                    silent_to_down_threshold = timedelta(hours=1)
                    down_to_dead_threshold = timedelta(days=7)

                if time_since_last_heartbeat > inactive_threshold:
                    if service.status == ServiceStatus.ALIVE:
                        service.status = ServiceStatus.SILENT
                        service.silent_since = datetime.now()
                        await self.send_telegram_notification(f"Service {service.name} has gone SILENT!")
                    elif (
                        service.status == ServiceStatus.SILENT and time_since_last_heartbeat > silent_to_down_threshold
                    ):
                        service.status = ServiceStatus.DOWN
                        service.down_since = datetime.now()
                        await self.send_telegram_notification(f"Service {service.name} is now DOWN!")
                    elif service.status == ServiceStatus.DOWN and time_since_last_heartbeat > down_to_dead_threshold:
                        service.status = ServiceStatus.DEAD
                        await self.send_telegram_notification(f"Service {service.name} is now considered DEAD!")

                await self.update_service(service)

            await asyncio.sleep(self.settings.check_interval_seconds)

    async def send_telegram_notification(self, message: str):
        await self.telegram_bot.send_message(chat_id=self.chat_id, text=message)

    async def send_daily_summary(self):
        tz = pytz.timezone(self.settings.timezone)
        summary_time = datetime.strptime(self.settings.daily_summary_time, "%H:%M").time()

        while True:
            if not self.settings.debug_mode:
                now = datetime.now(tz)
                target_time = datetime.combine(now.date(), summary_time)
                target_time = tz.localize(target_time)

                if now > target_time:
                    target_time += timedelta(days=1)

                await asyncio.sleep((target_time - now).total_seconds())

            all_services = self.services.find()
            summary = "Daily Service Summary:\n"
            for service_data in all_services:
                service = Service(**service_data)
                summary += f"{service.name}: {service.status}\n"
            await self.send_telegram_notification(summary)
            if self.settings.debug_mode:
                await asyncio.sleep(self.settings.debug_summary_interval_seconds)
