
# QXTI — Quantum X Tight-binding Interface

## General Description

QXTI is a modular object-oriented Python framework for perturbative optical-response simulations in generic tight-binding Hamiltonians.

All calculations are performed internally in atomic units.

Core outputs:
- rho^(0), rho^(1), rho^(2), rho^(3)
- Polarization P(t)
- Current J(t)
- Susceptibility tensors
- Harmonic spectra
- Band populations
- DOS and band structures

---

# Core Design Rules

1. Hamiltonian does NOT depend on Laser.
2. Laser does NOT depend on Hamiltonian.
3. CMD is the first module combining Hamiltonian + LaserSystem.
4. Graphics only plots.
5. PDG only organizes/export data.
6. QXTISimulation only coordinates.
7. All calculations use atomic units.
8. Everything comes from inputParams.cfg.

---

# Project Structure

```text
QXTI/
├── inputParams.cfg
├── main.py
├── qxti/
│   ├── core/
│   │   ├── simulation.py
│   │   ├── config.py
│   │   └── results.py
│   ├── physics/
│   │   ├── hamiltonian.py
│   │   ├── custom_hamiltonian.py
│   │   ├── laser.py
│   │   ├── laser_system.py
│   │   ├── operators.py
│   │   └── observables.py
│   ├── grids/
│   │   ├── kgrid.py
│   │   ├── timegrid.py
│   │   └── frequencygrid.py
│   ├── solvers/
│   │   ├── solver.py
│   │   ├── perturbative_solver.py
│   │   ├── time_domain_solver.py
│   │   └── frequency_domain_solver.py
│   ├── response/
│   │   ├── cmd.py
│   │   └── xtp.py
│   ├── data/
│   │   ├── pdg.py
│   │   ├── exporters.py
│   │   └── loaders.py
│   ├── graphics/
│   │   ├── graphics.py
│   │   ├── plot_bands.py
│   │   ├── plot_dos.py
│   │   ├── plot_response.py
│   │   └── plot_harmonics.py
│   └── utils/
│       ├── constants.py
│       ├── validators.py
│       ├── math_utils.py
│       └── io_utils.py
├── models/
├── examples/
├── tests/
└── docs/
```

---

# Main Simulation Flow

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
