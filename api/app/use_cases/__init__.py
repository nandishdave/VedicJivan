"""Use cases — application-specific business workflows.

A use case orchestrates one user-facing operation: validates input, calls
repositories, applies business rules, and returns a result. It MUST NOT
import fastapi or motor — those are infrastructure concerns it doesn't
need to know about.

Each use case is a callable class (`__call__` or `execute()`) that takes
its dependencies in `__init__` so they can be substituted in tests.
"""
