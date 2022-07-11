from os import stat
from fastapi import FastAPI, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from typing import Union
from .keystore import KeyStore
from .requests import KeyRequest, KeyIds, KeyId
from .responses import KeyContainer, Error


app = FastAPI(title="Zetta-3 QKD Device API")
keystore = KeyStore()

"""
Create 3 pre-calculated keys for use.
"""
for i in range(3):
    keystore.create_symmetric_key("Alice", "Bob")
    keystore.create_symmetric_key("Bob", "Alice")
    keystore.create_symmetric_key("Alice", "Charlie")
    keystore.create_symmetric_key("Charlie", "Alice")
    keystore.create_symmetric_key("Charlie", "Bob")
    keystore.create_symmetric_key("Bob", "Charlie")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(Error(message="malformated request"), status_code=400)

@app.post(
    "/{master_SAE_ID}/api/v1/keys/{slave_SAE_ID}/enc_keys",
    response_model=Union[KeyContainer, Error],
    status_code=status.HTTP_200_OK)
def enc_keys(
    master_SAE_ID: str,
    slave_SAE_ID: str,
    key_request: KeyRequest,
    response: Response) -> Union[KeyContainer, Error]:
    """
    Call this to get new Encryption Keys.
    Returns a new key without a key ID. Returns 200 Status Code with a KeyContainer
    if successful. Will return status code 401 if there are no keys left. It is
    recommended you call the status endpoint before calling this endpoint to make
    sure there are enough keys.
    """
    number = key_request.number
    size = key_request.size
    
    keys = []

    for _ in range(number):
    
        key = keystore.reserve_key(master_SAE_ID, slave_SAE_ID)
    
        if isinstance(key, Error):
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return Error
    
        if size != 4096:
            response.status_code = status.HTTP_400_BAD_REQUEST
            err = Error()
            err.message = "Only support 4096 bits"
            return err
        keys.append(key)

    return KeyContainer(keys=keys)

@app.get(
    "/{master_SAE_ID}/api/v1/keys/{slave_SAE_ID}/enc_keys",
    response_model=Union[KeyContainer, Error],
    status_code=status.HTTP_200_OK)
def get_enc_keys(
    master_SAE_ID: str, 
    slave_SAE_ID: str, 
    number: int, 
    size: int, 
    response: Response) -> Union[KeyContainer, Error]:
    """
    Call this to get new Encryption Keys.
    Returns a new key without a key ID. Returns 200 Status Code with a KeyContainer
    if successful. Will return status code 401 if there are no keys left. It is
    recommended you call the status endpoint before calling this endpoint to make
    sure there are enough keys.
    """
    if size != 4096:
        response.status_code = status.HTTP_400_BAD_REQUEST
        err = Error(message = "Only support 4096 bits")
        return err
    
    keys = []
    for _ in range(number):
        key = keystore.reserve_key(master_SAE_ID, slave_SAE_ID)
        if isinstance(key, Error):
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return key
        keys.append(key)

    return KeyContainer(keys=keys)

@app.post(
    "/{slave_SAE_ID}/api/v1/keys/{master_SAE_ID}/dec_keys",
    response_model=Union[KeyContainer, Error],
    status_code=status.HTTP_200_OK)
def dec_keys(slave_SAE_ID: str, master_SAE_ID: str, key_ids: KeyIds, response: Response):
    """
    Retrieve keys given a series of KeyIDs.
    Returns status 401 if keys are not found.
    """
    keys = []
    for key in key_ids.key_ids:
        res = keystore.get_key(master_SAE_ID, slave_SAE_ID, key)
        if isinstance(res, Error):
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return res
        keys.append(res)
    
    return KeyContainer(keys=keys)

@app.get("/{slave_SAE_ID}/api/v1/keys/{master_SAE_ID}/dec_keys")
def get_dec_keys(slave_SAE_ID: str, master_SAE_ID: str, key_ID: str, response: Response):
    """
    Retrieves a key given a series of KeyIDs.
    Returns status 401 if keys are not found.
    """
    res = keystore.get_key(master_SAE_ID, slave_SAE_ID, KeyId(key_id = key_ID))
    if isinstance(res, Error):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return res
    return KeyContainer(keys=[res])

@app.get("/{master_SAE_ID}/api/v1/keys/{slave_SAE_ID}/status")
def get_status(master_SAE_ID: str, slave_SAE_ID: str):
    """
    Get status. You should call this to check number of keys available.
    """
    return keystore.get_status(master_SAE_ID, slave_SAE_ID)