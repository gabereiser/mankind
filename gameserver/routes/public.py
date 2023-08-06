from fastapi import APIRouter
from fastapi.responses import HTMLResponse, StreamingResponse
from uuid import UUID

router = APIRouter(prefix="", default_response_class=HTMLResponse)


@router.get("/")
def index():
    def handler():
        with open("public/index.html", mode="rb") as fp:
            yield fp.read()

    return StreamingResponse(handler(), media_type="text/html")


@router.get("/{page}")
def page_handler(page: str):
    def handler():
        with open(f"public/{page}.html", mode="rb") as fp:
            yield fp.read()

    return StreamingResponse(handler(), media_type="text/html")


@router.get("/data/universe.json", response_class=StreamingResponse)
def download_universe_data():
    def iterfile():  #
        with open("data/universe.json", mode="rb") as fp:  #
            yield from fp  #

    return StreamingResponse(iterfile(), media_type="application/json")
