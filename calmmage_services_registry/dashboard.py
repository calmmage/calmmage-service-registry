from datetime import datetime

import humanize
from fastapi import FastAPI
from fastui import AnyComponent, FastUI
from fastui import components as c
from pydantic import BaseModel

from calmmage_services_registry.service_registry import ServiceRegistry, ServiceStatus

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
registry = ServiceRegistry()


@app.get("/")
async def read_root():
    return FileResponse("static/index.html")


registry = ServiceRegistry()


class ServiceStatusDisplay(BaseModel):
    name: str
    status: str
    last_heartbeat: str
    duration: str


def dashboard_page(content: AnyComponent) -> list[AnyComponent]:
    return [
        c.PageTitle(text="Service Status Dashboard"),
        c.Navbar(
            title="Service Registry",
            links=[
                c.Link(components=[c.Text(text="Dashboard")], on_click=c.GoToEvent(url="/")),
            ],
        ),
        c.Page(
            components=[
                c.Heading(text="Service Status Dashboard", level=1),
                content,
            ]
        ),
        c.Footer(
            text="© 2024 Service Registry",
        ),
    ]


@app.get("/api/", response_model=FastUI, response_model_exclude_none=True)
async def api_index() -> list[AnyComponent]:
    services = await registry.get_all_services()
    service_displays = []
    for service in services:
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

    table = c.Table[ServiceStatusDisplay](
        data=service_displays,
        columns=[
            c.Column(header="Service Name", accessor="name"),
            c.Column(header="Status", accessor="status"),
            c.Column(header="Last Heartbeat", accessor="last_heartbeat"),
            c.Column(header="Duration", accessor="duration"),
        ],
        row_style=lambda row: {
            "background": {
                "Alive": "lightgreen",
                "Silent": "yellow",
                "Down": "lightcoral",
                "Dead": "lightgray",
            }.get(row.status, "white")
        },
    )

    return dashboard_page(
        c.Div(
            components=[
                table,
                c.Button(text="Refresh", on_click=c.GoToEvent(url="/")),
            ]
        )
    )


@app.get("/{path:path}", status_code=404)
async def api_404():
    return {"message": "Not Found"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8005)
