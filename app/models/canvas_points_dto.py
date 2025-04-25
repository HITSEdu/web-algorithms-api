from typing import List
from pydantic import BaseModel
from app.models.point_dto import PointDTO


class CanvasPointsDTO(BaseModel):
    points: List[PointDTO]
