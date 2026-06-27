"""Hillshade computation for lunar DEM visualization."""

from __future__ import annotations

import numpy as np


def compute_hillshade(
    dem: np.ndarray,
    pixel_size_m: float = 10.0,
    azimuth_deg: float = 315.0,
    altitude_deg: float = 45.0,
) -> np.ndarray:
    """Generate shaded relief from DEM using simple hillshade model."""
    dy, dx = np.gradient(dem, pixel_size_m)
    slope = np.pi / 2.0 - np.arctan(np.sqrt(dx**2 + dy**2))
    aspect = np.arctan2(-dx, dy)

    az = np.radians(azimuth_deg)
    alt = np.radians(altitude_deg)

    shaded = (
        np.sin(alt) * np.sin(slope)
        + np.cos(alt) * np.cos(slope) * np.cos(az - aspect)
    )
    shaded = (shaded - shaded.min()) / (shaded.max() - shaded.min() + 1e-9)
    return shaded.astype(np.float32)
