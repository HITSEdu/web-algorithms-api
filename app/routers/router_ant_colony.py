from fastapi import APIRouter, Query
from app.models.canvas_dto import CanvasDTO
from app.core.ant_colony.ant_colony import find_path_ant
from app.core.ant_colony.generate_ant_grid import generate_ant_grid

tags = ["Ant Colony"]
router_ant_colony = APIRouter(
    prefix="/ant"
)


@router_ant_colony.get("/generate", tags=tags)
async def generate_grid(
    size: int = Query(...),
    fullness: int = Query(...)
):
    return {'grid': generate_ant_grid(size, fullness)}


@router_ant_colony.post("/find-path", tags=tags)
async def find_path_ant_route(
    data: CanvasDTO,
):
    path, history = find_path_ant(data.pixels)
    return {"path": path, "history": history}
