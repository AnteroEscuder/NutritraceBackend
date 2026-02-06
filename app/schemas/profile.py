from pydantic import BaseModel
from typing import List

class UserAllergiesUpdate(BaseModel):
    allergen_ids: List[int]
