# Contributing to QXTI

## General Principles

- Keep modules focused on one responsibility.
- Respect the architecture boundaries described in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).
- Prefer small, reviewable pull requests.
- Add or update tests when behavior changes.
- Keep documentation aligned with implementation.

## Development Workflow

1. Create a branch from `main`.
2. Make a focused change.
3. Run local checks relevant to the change.
4. Update docs if interfaces or behavior changed.
5. Open a pull request with context, scope, and validation notes.

## Coding Guidelines

- Use clear module boundaries.
- Avoid coupling physics, plotting, and export logic.
- Keep public APIs explicit and documented.
- Use atomic units consistently unless clearly stated otherwise.

## Pull Request Checklist

- The change has a clear purpose.
- The architecture rules are still respected.
- Tests were added or updated when appropriate.
- Documentation was updated when appropriate.
- The branch is ready to merge without hidden follow-up work.
