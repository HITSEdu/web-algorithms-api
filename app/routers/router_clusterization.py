from fastapi import APIRouter, Query
from app.models.canvas import Canvas
from app.core.clusterization.clusterization import clusterization_method
from app.core.clusterization.generate_grid import generate


tags = ["Clusterization"]
router_clusterization = APIRouter(
    prefix="/clusterization"
)


@router_clusterization.get("/generate", tags=tags)
async def generate_grid(
        size: int = Query(...),
        fullness: int = Query(...)
):
    return {'grid': generate(size, fullness)}


@router_clusterization.post("/clusterize", tags=tags)
async def clusterize(canvas: Canvas):
    data = clusterization_method(canvas=canvas.pixels);
    return {
        "k": data["k"],
        "canvas": data["canvas"],
        "c": data["c"],
        }
