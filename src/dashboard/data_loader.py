"""Cached data loading for dashboard."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import numpy as np
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "output"


@dataclass
class MissionData:
    summary: dict
    ice_prob: Optional[np.ndarray] = None
    cpr: Optional[np.ndarray] = None
    dop: Optional[np.ndarray] = None
    dem: Optional[np.ndarray] = None
    slope: Optional[np.ndarray] = None
    roughness: Optional[np.ndarray] = None
    hillshade: Optional[np.ndarray] = None
    has_rasters: bool = False


def _load_npy(name: str) -> Optional[np.ndarray]:
    path = OUTPUT / name
    if path.exists():
        return np.load(path)
    return None


@st.cache_data(show_spinner=False)
def load_mission_data() -> Optional[MissionData]:
    summary_path = OUTPUT / "summary.json"
    if not summary_path.exists():
        return None

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    ice_prob = _load_npy("ice_prob.npy")
    cpr = _load_npy("cpr.npy")
    dop = _load_npy("dop.npy")
    dem = _load_npy("dem.npy")
    slope = _load_npy("slope.npy")
    roughness = _load_npy("roughness.npy")
    hillshade = _load_npy("hillshade.npy")

    has_rasters = ice_prob is not None and hillshade is not None

    return MissionData(
        summary=summary,
        ice_prob=ice_prob,
        cpr=cpr,
        dop=dop,
        dem=dem,
        slope=slope,
        roughness=roughness,
        hillshade=hillshade,
        has_rasters=has_rasters,
    )
