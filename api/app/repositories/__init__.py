"""Repositories — abstract interfaces for persistence.

Each repository defines:
  - An abstract Protocol describing what use cases need
  - A concrete Mongo implementation

Use cases depend on the Protocol, not the concrete class. Tests can pass an
in-memory fake; production wires the Mongo impl via FastAPI Depends().
"""
