from fastapi import APIRouter

from app.core.genetic.genetic import Canvas, solve_tsp_genetic, generate_random_points

tags=["Genetic"]
router_genetic = APIRouter(
    prefix="/genetic"
)

@router_genetic.post("/solve", tags=tags)
async def solve_tsp(data: Canvas):
    result = solve_tsp_genetic(data.points)
    return {
        "path": result["path"],
        "history": result["history"]
    }

@router_genetic.get("/generate", tags=tags)
async def generate_points(count: int):
    points = generate_random_points(count)
    return {"points": points}