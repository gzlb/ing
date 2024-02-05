from typing import Union
from scipy.special import ive
from dataclasses import dataclass
import numpy as np

from ing.fit.models import Model

@dataclass
class CIR(Model):
    """
    Model for CIR (cox-ingersol-ross)
    Parameters:  [kappa, mu, sigma]

    dX(t) = mu(X,t)*dt + sigma(X,t)*dW_t

    where:
        mu(X,t)    = kappa * (mu - X)
        sigma(X,t) = sigma * sqrt(X)         (sigma>0)

    """

    def __init__(self):
        super().__init__(has_exact_density=True)

    def drift(self, x: Union[float, np.ndarray], t: float) -> Union[float, np.ndarray]:
        return self._params[0] * (self._params[1] - x)

    def diffusion(self, x: Union[float, np.ndarray], t: float) -> Union[float, np.ndarray]:
        return self._params[2] * np.sqrt(x)

    def exact_density(self, x0: float, xt: float, t0: float, dt: float) -> float:
        kappa, mu, sigma = self._params
        theta1 = kappa * mu
        theta2 = kappa
        theta3 = sigma

        et = np.exp(-theta2 * dt)
        c = 2 * theta2 / (theta3 ** 2 * (1 - et))
        u = c * x0 * et
        v = c * xt
        q = 2 * theta1 / theta3 ** 2 - 1

        z = 2 * np.sqrt(u * v)  # Note: we apply exponential scaling trick
        p = c * np.exp(-(u + v) + np.abs(z)) * (v / u) ** (q / 2)

        z = 2 * np.sqrt(u * v)
        p *= ive(q, z)
        return p

    def _set_is_positive(self, params: np.ndarray) -> bool:
        """ CIR is always non-negative """
        return True

    # =======================
    # (Optional) Overrides for numerical derivatives to improve performance
    # =======================

    def drift_t(self, x: Union[float, np.ndarray], t: float) -> Union[float, np.ndarray]:
        return 0.0