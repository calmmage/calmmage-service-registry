from fastapi import FastAPI
from fastui import FastUI, AnyComponent, components as c
from fastui.components.display import DisplayLookup
from fastui.events import GoToEvent
from pydantic import BaseModel

from calmmage_services_registry.service_registry import ServiceRegistry, ServiceStatus

app = FastAPI()
registry = ServiceRegistry()


class ServiceStatusDisplay(BaseModel):
    name: str
    status: str
    last_heartbeat: str
    duration: str


@app.get("/api/", response_model=FastUI, response_model_exclude_none=True)
async def dashboard() -> list[AnyComponent]:
    services = await registry.get_all_services()
    service_displays = []
    for service in services:
        status_color = {
            ServiceStatus.ALIVE: "green",
            ServiceStatus.SILENT: "yellow",
            ServiceStatus.DOWN: "red",
            ServiceStatus.DEAD: "gray",
        }.get(service.status, "black")

        duration = ""
        if service.status == ServiceStatus.DOWN and service.down_since:
            duration = f"Down for {humanize.naturaltime(datetime.now() - service.down_since)}"
        elif service.status == ServiceStatus.SILENT and service.silent_since:
            duration = f"Silent for {humanize.naturaltime(datetime.now() - service.silent_since)}"

        service_displays.append(
            ServiceStatusDisplay(
                name=service.name,
                status=service.status.value.capitalize(),
                last_heartbeat=str(service.last_heartbeat) if service.last_heartbeat else "N/A",
                duration=duration,
            )
        )

    service_displays.sort(key=lambda s: (s.status != "Alive", s.name))

    return [
        c.Page(
            components=[
                c.Heading(text="Service Status Dashboard", level=1),
                c.Table[ServiceStatusDisplay](
                    data=service_displays,
                    columns=[
                        DisplayLookup(field="name", header="Service Name"),
                        DisplayLookup(field="status", header="Status"),
                        DisplayLookup(field="last_heartbeat", header="Last Heartbeat"),
                        DisplayLookup(field="duration", header="Duration"),
                    ],
                    row_style=lambda row: {"background": status_color},
                ),
                c.Button(text="Refresh", on_click=GoToEvent(url="/")),
            ]
        )
    ]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8005)
