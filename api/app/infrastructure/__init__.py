"""Infrastructure — config, logging, DB connection, and DI wiring.

Everything here is concrete (env vars, Mongo driver, Python logging). The
domain and use_cases packages don't import from here directly — they get
their dependencies via FastAPI Depends() factories defined in this layer.
"""
