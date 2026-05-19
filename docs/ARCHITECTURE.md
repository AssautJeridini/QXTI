# QXTI Architecture

## Overview

QXTI is designed as a modular object-oriented framework for perturbative optical-response simulations in generic tight-binding Hamiltonians.

All calculations are intended to run internally in atomic units.

## Core Design Rules

1. The Hamiltonian layer must not depend on laser objects.
2. The laser layer must not depend on Hamiltonian objects.
3. `CMD` is the first layer allowed to combine Hamiltonian and laser information.
4. The graphics layer is responsible only for plotting.
5. `PDG` is responsible only for organizing and exporting data.
6. `QXTISimulation` coordinates the workflow but should not absorb physics-specific logic.
7. Atomic units are the default internal system everywhere.
8. Runtime configuration should originate from `inputParams.cfg`.

## Package Responsibilities

### `qxti/core`

- `config.py`: parse and validate simulation inputs.
- `simulation.py`: orchestrate the end-to-end run.
- `results.py`: define containers for simulation outputs.

### `qxti/physics`

- Hamiltonian abstractions and concrete models.
- Laser pulse definitions and composite laser systems.
- Operators and observables used during response calculations.

### `qxti/grids`

- Reciprocal-space grids.
- Time grids.
- Frequency grids.

### `qxti/solvers`

- Common solver interfaces.
- Perturbative and domain-specific implementations.

### `qxti/response`

- Coupling and response engines such as `CMD` and `XTP`.

### `qxti/data`

- Data organization, loading, and export utilities.

### `qxti/graphics`

- Plotting utilities for bands, DOS, response observables, and harmonics.

### `qxti/utils`

- Shared constants, validators, math helpers, and I/O helpers.

## Simulation Flow

```text
inputParams.cfg
        ↓
Config
        ↓
QXTISimulation
        ↓
Hamiltonian + LaserSystem + Grids
        ↓
OperatorFactory
        ↓
CMD
        ↓
rho^(0), rho^(1), rho^(2), rho^(3)
        ↓
XTP + ObservableCalculator
        ↓
P(t), J(t), chi, HHG
        ↓
SimulationResult
        ↓
PDG
        ↓
Graphics
```

## Implementation Note

The current repository state intentionally provides the full skeleton first. Scientific logic can now be added incrementally without changing the high-level structure.
