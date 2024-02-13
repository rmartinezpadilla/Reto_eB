from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Battle(BaseModel):
    name_pokemon_a:str
    name_pokemon_b:str
    created_at:Optional[datetime] = None
    updated_at:Optional[datetime] = None
