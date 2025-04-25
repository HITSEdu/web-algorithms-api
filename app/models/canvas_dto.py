from typing import List
from pydantic import BaseModel


class CanvasDTO(BaseModel):
    pixels: List[List[int]]
