from etsi0014_server.keystore import KeyStore
from etsi0014_server.responses import Error
from etsi0014_server.requests import KeyId

def test_keystore():

    keystore = KeyStore()
    keystore.create_symmetric_key("Alice", "Bob", b"Alice's secret")
    keystore.create_symmetric_key("Bob", "Alice", b"Bob's secret")

    key = KeyId(key_id = "ssaderds")
    res = keystore.get_key("Alice", "Bob", key)

    assert(isinstance(res, Error))