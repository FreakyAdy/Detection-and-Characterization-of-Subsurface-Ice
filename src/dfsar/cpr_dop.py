"""CPR/DOP computation and ice probability fusion — Pillar A."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np


@dataclass
class IceDetectionConfig:
    cpr_threshold: float = 1.0
    dop_threshold: float = 0.13
    fusion_weight_l_band: float = 0.5
    morphology_boost: float = 0.15
    morphology_penalty: float = 0.25


def compute_cpr(co_pol: np.ndarray, cross_pol: np.ndarray) -> np.ndarray:
    """Circular Polarization Ratio = cross-pol / co-pol."""
    return cross_pol / np.clip(co_pol, 1e-9, None)


def compute_dop(co_pol: np.ndarray, cross_pol: np.ndarray) -> np.ndarray:
    """
    Degree of Polarization (simplified Stokes-based proxy).

    DOP = (co - cross) / (co + cross) mapped to [0, 1] depolarization scale.
    Lower values indicate stronger volumetric depolarization (ice-like).
    """
    total = co_pol + cross_pol
    dop = np.abs(co_pol - cross_pol) / np.clip(total, 1e-9, None)
    return np.clip(dop, 0.0, 1.0)


def binary_ice_mask(cpr: np.ndarray, dop: np.ndarray, cfg: IceDetectionConfig) -> np.ndarray:
    """Apply ISRO/PRL 2026 criterion: CPR > 1 AND DOP < 0.13."""
    return (cpr > cfg.cpr_threshold) & (dop < cfg.dop_threshold)


def fuse_l_s_bands(
    cpr_l: np.ndarray,
    dop_l: np.ndarray,
    cpr_s: np.ndarray,
    dop_s: np.ndarray,
    cfg: IceDetectionConfig,
) -> np.ndarray:
    """Fuse L- and S-band ice probability maps."""
    w = cfg.fusion_weight_l_band
    prob_l = _band_probability(cpr_l, dop_l, cfg)
    prob_s = _band_probability(cpr_s, dop_s, cfg)
    return np.clip(w * prob_l + (1 - w) * prob_s, 0.0, 1.0)


def _band_probability(cpr: np.ndarray, dop: np.ndarray, cfg: IceDetectionConfig) -> np.ndarray:
    """Convert CPR/DOP to soft probability in [0, 1]."""
    cpr_score = np.clip((cpr - cfg.cpr_threshold) / 0.5 + 0.5, 0.0, 1.0)
    dop_score = np.clip((cfg.dop_threshold - dop) / cfg.dop_threshold, 0.0, 1.0)
    return np.where(
        (cpr > cfg.cpr_threshold) & (dop < cfg.dop_threshold),
        np.maximum(cpr_score * dop_score, 0.75),
        cpr_score * dop_score * 0.3,
    )


def apply_morphology_fusion(
    ice_prob: np.ndarray,
    roughness: np.ndarray,
    cfg: IceDetectionConfig,
) -> np.ndarray:
    """
    Adjust ice probability using OHRC-derived roughness.

    Low roughness (smooth floor) → boost; high roughness (boulder field) → penalty.
    """
    rough_norm = roughness / (np.nanmax(roughness) + 1e-9)
    adjusted = ice_prob.copy()
    smooth = rough_norm < 0.3
    rough = rough_norm > 0.7
    adjusted[smooth] = np.clip(adjusted[smooth] + cfg.morphology_boost, 0.0, 1.0)
    adjusted[rough] = np.clip(adjusted[rough] - cfg.morphology_penalty, 0.0, 1.0)
    return adjusted


def run_ice_detection(
    co_pol: np.ndarray,
    cross_pol: np.ndarray,
    roughness: np.ndarray | None = None,
    cfg: IceDetectionConfig | None = None,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Full Pillar A pipeline: CPR, DOP, fused ice probability."""
    cfg = cfg or IceDetectionConfig()
    cpr = compute_cpr(co_pol, cross_pol)
    dop = compute_dop(co_pol, cross_pol)
    ice_prob = _band_probability(cpr, dop, cfg)
    if roughness is not None:
        ice_prob = apply_morphology_fusion(ice_prob, roughness, cfg)
    return cpr, dop, ice_prob
