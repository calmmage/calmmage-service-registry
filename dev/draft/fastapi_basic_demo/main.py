from __future__ import annotations as _annotations

import sys
from contextlib import asynccontextmanager

from fastapi import APIRouter
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastui import AnyComponent, FastUI
from fastui import components as c
from fastui import prebuilt_html
from fastui.auth import fastapi_auth_exception_handling
from fastui.dev import dev_fastapi_app
from fastui.events import GoToEvent
from httpx import AsyncClient


def sidebar_menu(*components: AnyComponent, title: str | None = None) -> list[AnyComponent]:
    return [
        c.PageTitle(text=f"FastUI Demo — {title}" if title else "FastUI Demo"),
        c.Navbar(
            title="FastUI Demo",
            title_event=GoToEvent(url="/"),
            start_links=[
                c.Link(
                    components=[c.Text(text="Components")],
                    on_click=GoToEvent(url="/components"),
                    active="startswith:/components",
                ),
                c.Link(
                    components=[c.Text(text="Tables")],
                    on_click=GoToEvent(url="/table/cities"),
                    active="startswith:/table",
                ),
                c.Link(
                    components=[c.Text(text="Auth")],
                    on_click=GoToEvent(url="/auth/login/password"),
                    active="startswith:/auth",
                ),
                c.Link(
                    components=[c.Text(text="Forms")],
                    on_click=GoToEvent(url="/forms/login"),
                    active="startswith:/forms",
                ),
            ],
        ),
        c.Page(
            components=[
                *((c.Heading(text=title),) if title else ()),
                *components,
            ],
        ),
        c.Footer(
            extra_text="FastUI Demo",
            links=[
                c.Link(
                    components=[c.Text(text="Github")], on_click=GoToEvent(url="https://github.com/pydantic/FastUI")
                ),
                c.Link(components=[c.Text(text="PyPI")], on_click=GoToEvent(url="https://pypi.org/project/fastui/")),
                c.Link(components=[c.Text(text="NPM")], on_click=GoToEvent(url="https://www.npmjs.com/org/pydantic/")),
            ],
        ),
    ]


router = APIRouter()


@router.get("/", response_model=FastUI, response_model_exclude_none=True)
def api_index() -> list[AnyComponent]:
    # language=markdown
    markdown = """\
This site provides a demo of [FastUI](https://github.com/pydantic/FastUI), the code for the demo
is [here](https://github.com/pydantic/FastUI/tree/main/demo).

You can find the documentation for FastUI [here](https://docs.pydantic.dev/fastui/).

The following components are demonstrated:

* `Markdown` — that's me :-)
* `Text`— example [here](/components#text)
* `Paragraph` — example [here](/components#paragraph)
* `PageTitle` — you'll see the title in the browser tab change when you navigate through the site
* `Heading` — example [here](/components#heading)
* `Code` — example [here](/components#code)
* `Button` — example [here](/components#button-and-modal)
* `Link` — example [here](/components#link-list)
* `LinkList` — example [here](/components#link-list)
* `Navbar` — see the top of this page
* `Footer` — see the bottom of this page
* `Modal` — static example [here](/components#button-and-modal), dynamic content example [here](/components#dynamic-modal)
* `ServerLoad` — see [dynamic modal example](/components#dynamic-modal) and [SSE example](/components#server-load-sse)
* `Image` - example [here](/components#image)
* `Iframe` - example [here](/components#iframe)
* `Video` - example [here](/components#video)
* `Toast` - example [here](/components#toast)
* `Table` — See [cities table](/table/cities) and [users table](/table/users)
* `Pagination` — See the bottom of the [cities table](/table/cities)
* `ModelForm` — See [forms](/forms/login)

Authentication is supported via:
* token based authentication — see [here](/auth/login/password) for an example of password authentication
* GitHub OAuth — see [here](/auth/login/github) for an example of GitHub OAuth login
"""
    return sidebar_menu(c.Markdown(text=markdown))


@router.get("/{path:path}", status_code=404)
async def api_404():
    # so we don't fall through to the index page
    return {"message": "Not Found"}


@asynccontextmanager
async def lifespan(app_: FastAPI):
    async with AsyncClient() as client:
        app_.state.httpx_client = client
        yield


frontend_reload = "--reload" in sys.argv
if frontend_reload:
    # dev_fastapi_app reloads in the browser when the Python source changes
    app = dev_fastapi_app(lifespan=lifespan)
else:
    app = FastAPI(lifespan=lifespan)

fastapi_auth_exception_handling(app)
# app.include_router(components_router, prefix='/api/components')
# app.include_router(sse_router, prefix='/api/components')
# app.include_router(table_router, prefix='/api/table')
# app.include_router(forms_router, prefix='/api/forms')
# app.include_router(auth_router, prefix='/api/auth')
app.include_router(router, prefix="/api")


# @app.get("/robots.txt", response_class=PlainTextResponse)
# async def robots_txt() -> str:
#     return "User-agent: *\nAllow: /"
#
#
# @app.get("/favicon.ico", status_code=404, response_class=PlainTextResponse)
# async def favicon_ico() -> str:
#     return "page not found"
#
#


@app.get("/{path:path}")
async def html_landing() -> HTMLResponse:
    """
    # this part is essential for the frontend to work!!!
    :return:
    """
    return HTMLResponse(prebuilt_html(title="FastUI Demo"))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8006)
