# Mock `etsi-0014` Server

This repo contains a mock implementation of the ETSI GS QKD 014 V1.1.1 (2019).
It is meant to be used for testing integration with other parties. 

_DO NOT USE THIS IN PRODUCTION_ 


# Develop
We use [poetry](https://python-poetry.org/) to develop and maintain this
application.

To get started grab a copy of this source code and clone it.

To run enter:
```bash
poetry  run uvicorn etsi0014_server.asgi:app --reload
```