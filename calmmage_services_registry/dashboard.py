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


# Remove lines: all
# Remove lines: all
@router.get("/", response_model=FastUI, response_model_exclude_none=True)
async def services_dashboard() -> list[AnyComponent]:
    registry = ServiceRegistry()
    services = registry.services.find()

    status_classes = {
        ServiceStatus.ALIVE: "text-green-500",
        ServiceStatus.SILENT: "text-yellow-500",
        ServiceStatus.DOWN: "text-red-500",
        ServiceStatus.DEAD: "text-gray-500",
    }

    service_components = []
    for service in services:
        status = ServiceStatus(service["status"])
        service_components.append(
            c.Div(
                components=[
                    c.Text(text=f"{service['name']}: "),
                    c.Div(
                        components=[c.Text(text=f"{status.value}")],
                        class_name=status_classes.get(status, "text-black"),
                    ),
                ],
                class_name="mb-2",
            ),
            # c.Div(
            #     components=[
            #         c.Heading(text="Custom", level=2),
            #         c.Markdown(
            #             text="""\
            #             Below is a custom component, in this case it implements [cowsay](https://en.wikipedia.org/wiki/Cowsay),
            #             but you might be able to do something even more useful with it.
            #
            #             The statement spoken by the famous cow is provided by the backend."""
            #         ),
            #         c.Custom(data="This is a custom component", sub_type="cowsay"),
            #     ],
            #     class_name="border-top mt-3 pt-1",
            # ),
        )

    return sidebar_menu(
        c.Heading(text="Services Status"), c.Div(components=service_components), title="Services Dashboard"
    )


@router.get("/{path:path}", status_code=404)
async def api_404():
    return {"message": "Not Found"}
