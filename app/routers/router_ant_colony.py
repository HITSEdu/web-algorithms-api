from fastapi import APIRouter, Body, Query
from app.models.canvas import Canvas
from app.core.ant_colony.ant_colony import create_random_ant_grid, find_path_ant

tags = ["Ant Colony"]
router_ant_colony = APIRouter(
    prefix="/ant"
)


@router_ant_colony.get("/generate", tags=tags)
async def generate_ant_grid(
    size: int = Query(...),
    fullness: int = Query(...)
):
    return {'grid': create_random_ant_grid(size, fullness)}


@router_ant_colony.post("/find-path", tags=tags)
async def find_path_ant_route(
    data: Canvas,
):
    path, history = find_path_ant(data.pixels)
    return {"path": path, "history": history}