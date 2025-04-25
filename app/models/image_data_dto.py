from pydantic import BaseModel


class ImageDataDTO(BaseModel):
    pixels: list[int]
