# app/schemas.py
from pydantic import BaseModel, ConfigDict

class Item(BaseModel):
    id: str
    name: str

    model_config = ConfigDict(from_attributes=True)