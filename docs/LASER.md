# Laser Class Guide

## Purpose

`qxti.physics.laser.Laser` represents a single optical pulse.

Its job is intentionally narrow:

- store the pulse parameters
- define the envelope and carrier
- define the polarization geometry
- return the electric field `E(t)`
- return the vector potential `A(t)`

It does not know anything about the Hamiltonian, bands, k-space, or the solver.

## File Location

- Implementation: `qxti/physics/laser.py`
- Interactive preview/test script: `tests/test_laser.py`

## Current Design

The current version of `Laser` is a simplified pulse model based on:

- one carrier frequency `omega`
- one field amplitude `E0`
- one scalar ellipticity parameter
- one envelope function
- one time center `t0`
- one orientation in space through `theta` and `phi`

This is the full public interface right now:

```python
Laser(
    omega,
    E0,
    phase=0.0,
    ellipticity=0.0,
    fwhm=1.0,
    envelope="gaussian",
    t0=0.0,
    theta=math.pi / 2.0,
    phi=0.0,
)
```

## Parameter-by-Parameter Explanation

### `omega`

Carrier angular frequency.

- Must be strictly positive.
- Sets the oscillation rate of the carrier.
- Also sets the natural period:

```text
T = 2 pi / omega
```

### `E0`

Peak field amplitude scale.

- Must be non-negative.
- Scales both `E(t)` and `A(t)`.

### `phase`

Carrier phase offset.

- Shifts the oscillation phase.
- Appears inside the carrier as:

```text
omega * (t - t0) + phase
```

### `ellipticity`

Controls polarization shape and rotation sense.

Allowed range:

```text
-1 <= ellipticity <= 1
```

Interpretation:

- `ellipticity = 0`: linear polarization
- `ellipticity = +1`: right-circular polarization
- `ellipticity = -1`: left-circular polarization
- intermediate values: elliptical polarization

In the current implementation, the major-axis component has unit weight and the minor-axis component is multiplied by `ellipticity`.

That means:

- the sign chooses the handedness
- the magnitude chooses how much of the minor axis is mixed in

### `fwhm`

Pulse width parameter.

- Must be strictly positive.
- Used by the supported envelope functions.
- Interpreted as a full width at half maximum scale for the supported pulse shapes.

### `envelope`

Name of the envelope model.

Supported values:

- `"gaussian"`
- `"sech"`
- `"cos2"`
- `"constant"`

More detail appears in the envelope section below.

### `t0`

Pulse center in time.

- Shifts the pulse along the time axis.
- The envelope is evaluated using `t - t0`.
- The carrier phase is also centered around `t0`.

So:

- `t0 = 0` centers the pulse at `t = 0`
- `t0 > 0` shifts the pulse to later times
- `t0 < 0` shifts the pulse to earlier times

### `theta`

Polar angle used to orient the main polarization axis.

This follows the usual spherical-angle convention used in the class:

- `theta = pi/2, phi = 0` points along `x`
- `theta = pi/2, phi = pi/2` points along `y`
- `theta = 0` points along `z`

### `phi`

Azimuthal angle used together with `theta` to orient the major polarization axis in 3D.

## Polarization Convention

The class first builds the major polarization direction:

```text
u_major = (
    sin(theta) cos(phi),
    sin(theta) sin(phi),
    cos(theta)
)
```

That vector is what `polarization_vector()` returns.

Then the class constructs a local orthonormal basis:

- major axis
- minor axis
- normal to the polarization plane

This basis is created internally by:

1. taking the major axis from `theta` and `phi`
2. choosing a reference vector
3. building a perpendicular minor axis with a cross product
4. building the plane normal from another cross product

This basis is what `rotation_matrix()` returns as its columns.

## Supported Envelopes

All envelopes are centered around:

```text
tau = t - t0
```

### 1. Gaussian

```text
g(t) = exp(-4 ln(2) (tau / fwhm)^2)
```

Properties:

- smooth
- symmetric around `t0`
- decays rapidly
- reaches half maximum at `|tau| = fwhm / 2`

### 2. Sech

```text
g(t) = 1 / cosh(scale * tau)
scale = 2 acosh(2) / fwhm
```

Properties:

- smooth
- symmetric around `t0`
- slower tails than a Gaussian
- often used in ultrafast pulse models

### 3. Cosine-Squared

```text
g(t) = cos(pi tau / fwhm)^2    for |tau| <= fwhm / 2
g(t) = 0                       otherwise
```

Properties:

- compact support
- exactly zero outside a finite time window
- useful when you want a pulse that is explicitly cut off

### 4. Constant

```text
g(t) = 1
```

Properties:

- no pulse decay
- useful for debugging
- useful for visualizing polarization more clearly

## Carrier

The carrier used by the class is:

```text
carrier(t) = cos(omega * (t - t0) + phase)
```

This is returned by `carrier(t)`.

## Electric Field

The electric field is constructed in the local polarization basis as:

```text
E(t) = E0 * g(t) * [ cos(phase_arg) * u_major
                   + ellipticity * sin(phase_arg) * u_minor ]
```

where:

- `g(t)` is the envelope
- `phase_arg = omega * (t - t0) + phase`
- `u_major` is the main polarization direction
- `u_minor` is the perpendicular minor-axis direction

Interpretation:

