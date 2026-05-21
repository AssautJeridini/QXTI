from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

import numpy as np
from numpy.typing import NDArray


ComplexArray = NDArray[np.complex128]


@dataclass(slots=True)
class Hamiltonian(ABC):
    """Abstract tight-binding Hamiltonian interface.

    The Hamiltonian layer depends only on reciprocal-space coordinates. It does
    not know anything about laser pulses or external fields.
    """

    model_name: str
    params: dict[str, Any] = field(default_factory=dict)
    basis_size: int = 1
    dimension: int = 3
    basis_type: str = "orbital"
    is_periodic: bool = True

    _FINITE_DIFFERENCE_STEP = 1.0e-5
    _VALID_DIRECTIONS = {"x": 0, "y": 1, "z": 2}

    def __post_init__(self) -> None:
        if self.basis_size <= 0:
            raise ValueError("basis_size must be strictly positive.")
        if not 1 <= self.dimension <= 3:
            raise ValueError("dimension must be between 1 and 3.")
        if not self.model_name:
            raise ValueError("model_name must be a non-empty string.")
        if not self.basis_type:
            raise ValueError("basis_type must be a non-empty string.")

        defaults = self.default_params()
        defaults.update(self.params)
        self.set_params(defaults)

    def default_params(self) -> dict[str, Any]:
        """Return model parameters used when no explicit values are provided."""

        return {}

    def set_params(self, params: dict[str, Any]) -> None:
        """Update the model parameter dictionary."""

        self.params = dict(params)

    @abstractmethod
    def H(self, kx: float, ky: float, kz: float) -> ComplexArray:
        """Return the Hamiltonian matrix H(k)."""

    def dH_dk(self, kx: float, ky: float, kz: float, dir: str) -> ComplexArray:
        """Return the first k-derivative of H(k) along one direction."""

        k_plus, k_minus = self._shifted_k_points(kx, ky, kz, dir)
        step = self._FINITE_DIFFERENCE_STEP
        return (self._matrix_at(*k_plus) - self._matrix_at(*k_minus)) / (2.0 * step)

    def d2H_dk2(
        self,
        kx: float,
        ky: float,
        kz: float,
        dir1: str,
        dir2: str,
    ) -> ComplexArray:
        """Return the second k-derivative of H(k)."""

        step = self._FINITE_DIFFERENCE_STEP
        k = np.array([kx, ky, kz], dtype=float)
        axis1 = self._direction_axis(dir1)
        axis2 = self._direction_axis(dir2)

        if axis1 == axis2:
            k_plus = k.copy()
            k_minus = k.copy()
            k_plus[axis1] += step
            k_minus[axis1] -= step
            return (
                self._matrix_at(*k_plus)
                - 2.0 * self._matrix_at(*k)
                + self._matrix_at(*k_minus)
            ) / step**2

        k_pp = k.copy()
        k_pm = k.copy()
        k_mp = k.copy()
        k_mm = k.copy()
        k_pp[[axis1, axis2]] += step
        k_pm[axis1] += step
        k_pm[axis2] -= step
        k_mp[axis1] -= step
        k_mp[axis2] += step
        k_mm[[axis1, axis2]] -= step

        return (
            self._matrix_at(*k_pp)
            - self._matrix_at(*k_pm)
            - self._matrix_at(*k_mp)
            + self._matrix_at(*k_mm)
        ) / (4.0 * step**2)

    def velocity_operator(
        self,
        kx: float,
        ky: float,
        kz: float,
        dir: str,
    ) -> ComplexArray:
        """Return the velocity operator in atomic units."""

        return self.dH_dk(kx, ky, kz, dir)

    def inverse_mass_operator(
        self,
        kx: float,
        ky: float,
        kz: float,
        dir1: str,
        dir2: str,
    ) -> ComplexArray:
        """Return the inverse mass operator in atomic units."""

        return self.d2H_dk2(kx, ky, kz, dir1, dir2)

    def diagonalize(
        self,
        kx: float,
        ky: float,
        kz: float,
    ) -> tuple[NDArray[np.float64], ComplexArray]:
        """Return eigenvalues and eigenvectors of H(k)."""

        return np.linalg.eigh(self._matrix_at(kx, ky, kz))

    def eigenvalues(self, kx: float, ky: float, kz: float) -> NDArray[np.float64]:
        """Return the band energies of H(k)."""

        values, _ = self.diagonalize(kx, ky, kz)
        return values

    def eigenvectors(self, kx: float, ky: float, kz: float) -> ComplexArray:
        """Return the eigenvectors of H(k)."""

        _, vectors = self.diagonalize(kx, ky, kz)
        return vectors

    def transform_to_band_basis(
        self,
        op: NDArray[np.complexfloating[Any, Any]] | NDArray[np.floating[Any]],
        kx: float,
        ky: float,
        kz: float,
    ) -> ComplexArray:
        """Transform one operator from the original basis to the band basis."""

        operator = self._validate_matrix(op)
        vectors = self.eigenvectors(kx, ky, kz)
        return vectors.conj().T @ operator @ vectors

    def validate_hermiticity(self, kx: float, ky: float, kz: float) -> bool:
        """Return True when H(k) is Hermitian within numerical tolerance."""

        matrix = self._matrix_at(kx, ky, kz)
        return bool(np.allclose(matrix, matrix.conj().T))

    def _matrix_at(self, kx: float, ky: float, kz: float) -> ComplexArray:
        return self._validate_matrix(self.H(float(kx), float(ky), float(kz)))

    def _shifted_k_points(
        self,
        kx: float,
        ky: float,
        kz: float,
        dir: str,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        axis = self._direction_axis(dir)
        step = self._FINITE_DIFFERENCE_STEP
        k_plus = np.array([kx, ky, kz], dtype=float)
        k_minus = k_plus.copy()
        k_plus[axis] += step
        k_minus[axis] -= step
        return k_plus, k_minus

    def _direction_axis(self, dir: str) -> int:
        try:
            axis = self._VALID_DIRECTIONS[dir.lower()]
        except KeyError as exc:
            raise ValueError("dir must be one of 'x', 'y', or 'z'.") from exc
        if axis >= self.dimension:
            raise ValueError(f"Direction '{dir}' is outside dimension {self.dimension}.")
        return axis

    def _validate_matrix(
        self,
        matrix: NDArray[np.complexfloating[Any, Any]] | NDArray[np.floating[Any]],
    ) -> ComplexArray:
        values = np.asarray(matrix, dtype=complex)
        expected_shape = (self.basis_size, self.basis_size)
        if values.shape != expected_shape:
            raise ValueError(
                f"Hamiltonian matrix must have shape {expected_shape}, "
                f"got {values.shape}."
            )
        return values
