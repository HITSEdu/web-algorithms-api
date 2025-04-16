from fastapi import APIRouter, Query
from app.models.canvas import Canvas
from app.core.ant_colony.ant_colony import find_path_ant
from app.core.generate_tsp_grid import generate_tsp_grid

tags = ["Ant Colony"]
router_ant_colony = APIRouter(
    prefix="/ant"
)


@router_ant_colony.get("/generate", tags=tags)
async def generate_ant_grid(
    size: int = Query(...),
    fullness: int = Query(...)
):
    return {'grid': generate_tsp_grid(size, fullness)}


@router_ant_colony.post("/find-path", tags=tags)
async def find_path_ant_route(
    data: Canvas,
):
    path, history = find_path_ant(data.pixels)
    return {"path": path, "history": history}
