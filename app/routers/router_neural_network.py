from fastapi import APIRouter
from app.models.canvas import Canvas
from app.core.neural_network.recognize_digit import predict_digit

tags = ["Neural network"]
router_neural_network = APIRouter(
    prefix="/neural_network"
)


@router_neural_network.post("/recognize", tags=tags)
async def recognize_route(canvas: Canvas):
    digit, predict = predict_digit(canvas)
    return {
        "digit": digit,
        "predict": predict,
    }
