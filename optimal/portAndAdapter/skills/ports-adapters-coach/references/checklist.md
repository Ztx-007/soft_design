# Ports and Adapters Checklist

## Boundary Checks

- Domain imports no FastAPI/Flask/SQLAlchemy modules.
- API layer does not encode core business decisions.
- Adapter contains SQL/network/framework-specific code only.
- Port names reflect business capabilities, not implementation details.

## Refactor Safety Checks

- Endpoint request/response schemas remain compatible.
- Domain exceptions are mapped to transport errors at boundary.
- Adapter switching requires wiring change, not domain rewrite.
- DB transaction/connection scope is explicit and localized.

## Test Checks

- Domain use case has unit tests with fake/stub port.
- At least one adapter-level integration path is covered.
- Error scenarios covered: invalid input, unknown entity, insufficient state.
