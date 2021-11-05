from fastapi import FastAPI
from typing import Union
from .requests import KeyRequest, KeyIds
from .responses import KeyContainer, Error


app = FastAPI(title="Mock ETSI0014 API")

@app.post("/api/v1/keys/{slave_SAE_ID}/enc_keys")
def enc_keys(slave_SAE_ID: str, key_request: KeyRequest):
    return {}

@app.get("/api/v1/keys/{slave_SAE_ID}/enc_keys")
def get_enc_keys(slave_SAE_ID: str, number: int, size: int) -> Union[Error, KeyContainer]:
    if size != 4096:
        err = Error()
        err.message = "Only support 4096 bits"
        return err
    return {}

@app.post("/api/v1/keys/{master_SAE_ID}/dec_keys")
def dec_keys(master_SAE_ID: str, key_ids: KeyIds):
    return {}

@app.get("/api/v1/keys/{master_SAE_ID}/dec_keys")
def dec_keys(master_SAE_ID: str, key_ids: KeyIds):
    return {}

@app.get("/api/v1/keys/{slave_SAE_ID}/status")
def status(slave_SAE_ID: str):
    return {}