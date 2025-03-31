from fastapi import APIRouter, Query
from app.models.canvas import Canvas
from app.algorithms.a_star import create_random, find_path
from app.algorithms.neural_net.recognize_digit import predict_digit

router = APIRouter()


@router.get("/generate")
async def generate_grid(
        size: int = Query(...),
        fullness: int = Query(...)
):
    return {'grid': create_random(size, fullness)}


@router.post("/find-path")
async def find_path_route(data: Canvas):
    return {"path": find_path(data.pixels)}


@router.post("/recognize")
async def recognize_route(data: Canvas):
    return {"digit": predict_digit(data.pixels)}
