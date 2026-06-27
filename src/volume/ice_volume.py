"""Subsurface ice volume estimation with Monte Carlo CI — Pillar C."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class VolumeEstimate:
    mean_m3: float
    ci_lower_m3: float
    ci_upper_m3: float
    mean_water_kg: float
    ice_pixel_count: int
    ice_fraction_mean: float


def estimate_ice_volume(
    ice_prob: np.ndarray,
    pixel_size_m: float,
    depth_m: float = 5.0,
    ice_fraction: float = 0.15,
    threshold: float = 0.7,
    n_samples: int = 1000,
    seed: int = 42,
) -> VolumeEstimate:
    """
    Estimate ice volume in top `depth_m` of regolith for high-probability pixels.

    Monte Carlo perturbs ice fraction (±50%) and depth (±20%) and boundary (±1 px).
    """
    rng = np.random.default_rng(seed)
    mask = ice_prob >= threshold
    pixel_area = pixel_size_m**2
    base_volume = float(mask.sum()) * pixel_area * depth_m * ice_fraction

    samples = []
    for _ in range(n_samples):
        frac = ice_fraction * rng.uniform(0.5, 1.5)
        d = depth_m * rng.uniform(0.8, 1.2)
        # Boundary perturbation via random erosion/dilation proxy
        noise = rng.random(ice_prob.shape) > 0.98
        perturbed = (ice_prob >= threshold) ^ noise
        vol = float(perturbed.sum()) * pixel_area * d * frac
        samples.append(vol)

    samples_arr = np.array(samples)
    ci_low, ci_high = np.percentile(samples_arr, [2.5, 97.5])
    water_density = 1000.0  # kg/m³

    return VolumeEstimate(
        mean_m3=float(np.mean(samples_arr)),
        ci_lower_m3=float(ci_low),
        ci_upper_m3=float(ci_high),
        mean_water_kg=float(np.mean(samples_arr) * water_density),
        ice_pixel_count=int(mask.sum()),
        ice_fraction_mean=ice_fraction,
    )
