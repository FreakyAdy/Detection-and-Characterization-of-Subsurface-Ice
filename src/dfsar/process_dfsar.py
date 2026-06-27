"""Chandrayaan-2 DFSAR loading and preprocessing utilities."""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import numpy as np
import rasterio
from rasterio.transform import from_origin


def load_band(path: str | Path) -> Tuple[np.ndarray, dict]:
    """Load a single-band GeoTIFF and return array + profile."""
    with rasterio.open(path) as src:
        data = src.read(1).astype(np.float64)
        profile = src.profile.copy()
        nodata = src.nodata
        if nodata is not None:
            data = np.where(data == nodata, np.nan, data)
    return data, profile


def save_geotiff(path: str | Path, data: np.ndarray, profile: dict, dtype: str = "float32") -> None:
    """Write a single-band GeoTIFF."""
    out = profile.copy()
    out.update(dtype=dtype, count=1, nodata=-9999.0)
    arr = np.where(np.isnan(data), -9999.0, data).astype(dtype)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(path, "w", **out) as dst:
        dst.write(arr, 1)


def build_synthetic_dfsar(
    size: int = 128,
    pixel_size_m: float = 10.0,
    seed: int = 42,
) -> Tuple[np.ndarray, np.ndarray, dict]:
    """
    Generate synthetic co/cross-pol backscatter for pipeline testing.

    Simulates an ice-rich crater floor (center) with rough rim (false-positive CPR).
    """
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0:size, 0:size]
    cy, cx = size // 2, size // 2
    dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)

    # Crater floor: low roughness, ice-like volumetric scatter
    floor = dist < size * 0.22
    rim = (dist >= size * 0.22) & (dist < size * 0.32)

    co_pol = np.full((size, size), 0.5)
    cross_pol = np.full((size, size), 0.35)

    # Ice-like: CPR > 1 and DOP < 0.13 (similar co/cross → low DOP, cross > co → high CPR)
    co_pol[floor] = 0.42 + rng.normal(0, 0.02, floor.sum())
    cross_pol[floor] = 0.48 + rng.normal(0, 0.02, floor.sum())

    # Rough rim: high CPR but should be filtered by roughness in fusion
    co_pol[rim] = 0.3 + rng.normal(0, 0.05, rim.sum())
    cross_pol[rim] = 0.5 + rng.normal(0, 0.06, rim.sum())

    co_pol = np.clip(co_pol, 0.05, None)
    cross_pol = np.clip(cross_pol, 0.05, None)

    profile = {
        "driver": "GTiff",
        "height": size,
        "width": size,
        "count": 1,
        "crs": "EPSG:4326",
        "transform": from_origin(0, 0, pixel_size_m, pixel_size_m),
    }
    return co_pol, cross_pol, profile


def preprocess_backscatter(co_pol: np.ndarray, cross_pol: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Apply log-scale normalization and clamp invalid values."""
    co = np.clip(co_pol, 1e-6, None)
    cross = np.clip(cross_pol, 1e-6, None)
    return co, cross
