from .requests import KeyId
from .responses import Key, Error, Status

from typing import Union

import uuid
import secrets
import base64

class KeyStore:
    def __init__(self) -> None:
        self.keys = {}
        self.owners = {}
        self.unallocated_keys = {}

    def create_symmetric_key(self, master: str, slave: str, secret = secrets.token_bytes(512)) -> None:
        """
        Called when we want to create a symmetric key pair in the key store. 
        This should be called whenever the quantum link successfully establishes
        a key pair.

        Parameters
        ------
        master: str
        The master SAE ID

        slave: str
        The slave SAE ID

        secret: bytes
        Optional. The bytes to be encoded. If no value is passed, we simulate a
        random source.
        """
        key_id = str(uuid.uuid4())
        while key_id in self.keys:
            key_id = str(uuid.uuid4())

        self.keys[key_id] = base64.b64encode(secret).decode('utf-8')
        
        if slave not in self.owners:
            self.owners[slave] = {}
            self.unallocated_keys[slave] = {}

        if master not in self.owners[slave]:
            self.owners[slave][master] = set()
            self.unallocated_keys[slave][master] = set()

        self.owners[slave][master].add(key_id)
        self.unallocated_keys[slave][master].add(key_id)

    def get_key(self, master: str, slave: str, key_id: KeyId) -> Union[Key, Error]:
        """" Retrieve a key given master, slave and key_id values"""
        key_uuid = key_id.key_id

        if slave not in self.owners:
            return Error(message = "Wrong master SAE ID", details = [])

        if master not in self.owners[slave]:
            return Error(message = "Wrong slave SAE ID", details = [])

        if key_uuid not in self.owners[slave][master] or key_uuid in self.unallocated_keys[slave][master]:
            return Error(message = "Key not found", details = [])
        
        key_response = Key(key_ID = key_uuid, key = self.keys[key_uuid])

        return key_response
        
    def reserve_key(self, master: str, slave: str) -> Union[Key, Error]:
        if slave not in self.owners:
            return Error(message = "Wrong slave SAE ID", details = [])

        if master not in self.owners[slave]:
            return Error(message = "Master SAE ID has no key pair established with Slave", details = [])
        
        if len(self.unallocated_keys[slave][master]) == 0:
            return Error(message = "Key pair generation not ready", details = [])
        
        key_uuid = self.unallocated_keys[slave][master].pop()
        return Key(key_ID = key_uuid, key = self.keys[key_uuid])

    def get_status(self, slave: str) -> Union[Status, Error]:

        if slave not in self.owners:
            return Error(message = "slave not found", details = [])

        status = Status() 
        status.source_KME_ID = ""
        status.target_KME_ID = ""
        status.slave_SAE_ID = slave

        return status