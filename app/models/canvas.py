from pydantic import BaseModel


class Canvas(BaseModel):
    pixels: list[list[int]]
