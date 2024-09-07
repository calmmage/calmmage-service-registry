import asyncio
from datetime import datetime, timedelta

from pydantic import BaseModel
from pymongo import MongoClient
from telegram import Bot


class Service(BaseModel):
    name: str
    last_heartbeat: datetime = None
    status: str = "unknown"

class ServiceRegistry:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["service_registry"]
        self.services = self.db["services"]
        self.telegram_bot = Bot("YOUR_TELEGRAM_BOT_TOKEN")
        self.chat_id = "YOUR_TELEGRAM_CHAT_ID"

    async def add_service(self, service: Service):
        self.services.update_one({"name": service.name}, {"$set": service.dict()}, upsert=True)

    async def get_service(self, name: str):
        service_data = self.services.find_one({"name": name})
        return Service(**service_data) if service_data else None

    async def update_service(self, service: Service):
        self.services.update_one({"name": service.name}, {"$set": service.dict()})

    async def delete_service(self, name: str):
        self.services.delete_one({"name": name})

    async def handle_heartbeat(self, name: str):
        service = await self.get_service(name)
        if not service:
            service = Service(name=name)
        service.last_heartbeat = datetime.utcnow()
        service.status = "active"
        await self.update_service(service)

    async def check_inactive_services(self):
        while True:
            all_services = self.services.find()
            for service_data in all_services:
                service = Service(**service_data)
                if service.last_heartbeat and datetime.utcnow() - service.last_heartbeat > timedelta(minutes=5):
                    service.status = "inactive"
                    await self.update_service(service)
                    await self.send_telegram_notification(f"Service {service.name} is inactive!")
            await asyncio.sleep(60)  # Check every minute

    async def send_telegram_notification(self, message: str):
        await self.telegram_bot.send_message(chat_id=self.chat_id, text=message)

    async def send_daily_summary(self):
        while True:
            all_services = self.services.find()
            summary = "Daily Service Summary:\n"
            for service_data in all_services:
                service = Service(**service_data)
                summary += f"{service.name}: {service.status}\n"
            await self.send_telegram_notification(summary)
            await asyncio.sleep(86400)  # Wait for 24 hours
