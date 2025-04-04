from typing import List
from pydantic import BaseModel


class Canvas(BaseModel):
    pixels: List[List[int]]
