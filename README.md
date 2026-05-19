# QXTI

Quantum X Tight-binding Interface is a modular Python framework for perturbative optical-response simulations in generic tight-binding Hamiltonians.

This repository is currently in scaffold mode: the package layout, documentation, and GitHub-ready project files are in place, while the scientific modules themselves have intentionally been left blank for the next implementation phase.

## Project Goals

- Keep Hamiltonians independent from laser definitions.
- Keep laser definitions independent from Hamiltonian models.
- Centralize simulation orchestration in a dedicated coordinator.
- Separate computation, data handling, and plotting responsibilities.
- Use atomic units consistently across the full codebase.
- Drive simulations from a single configuration entry point.

## Current Status

- Base repository structure created from the project reference document.
- Core package modules generated and left empty on purpose.
- Documentation and repository metadata prepared for GitHub publication.
- Ready for iterative implementation module by module.

## Repository Layout

```text
QXTI/
├── inputParams.cfg
├── main.py
├── qxti/
├── models/
├── examples/
├── tests/
├── docs/
├── .github/
├── README.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── CHANGELOG.md
├── LICENSE
└── pyproject.toml
```

For the full module map and architectural rules, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).
For the pulse model documentation, see [docs/LASER.md](docs/LASER.md).

## Development Roadmap

1. Define the configuration schema in `inputParams.cfg` and `qxti/core/config.py`.
2. Implement the simulation coordinator in `qxti/core/simulation.py`.
3. Add Hamiltonian, laser, grid, and operator abstractions.
4. Implement perturbative and domain-specific solvers.
5. Add post-processing, export, and visualization layers.
6. Populate `examples/`, `tests/`, and user documentation.

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
```

## Suggested First Commits

1. Define package-level constants and physical units.
2. Create the configuration parser and validation layer.
3. Add a minimal Hamiltonian interface and one toy model.
4. Wire a first executable flow through `main.py`.

## GitHub Publishing

The repository already includes issue templates, a pull request template, contributing guidelines, and a project license.

For a simple publish checklist, see [docs/GITHUB_SETUP.md](docs/GITHUB_SETUP.md).

## License

This project is distributed under the MIT License. See [LICENSE](LICENSE) for details.
