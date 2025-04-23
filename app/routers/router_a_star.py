from fastapi import APIRouter, Query
from app.models.canvas import Canvas
from app.core.a_star.a_star import find_path
from app.core.a_star.generate_maze import generate_maze

tags = ["A*"]
router_a_star = APIRouter(
    prefix="/a"
)


@router_a_star.get("/generate", tags=tags)
async def generate_grid(
        size: int = Query(...),
        fullness: int = Query(...)
):
    return {'grid': generate_maze(size, fullness)}


@router_a_star.post("/find-path", tags=tags)
async def find_path_route(data: Canvas):
    try:
        path, history = find_path(data.pixels)
    except Exception:
        return {"path": [], "history": []}
    return {"path": path, "history": history}
