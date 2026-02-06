from pydantic import BaseModel

class AllergenOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
