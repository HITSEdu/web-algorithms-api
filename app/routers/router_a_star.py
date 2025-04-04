from fastapi import APIRouter, Query
from app.models.canvas import Canvas
from app.core.a_star.a_star import create_random, find_path


tags = ["A*"]
router_a_star = APIRouter(
    prefix="/a"
)


@router_a_star.get("/generate", tags=tags)
async def generate_grid(
        size: int = Query(...),
        fullness: int = Query(...)
):
    return {'grid': create_random(size, fullness)}


@router_a_star.post("/find-path", tags=tags)
async def find_path_route(data: Canvas):
    path, history = find_path(data.pixels)
    return {"path": path, "history": history}