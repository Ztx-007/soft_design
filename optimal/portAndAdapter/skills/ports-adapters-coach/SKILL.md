---
name: ports-adapters-coach
description: Explain and apply Ports and Adapters (Hexagonal) architecture in Python/FastAPI services. Use when code mixes route handlers, business rules, and database access in the same function, or when the user asks to extract domain use cases, define ports, add adapters, improve testability, or switch infrastructure implementations with minimal behavior change.
---

# Ports Adapters Coach

## Overview

Refactor Python backend code from tightly coupled handlers into clear domain, port, and adapter layers. Keep behavior stable while making infrastructure replaceable and domain logic unit-test friendly.

## Workflow

1. Identify coupling hotspots
- Find files where HTTP concerns, business checks, and DB queries are mixed.
- Record current behavior and API contract before edits.

2. Extract domain core
- Move request-independent business rules into `domain/use_cases.py`.
- Keep business data in `domain/models.py`.
- Keep business-only exceptions in `domain/errors.py`.

3. Define ports
- Add protocol-style interfaces in `domain/ports.py`.
- Describe required behavior (`get_stock`, `decrease_stock`) without framework details.

4. Implement adapters
- Put SQLAlchemy/FastAPI/client specific code in `adapters/`.
- Implement each port against concrete infrastructure.

5. Wire dependencies at boundary
- In API layer (`api.py`, startup), instantiate adapter and inject it into use case.
- Convert domain exceptions to transport errors (HTTP status codes) only in API layer.

6. Verify behavior
- Run endpoint checks and ensure response schema is unchanged.
- Add at least one unit test with a fake port for domain use case.

## Guardrails

- Do not import FastAPI or SQLAlchemy inside `domain/`.
- Do not mutate port interface unless business contract changed.
- Prefer changing adapter/wiring instead of changing domain.
- Keep transaction/connection lifecycle in infrastructure boundary (`db.py`/adapter).

## Quick Mapping

- `before_api.py` style:
  route + validation + business rule + SQL in one place
- Target shape:
  `api.py` -> parse/map HTTP only
  `domain/use_cases.py` -> business decisions
  `domain/ports.py` -> abstraction contract
  `adapters/*.py` -> concrete DB/service implementation

## Response Style

When using this skill, respond with:
1. Findings: concrete coupling points with file paths.
2. Refactor plan: minimal safe steps.
3. Patch: focused edits only.
4. Validation: what was run and what remains untested.

## References

Load [references/checklist.md](references/checklist.md) when doing architecture review or final verification.
