from typing import List, Optional, Any, AnyStr, Dict, Union

from pydantic import BaseModel

JSONObject = Dict[AnyStr, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]

class KeyRequest(BaseModel):
    number: Optional[int]
    size: Optional[int]
    additional_slave_SAE_IDs: Optional[List[int]]
    extension_mandatory: Optional[JSONStructure]
    extension_optional: Optional[JSONStructure]

class KeyId(BaseModel):
    key_id: str

class KeyIds(BaseModel):
    key_ids: List[KeyId]