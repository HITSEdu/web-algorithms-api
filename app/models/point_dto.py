from pydantic import BaseModel


class PointDTO(BaseModel):
    id: int
    x: float
    y: float
