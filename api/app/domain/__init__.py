"""Domain layer — pure business types and rules.

Anything in this package MUST NOT import:
  - fastapi (no HTTP concepts)
  - motor / pymongo (no DB concepts)
  - app.routers / app.services (no infrastructure)

This is the heart of the application. If FastAPI was replaced by gRPC and
MongoDB by Postgres, this package would not change.
"""
