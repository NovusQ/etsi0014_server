from etsi0014_server.keystore import KeyStore
from etsi0014_server.responses import Error, Key
from etsi0014_server.requests import KeyId

import base64

def test_keystore():

    alice_secret = b"Alice's secret"
    keystore = KeyStore()
    keystore.create_symmetric_key("Alice", "Bob", alice_secret)
    keystore.create_symmetric_key("Bob", "Alice", b"Bob's secret")

    # Invalid Key ID.
    key = KeyId(key_id = "ssaderds")
    res = keystore.get_key("Alice", "Bob", key)
    assert(isinstance(res, Error))

    # Reserve invalid sae id
    key = keystore.reserve_key("Charlie", "Sydney")
    assert(isinstance(res, Error))

    key = keystore.reserve_key("Alice", "Sydney")
    assert(isinstance(res, Error))

    # Try to reserve key for valid SAE IDs
    key_id = keystore.reserve_key("Alice", "Bob")
    key_uuid = KeyId(key_id = key_id.key_ID)
    key = keystore.get_key("Alice", "Bob", key_uuid)
    
    # Retrive those keys
    assert(isinstance(key, Key))
    assert(key_id == key)

    key = keystore.get_key("Bob", "Alice", key_uuid)
    assert(isinstance(key, Error))
