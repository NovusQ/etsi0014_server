from typing import List

from pydantic import BaseModel

class Status(BaseModel):
    source_KME_ID: str
    target_KME_ID: str
    master_SAE_ID: str
    slave_SAE_ID: str
    key_size: int
    stored_key_count: int
    max_key_count: int
    max_key_per_request: int
    max_key_size: int
    min_key_size: int
    max_SAE_ID_count: int
    # leaving out status extension for now


class Key(BaseModel):
    key_ID: str
    key: str

class KeyContainer(BaseModel):
    keys: List[Key]
