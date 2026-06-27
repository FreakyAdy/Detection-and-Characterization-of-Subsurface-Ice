"""Plotly colorscales for lunar science layers."""

from __future__ import annotations

from typing import List, Tuple

ICE_CMAP: List[Tuple[float, str]] = [
    (0.0, "#000000"),
    (0.2, "#0a1628"),
    (0.5, "#2d7dd2"),
    (0.8, "#4da6ff"),
    (1.0, "#cce8ff"),
]

CPR_CMAP: List[Tuple[float, str]] = [
    (0.0, "#1a1a2e"),
    (0.3, "#4a3728"),
    (0.6, "#c45c26"),
    (0.8, "#f5a623"),
    (1.0, "#ffe066"),
]

DOP_CMAP: List[Tuple[float, str]] = [
    (0.0, "#00d4ff"),
    (0.3, "#2d6a8f"),
    (0.6, "#5c4d3c"),
    (1.0, "#8b7355"),
]

SLOPE_CMAP: List[Tuple[float, str]] = [
    (0.0, "#2d5016"),
    (0.3, "#5a8f3c"),
    (0.6, "#c9a227"),
    (1.0, "#c0392b"),
]

HILLSHADE_CMAP: List[Tuple[float, str]] = [
    (0.0, "#1a1a1a"),
    (0.5, "#4a4a4a"),
    (1.0, "#c8c8c8"),
]

PLOTLY_DARK_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(10,22,40,0.55)",
    font=dict(color="#e8edf5", family="Rajdhani, Inter, sans-serif", size=12),
    margin=dict(l=48, r=48, t=72, b=88),
    colorway=["#4da6ff", "#f5c842", "#4da6ff", "#7b68ee", "#2ecc71"],
)

PLOTLY_LEGEND_BOTTOM = dict(
    orientation="h",
    yanchor="top",
    y=-0.14,
    xanchor="center",
    x=0.5,
    bgcolor="rgba(8,12,20,0.9)",
    bordercolor="rgba(77,166,255,0.25)",
    borderwidth=1,
    font=dict(size=11, color="#9aa8bc"),
    itemsizing="constant",
    tracegroupgap=18,
)
