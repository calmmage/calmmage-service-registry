from __future__ import annotations as _annotations

from fastapi import APIRouter
from fastui import AnyComponent, FastUI
from fastui import components as c
from fastui.events import GoToEvent

from calmmage_services_registry.service_registry import ServiceRegistry, ServiceStatus

router = APIRouter()


def sidebar_menu(*components: AnyComponent, title: str | None = None) -> list[AnyComponent]:
    return [
        c.PageTitle(text=f"Calmmage Services Registry — {title}" if title else "Calmmage Services Registry"),
        c.Navbar(
            title="Services Dashboard",
            title_event=GoToEvent(url="/"),
            start_links=[
                c.Link(
                    components=[c.Text(text="Services Status")],
                    on_click=GoToEvent(url="/"),
                    active="exact:/",
                ),
                # Add more links here as needed
            ],
        ),
        c.Page(
            components=[
                *((c.Heading(text=title),) if title else ()),
                *components,
            ],
        ),
        c.Footer(
            extra_text="Calmmage Services Registry",
            links=[
                c.Link(
                    components=[c.Text(text="Github")],
                    on_click=GoToEvent(url="https://github.com/calmmage/calmmage-services-registry"),
                ),
            ],
        ),
    ]


@router.get("/", response_model=FastUI, response_model_exclude_none=True)
async def services_dashboard() -> list[AnyComponent]:
    registry = ServiceRegistry()
    services = registry.services.find()

    status_styles = {
        ServiceStatus.ALIVE: "primary",
        ServiceStatus.SILENT: "warning",
        ServiceStatus.DOWN: "secondary",
        ServiceStatus.DEAD: "secondary",
    }

    service_components = []
    for service in sorted(services, key=lambda s: s["status"]):
        status = ServiceStatus(service["status"])
        named_style = status_styles[status]
        service_components.append(
            c.Button(
                text=f"{service['name']}: {status.value}",
                named_style=named_style,
            ),
        )

    return sidebar_menu(
        c.Heading(text="Services Status"),
        c.Div(components=service_components, class_name="d-flex flex-wrap"),
        title="Services Dashboard",
    )


@router.get("/{path:path}", status_code=404)
async def api_404():
    return {"message": "Not Found"}