- the cosine term lives on the major axis
- the sine term lives on the minor axis
- the sign of `ellipticity` changes the rotation sense
- the magnitude of `ellipticity` controls how circular the field becomes

Special cases:

- `ellipticity = 0`: only the major-axis term survives, so the field is linear
- `ellipticity = +1`: the major and minor components have equal amplitude, producing right-circular motion
- `ellipticity = -1`: same amplitude, opposite rotation sense

## Vector Potential

The class also defines:

```text
A(t) = -(E0 / omega) * g(t) * [ sin(phase_arg) * u_major
                              - ellipticity * cos(phase_arg) * u_minor ]
```

This is returned by `vector_potential(t)`.

## Important Modeling Note

In the current simplified implementation, `E(t)` and `A(t)` are both defined analytically from the same envelope and carrier structure.

That means:

- the class does provide both `E(t)` and `A(t)`
- but `A(t)` is not built by numerically integrating `E(t)`
- and `E(t)` is not explicitly computed as `-dA/dt` including envelope-derivative corrections

For constant envelopes, the two are consistent with the usual carrier-level relation.

For time-dependent envelopes, this is still a useful and simple model, but it is not yet the most complete gauge-consistent implementation possible.

That simplification is deliberate in the current stage of the project.

## Intensity

The class currently uses:

```text
intensity = 0.5 * E0^2 * (1 + ellipticity^2)
```

This is a simple cycle-averaged scalar intensity estimate in atomic units.

It is returned by `intensity()`.

## Summary Output

`summary()` returns a dictionary containing:

- all dataclass fields
- `polarization_vector`
- `rotation_matrix`
- `intensity`

This is helpful for debugging, logging, exporting, or inspecting the pulse configuration.

## Input and Output Shapes

Most time-dependent methods accept either:

- a scalar time
- a NumPy array of times

Behavior:

- scalar input -> scalar for scalar-returning methods
- array input -> NumPy array output

Examples:

- `envelope_function(t)` -> scalar or array
- `carrier(t)` -> scalar or array
- `electric_field(t)` -> shape `(..., 3)`
- `vector_potential(t)` -> shape `(..., 3)`

## Validation Rules

The constructor currently checks:

- `omega > 0`
- `E0 >= 0`
- `-1 <= ellipticity <= 1`
- `fwhm > 0`
- `envelope` belongs to the supported set

If a value is invalid, the class raises `ValueError`.

## Minimal Examples

### Linear polarization along x

```python
from qxti.physics import Laser
import math

laser = Laser(
    omega=1.0,
    E0=1.0,
    ellipticity=0.0,
    envelope="gaussian",
    fwhm=20.0,
    theta=math.pi / 2,
    phi=0.0,
)
```

### Linear polarization along y

```python
laser = Laser(
    omega=1.0,
    E0=1.0,
    ellipticity=0.0,
    envelope="gaussian",
    fwhm=20.0,
    theta=math.pi / 2,
    phi=math.pi / 2,
)
```

### Linear polarization along z

```python
laser = Laser(
    omega=1.0,
    E0=1.0,
    ellipticity=0.0,
    envelope="gaussian",
    fwhm=20.0,
    theta=0.0,
    phi=0.0,
)
```

### Right-circular polarization

```python
laser = Laser(
    omega=1.0,
    E0=1.0,
    ellipticity=1.0,
    envelope="constant",
    fwhm=20.0,
    theta=math.pi / 2,
    phi=0.0,
)
```

### Left-circular polarization

```python
laser = Laser(
    omega=1.0,
    E0=1.0,
    ellipticity=-1.0,
    envelope="constant",
    fwhm=20.0,
    theta=math.pi / 2,
    phi=0.0,
)
```

## How to Preview a Pulse

The easiest way to inspect the class visually is the test script:

`tests/test_laser.py`

At the top of that file you can edit:

- `PREVIEW_LASER_PARAMS`
- `PREVIEW_TIME_PARAMS`

Then run:

```bash
python tests/test_laser.py
```

If `matplotlib` is available, the script generates:

- `tests/laser_preview.png`

That preview currently shows:

- `Ex` vs `Ey`
- `Ex` vs `Ez`
- `Ex(t)`, `Ey(t)`, `Ez(t)`
- the positive and negative envelope in normalized time

## Relationship With the Rest of QXTI

This class is meant to be a low-level pulse object.

In the project architecture:

- `Laser` defines one pulse
- a future `LaserSystem` will combine several pulses if needed
- the Hamiltonian remains independent from the pulse definition
- higher-level response modules will consume `E(t)` or `A(t)` without storing laser-specific logic inside the Hamiltonian layer

## Current Limitations

The current class is intentionally simple.

Things not yet implemented include:

- multiple pulses in one object
- gauge-selection logic beyond the current simplified formulas
- chirp
- CEP-specific helpers beyond the raw `phase`
- independent major/minor-axis amplitude controls
- arbitrary user-defined envelope callables
- explicit unit-conversion helpers

## Practical Recommendation

Use this class when you want:

- a clean and simple pulse model
- direct access to `E(t)` and `A(t)`
- easy control of linear, elliptical, and circular polarization
- a small number of parameters that are easy to visualize and debug

If later the project needs stronger physical detail, this class can be extended without changing its main role: represent one pulse and only one pulse.
