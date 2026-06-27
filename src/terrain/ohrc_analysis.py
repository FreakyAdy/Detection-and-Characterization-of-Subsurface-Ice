"""OHRC terrain analysis — slope, roughness, landing site scoring."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
from scipy.ndimage import generic_filter, uniform_filter


@dataclass
class LandingSite:
    row: int
    col: int
    score: float
    mean_slope_deg: float
    mean_roughness: float


def compute_slope(dem: np.ndarray, pixel_size_m: float) -> np.ndarray:
    """Compute slope in degrees from DEM using gradient."""
    dy, dx = np.gradient(dem, pixel_size_m)
    slope_rad = np.arctan(np.sqrt(dx**2 + dy**2))
    return np.degrees(slope_rad)


def compute_roughness(dem: np.ndarray, window: int = 5) -> np.ndarray:
    """Surface roughness as std dev of elevation in moving window."""

    def _std(arr):
        return np.std(arr)

    return generic_filter(dem, _std, size=window, mode="nearest")


def build_synthetic_dem(size: int = 128, pixel_size_m: float = 10.0, seed: int = 42) -> np.ndarray:
    """Crater-like DEM for demo: depressed center, elevated rim."""
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0:size, 0:size]
    cy, cx = size // 2, size // 2
    dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
    dem = -0.3 * np.exp(-(dist**2) / (2 * (size * 0.2) ** 2))
    dem += 0.15 * np.exp(-((dist - size * 0.28) ** 2) / (2 * (size * 0.04) ** 2))
    dem += rng.normal(0, 0.01, (size, size))
    return dem * 100.0  # scale to ~meters variation


def score_landing_sites(
    slope: np.ndarray,
    roughness: np.ndarray,
    max_slope_deg: float = 8.0,
    grid_step: int = 8,
) -> List[LandingSite]:
    """
    Grid search for flat, low-roughness landing ellipses.

    Higher score = safer landing site.
    """
    sites: List[LandingSite] = []
    h, w = slope.shape
    for r in range(grid_step, h - grid_step, grid_step):
        for c in range(grid_step, w - grid_step, grid_step):
            patch_s = slope[r - 2 : r + 3, c - 2 : c + 3]
            patch_r = roughness[r - 2 : r + 3, c - 2 : c + 3]
            ms = float(np.nanmean(patch_s))
            mr = float(np.nanmean(patch_r))
            if ms > max_slope_deg:
                continue
            score = (max_slope_deg - ms) / max_slope_deg - 0.3 * (mr / (np.nanmax(roughness) + 1e-9))
            sites.append(LandingSite(row=r, col=c, score=score, mean_slope_deg=ms, mean_roughness=mr))
    sites.sort(key=lambda s: s.score, reverse=True)
    return sites


def terrain_cost_surface(
    slope: np.ndarray,
    roughness: np.ndarray,
    ice_prob: np.ndarray,
    weights: dict,
) -> np.ndarray:
    """Combined traversability cost (lower = easier)."""
    s_norm = slope / (np.nanmax(slope) + 1e-9)
    r_norm = roughness / (np.nanmax(roughness) + 1e-9)
    cost = weights.get("slope", 2.0) * s_norm + weights.get("roughness", 1.5) * r_norm
    cost -= weights.get("ice_proximity", 3.0) * ice_prob  # reward ice proximity
    return np.clip(cost, 0.01, None)
