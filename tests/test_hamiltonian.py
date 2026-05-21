import numpy as np
import pytest

from qxti.physics import Hamiltonian


class TwoBandHamiltonian(Hamiltonian):
    def H(self, kx: float, ky: float, kz: float) -> np.ndarray:
        mass = self.params["mass"]
        coupling = self.params["coupling"]
        return np.array(
            [
                [mass + kx**2, coupling * (kx - 1j * ky)],
                [coupling * (kx + 1j * ky), -mass + ky**2],
            ],
            dtype=complex,
        )

    def default_params(self) -> dict[str, float]:
        return {"mass": 1.0, "coupling": 2.0}


def test_hamiltonian_defaults_and_shape() -> None:
    hamiltonian = TwoBandHamiltonian(model_name="two-band", basis_size=2)

    assert hamiltonian.params == {"mass": 1.0, "coupling": 2.0}
    assert hamiltonian.H(0.0, 0.0, 0.0).shape == (2, 2)
    assert hamiltonian.validate_hermiticity(0.2, -0.1, 0.0)


def test_hamiltonian_derivative_and_operators() -> None:
    hamiltonian = TwoBandHamiltonian(model_name="two-band", basis_size=2)

    velocity_x = hamiltonian.velocity_operator(0.3, 0.2, 0.0, "x")
    inverse_mass_xx = hamiltonian.inverse_mass_operator(0.3, 0.2, 0.0, "x", "x")

    np.testing.assert_allclose(
        velocity_x,
        np.array([[0.6, 2.0], [2.0, 0.0]], dtype=complex),
        atol=1.0e-9,
    )
    np.testing.assert_allclose(
        inverse_mass_xx,
        np.array([[2.0, 0.0], [0.0, 0.0]], dtype=complex),
        atol=1.0e-5,
    )


def test_hamiltonian_band_basis_transform_is_unitary_similarity() -> None:
    hamiltonian = TwoBandHamiltonian(model_name="two-band", basis_size=2)
    operator = hamiltonian.velocity_operator(0.3, 0.2, 0.0, "y")
    vectors = hamiltonian.eigenvectors(0.3, 0.2, 0.0)

    transformed = hamiltonian.transform_to_band_basis(operator, 0.3, 0.2, 0.0)

    np.testing.assert_allclose(transformed, vectors.conj().T @ operator @ vectors)


def test_hamiltonian_rejects_invalid_direction() -> None:
    hamiltonian = TwoBandHamiltonian(
        model_name="two-band",
        basis_size=2,
        dimension=2,
    )

    with pytest.raises(ValueError, match="outside dimension"):
        hamiltonian.dH_dk(0.0, 0.0, 0.0, "z")
