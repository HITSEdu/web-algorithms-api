from fastapi import APIRouter
from app.core.genetic.genetic import solve_tsp_genetic
from app.core.genetic.generate_points import generate_random_points
from app.models.canvas_points_dto import CanvasPointsDTO

tags=["Genetic"]
router_genetic = APIRouter(
    prefix="/genetic"
)

@router_genetic.post("/solve", tags=tags)
async def solve_tsp(data: CanvasPointsDTO):
    result = solve_tsp_genetic(data.points)
    return {
        "path": result["path"],
        "history": result["history"]
    }


@router_genetic.get("/generate", tags=tags)
async def generate_points(count: int):
    points = generate_random_points(count)
    return {"points": points}
