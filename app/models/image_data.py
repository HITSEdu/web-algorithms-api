from pydantic import BaseModel


class ImageData(BaseModel):
    pixels: list[int]
