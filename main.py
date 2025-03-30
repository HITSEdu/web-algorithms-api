from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from algorithms.aStar import a_star, create_random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Canvas(BaseModel):
    pixels: list[list[int]]


@app.get("/generate")
async def generate_grid(
        size: int = Query(...),
        fullness: int = Query(...)
):
    return {'grid': create_random(size, fullness)}


@app.post("/find-path")
async def find_path(data: Canvas):
    start, end = None, None

    for row_idx, row in enumerate(data.pixels):
        for col_idx, cell in enumerate(row):
            if cell == 2:
                start = (row_idx, col_idx)
            elif cell == 3:
                end = (row_idx, col_idx)

    path = a_star(data.pixels, start, end)

    if path is None:
        return {"path": []}

    return {"path": path}
