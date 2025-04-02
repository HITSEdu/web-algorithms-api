from fastapi import APIRouter, Query
from app.models.canvas import Canvas
from app.algorithms.clusterization.clusterization import clusterization_method
from app.algorithms.clusterization.generate_grid import generate

clusterization_router = APIRouter(
    prefix="/clusterization"
)


@clusterization_router.get("/generate")
async def generate_grid(
        size: int = Query(...),
        fullness: int = Query(...)
):
    return {'grid': generate(size, fullness)}


@clusterization_router.post("/clusterize")
async def clusterize(canvas: Canvas):
    data = clusterization_method(canvas=canvas.pixels);
    return {
        "k": data["k"],
        "canvas": data["canvas"],
        "c": data["c"],
        }

# uvicorn main:app --host 0.0.0.0 --port 80