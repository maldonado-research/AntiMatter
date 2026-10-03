"""Linear, detailed-balance reaction comparator; all numerical inputs dimensionless.

This does not specify a particle model or a candidate baryogenesis source.
S[:, r] is the change in species number per forward reaction event.
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np


def null_space(matrix):
    matrix = np.asarray(matrix, dtype=float)
    _, singular, vh = np.linalg.svd(matrix, full_matrices=True)
    scale = singular.max(initial=0.0)
    rank = int(np.count_nonzero(singular > 64 * np.finfo(float).eps * scale))
    return vh[rank:].T


@dataclass
class Network:
    S: np.ndarray
    C: np.ndarray
    rates: np.ndarray

    def __post_init__(self):
        self.S = np.asarray(self.S, dtype=float)
        self.C = np.asarray(self.C, dtype=float)
        self.rates = np.asarray(self.rates, dtype=float)
        if self.S.ndim != 2:
            raise ValueError('S must be a matrix')
        n, reactions = self.S.shape
        if self.C.shape != (n, n) or self.rates.shape != (reactions,):
            raise ValueError('inconsistent dimensions')
        if not all(np.isfinite(value).all() for value in [self.S, self.C, self.rates]):
            raise ValueError('non-finite input')
        if not np.allclose(self.C, self.C.T, atol=1e-14, rtol=1e-14):
            raise ValueError('C must be symmetric')
        if np.any(self.rates < 0):
            raise ValueError('negative reaction rate')
        eigen, rotation = np.linalg.eigh(self.C)
        if np.any(eigen <= 0):
            raise ValueError('C must be positive definite')
        self.C_half = (rotation * np.sqrt(eigen)) @ rotation.T
        self.C_mhalf = (rotation / np.sqrt(eigen)) @ rotation.T
        self.C_inv = (rotation / eigen) @ rotation.T
        self.K = (self.S * self.rates) @ self.S.T
        self.W = self.K @ self.C_inv
        self.A = self.C_mhalf @ self.K @ self.C_mhalf
        self.eigenvalues, self.rotation = np.linalg.eigh(self.A)
        tolerance = 64 * np.finfo(float).eps * np.abs(self.eigenvalues).max(initial=0)
        if self.eigenvalues.min(initial=0) < -tolerance:
            raise ValueError('non-positive relaxation operator')
        self.positive = self.eigenvalues > tolerance
        self.eigenvalues = np.where(self.positive, self.eigenvalues, 0)

    def chemical_potential(self, x):
        return self.C_inv @ np.asarray(x, dtype=float)

    def progress(self, x, bias):
        return self.rates * (np.asarray(bias) - self.S.T @ self.chemical_potential(x))

    def derivative(self, x, bias):
        return self.S @ self.progress(x, bias)

    def charges(self):
        return null_space(self.S[:, self.rates > 0].T)

    def compatibility(self, bias):
        """Residual for all active reaction affinities to vanish simultaneously."""
        active = self.rates > 0
        bias = np.asarray(bias, dtype=float)
        chemical = np.linalg.lstsq(self.S[:, active].T, bias[active], rcond=None)[0]
        residual = bias[active] - self.S[:, active].T @ chemical
        return {'compatible': bool(np.linalg.norm(residual) < 2e-12),
                'residual_norm': float(np.linalg.norm(residual)),
                'residual': residual.tolist()}

    def propagate(self, x, bias, duration):
        """Exact constant-segment response; no inversion of a singular W."""
        if not np.isfinite(duration) or duration < 0:
            raise ValueError('duration must be finite and nonnegative')
        x, bias = np.asarray(x, dtype=float), np.asarray(bias, dtype=float)
        if x.shape != (self.S.shape[0],) or bias.shape != (self.S.shape[1],):
            raise ValueError('state/source dimension mismatch')
        if not np.isfinite(x).all() or not np.isfinite(bias).all():
            raise ValueError('non-finite state or source')
        z = self.rotation.T @ self.C_mhalf @ x
        source = self.rotation.T @ self.C_mhalf @ (self.S @ (self.rates * bias))
        damping = np.exp(-self.eigenvalues * duration)
        integral = np.full_like(damping, duration)
        integral[self.positive] = (-np.expm1(-self.eigenvalues[self.positive] * duration)
                                  / self.eigenvalues[self.positive])
        return self.C_half @ self.rotation @ (damping * z + integral * source)

    def stationary(self, bias, initial=None):
        initial = np.zeros(self.S.shape[0]) if initial is None else np.asarray(initial)
        z_initial = self.rotation.T @ self.C_mhalf @ initial
        source = self.rotation.T @ self.C_mhalf @ (self.S @ (self.rates * bias))
        z = np.where(self.positive, 0, z_initial)
        z[self.positive] = source[self.positive] / self.eigenvalues[self.positive]
        return self.C_half @ self.rotation @ z


def rk4(network, initial, bias, duration, steps):
    """Ordinary-coordinate integration, independent of spectral propagation."""
    x = np.asarray(initial, dtype=float).copy()
    h = duration / steps
    for _ in range(steps):
        k1 = network.derivative(x, bias)
        k2 = network.derivative(x + h*k1/2, bias)
        k3 = network.derivative(x + h*k2/2, bias)
        k4 = network.derivative(x + h*k3, bias)
        x += h*(k1 + 2*k2 + 2*k3 + k4)/6
    return x


S = np.array([[-1., 0., 1.], [1., -1., 0.], [0., 1., -1.]])
C = np.diag([1., 2., 3.])
Q = np.ones(3)
D = np.array([1., 0., 0.])
AMPLITUDE = 0.01
BIAS = S.T @ D * AMPLITUDE
