# Mock `etsi-0014` Server

This repo contains a mock implementation of the [ETSI GS QKD 014 V1.1.1 (2019)](https://www.etsi.org/deliver/etsi_gs/QKD/001_099/014/01.01.01_60/gs_qkd014v010101p.pdf).
It is meant to be used for testing integration with other parties. 

_DO NOT USE THIS IN PRODUCTION_ 


# Develop
We use [poetry](https://python-poetry.org/) to manage dependencies of this
application.

To get started grab a copy of this source code and clone it.

To fetch dependencies run:
```bash
poetry install
```

To run enter:
```bash
poetry run uvicorn etsi0014_server.asgi:app --reload
```

## Docs

Once running you can access the OpenAPI docs at `localhost:8080/docs`.

## Unit Tests

To run unit tests simply run the following command
```bash
poetry run pytest test
```
