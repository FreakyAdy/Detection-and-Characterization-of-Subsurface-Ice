"""Plotly chart builders for LunarIcePath dashboard."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.dashboard.colormaps import (
    CPR_CMAP,
    DOP_CMAP,
    ICE_CMAP,
    PLOTLY_DARK_LAYOUT,
    PLOTLY_LEGEND_BOTTOM,
    SLOPE_CMAP,
)


def _apply_dark(fig: go.Figure, title: str = "", height: int = 400) -> go.Figure:
    fig.update_layout(
        **PLOTLY_DARK_LAYOUT,
        title=dict(text=title, font=dict(family="Orbitron, sans-serif", size=14, color="#ffffff"), x=0.02, xanchor="left"),
        height=height,
    )
    return fig


def build_cpr_dop_heatmaps(
    cpr: np.ndarray,
    dop: np.ndarray,
    cpr_threshold: float = 1.0,
    dop_threshold: float = 0.13,
) -> go.Figure:
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("CPR (Circular Polarization Ratio)", "DOP (Degree of Polarization)"),
        horizontal_spacing=0.08,
    )
    fig.add_trace(
        go.Heatmap(z=cpr, colorscale=CPR_CMAP, zmin=0, zmax=min(3.0, float(np.nanmax(cpr))),
                   colorbar=dict(title="CPR", x=0.45, len=0.9), showscale=True),
        row=1, col=1,
    )
    fig.add_trace(
        go.Heatmap(z=dop, colorscale=DOP_CMAP, zmin=0, zmax=1.0,
                   colorbar=dict(title="DOP", x=1.02, len=0.9), showscale=True),
        row=1, col=2,
    )
    fig.add_annotation(
        text=f"Ice if CPR > {cpr_threshold}", xref="paper", yref="paper",
        x=0.22, y=1.02, showarrow=False, font=dict(color="#4da6ff", size=11),
    )
    fig.add_annotation(
        text=f"Ice if DOP < {dop_threshold}", xref="paper", yref="paper",
        x=0.78, y=1.02, showarrow=False, font=dict(color="#f5c842", size=11),
    )
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False, scaleanchor="x", scaleratio=1)
    return _apply_dark(fig, "DFSAR Polarimetric Products", height=380)


def build_cpr_dop_histograms(
    cpr: np.ndarray,
    dop: np.ndarray,
    cpr_threshold: float = 1.0,
    dop_threshold: float = 0.13,
) -> go.Figure:
    fig = make_subplots(rows=1, cols=2, subplot_titles=("CPR Distribution", "DOP Distribution"))
    fig.add_trace(go.Histogram(x=cpr.ravel(), nbinsx=50, marker_color="#4da6ff", name="CPR"), row=1, col=1)
    fig.add_trace(go.Histogram(x=dop.ravel(), nbinsx=50, marker_color="#7b68ee", name="DOP"), row=1, col=2)
    fig.add_vline(x=cpr_threshold, line_dash="dash", line_color="#4da6ff", row=1, col=1)
    fig.add_vline(x=dop_threshold, line_dash="dash", line_color="#f5c842", row=1, col=2)
    return _apply_dark(fig, "Threshold Analysis", height=320)


def build_landing_bar_chart(sites: List[Dict[str, Any]]) -> go.Figure:
    if not sites:
        fig = go.Figure()
        return _apply_dark(fig, "Landing Sites", height=300)
    ranks = [f"#{s['rank']}" for s in sites]
    scores = [s["score"] for s in sites]
    colors = ["#f5c842" if s["rank"] == 1 else "#4da6ff" for s in sites]
    fig = go.Figure(go.Bar(x=ranks, y=scores, marker_color=colors, text=[f"{s:.3f}" for s in scores], textposition="outside"))
    fig.update_layout(yaxis_title="Safety Score", xaxis_title="Rank")
    return _apply_dark(fig, "Ranked Landing Sites", height=320)


def build_landing_radar_chart(sites: List[Dict[str, Any]]) -> go.Figure:
    if not sites:
        fig = go.Figure()
        return _apply_dark(fig, "Site Comparison", height=350)
    top = sites[0]
    max_slope = max(s["slope_deg"] for s in sites) or 1.0
    max_rough = max(s["roughness"] for s in sites) or 1.0
    categories = ["Score", "Flatness", "Low Roughness"]
    values = [
        top["score"],
        1.0 - top["slope_deg"] / max(max_slope, 8.0),
        1.0 - top["roughness"] / max(max_rough, 1.0),
    ]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill="toself",
        fillcolor="rgba(77,166,255,0.2)",
        line=dict(color="#4da6ff", width=2),
        name=f"Site #{top['rank']}",
    ))
    fig.update_layout(polar=dict(
        radialaxis=dict(visible=True, range=[0, 1], gridcolor="rgba(139,156,179,0.3)"),
        bgcolor="rgba(18,24,38,0.6)",
    ))
    return _apply_dark(fig, f"Landing Site #{top['rank']} Profile", height=350)


def build_volume_ci_chart(summary: Dict[str, Any]) -> go.Figure:
    mean = summary.get("volume_mean_m3", 0)
    lo = summary.get("volume_ci_low", 0)
    hi = summary.get("volume_ci_high", 0)
    water = summary.get("water_kg", 0)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[lo, mean, hi],
        y=["Volume"] * 3,
        mode="markers+lines",
        marker=dict(size=[12, 18, 12], color=["#7b68ee", "#4da6ff", "#7b68ee"]),
        line=dict(color="rgba(77,166,255,0.5)", width=4),
        name="95% CI",
    ))
    fig.add_vrect(x0=lo, x1=hi, fillcolor="rgba(77,166,255,0.15)", line_width=0)
    fig.add_annotation(
        x=mean, y=1.15, yref="paper",
        text=f"Mean: {mean:,.0f} m³<br>Water: {water:,.0f} kg",
        showarrow=False, font=dict(color="#e8edf5", size=12),
        bgcolor="rgba(10,22,40,0.9)", bordercolor="#4da6ff",
    )
    fig.update_layout(xaxis_title="Volume (m³)", showlegend=False)
    return _apply_dark(fig, "Monte Carlo Ice Volume (95% CI)", height=340)


def build_traverse_animation(
    path: List[List[int]],
    dem: np.ndarray,
    slope: np.ndarray,
    pixel_size_m: float = 10.0,
    frame_step: int = 1,
) -> Tuple[go.Figure, go.Figure]:
    """Build animated map + elevation profile figures."""
    if not path:
        empty = go.Figure()
        return _apply_dark(empty), _apply_dark(empty)

    path = path[::frame_step] if frame_step > 1 else path
    rows = [p[0] for p in path]
    cols = [p[1] for p in path]
    size = dem.shape[0]

    elevations = [float(dem[r, c]) for r, c in path]
    distances = [0.0]
    for i in range(1, len(path)):
        dr = (rows[i] - rows[i - 1]) * pixel_size_m
        dc = (cols[i] - cols[i - 1]) * pixel_size_m
        distances.append(distances[-1] + float(np.sqrt(dr**2 + dc**2)))

    hillshade = dem  # use dem for background in animation
    zmin, zmax = float(np.nanmin(hillshade)), float(np.nanmax(hillshade))

    map_fig = go.Figure()
    map_fig.add_trace(go.Heatmap(
        z=hillshade, colorscale="Greys", zmin=zmin, zmax=zmax,
        showscale=False, hoverinfo="skip",
    ))
    map_fig.add_trace(go.Scatter(
        x=cols, y=rows, mode="lines",
        line=dict(color="rgba(77,166,255,0.35)", width=2),
        name="Full path", showlegend=True,
    ))
    map_fig.add_trace(go.Scatter(
        x=[cols[0]], y=[rows[0]], mode="markers+text",
        marker=dict(size=14, color="#4da6ff", symbol="triangle-up"),
        text=["START"], textposition="top center", name="Start",
    ))
    map_fig.add_trace(go.Scatter(
        x=[cols[-1]], y=[rows[-1]], mode="markers+text",
        marker=dict(size=14, color="#f5c842", symbol="star"),
        text=["GOAL"], textposition="top center", name="Goal",
    ))
    map_fig.add_trace(go.Scatter(
        x=[cols[0]], y=[rows[0]], mode="markers+lines",
        marker=dict(size=16, color="#4da6ff", symbol="circle",
                    line=dict(width=2, color="#ffffff")),
        line=dict(color="#4da6ff", width=3),
        name="Rover",
    ))

    frames = []
    for i in range(len(path)):
        trail_x = cols[: i + 1]
        trail_y = rows[: i + 1]
        frames.append(go.Frame(
            name=str(i),
            data=[
                go.Heatmap(z=hillshade, colorscale="Greys", zmin=zmin, zmax=zmax, showscale=False, hoverinfo="skip"),
                go.Scatter(x=cols, y=rows, mode="lines", line=dict(color="rgba(255,107,53,0.4)", width=2)),
                go.Scatter(x=[cols[0]], y=[rows[0]], mode="markers+text",
                           marker=dict(size=14, color="#2ecc71", symbol="triangle-up"), text=["START"]),
                go.Scatter(x=[cols[-1]], y=[rows[-1]], mode="markers+text",
                           marker=dict(size=14, color="#f5c842", symbol="star"), text=["GOAL"]),
                go.Scatter(x=trail_x, y=trail_y, mode="markers+lines",
                           marker=dict(size=16, color="#ff6b35"), line=dict(color="#ff6b35", width=3)),
            ],
        ))

    map_fig.frames = frames
    map_fig.update_layout(
        **PLOTLY_DARK_LAYOUT,
        title="Rover Traverse Animation",
        height=420,
        xaxis=dict(range=[0, size], constrain="domain"),
        yaxis=dict(range=[size, 0], scaleanchor="x", scaleratio=1),
        updatemenus=[{
            "type": "buttons",
            "showactive": False,
            "x": 0.1, "y": 1.12,
            "buttons": [
                {"label": "Play", "method": "animate",
                 "args": [None, {"frame": {"duration": 80, "redraw": True}, "fromcurrent": True}]},
                {"label": "Pause", "method": "animate",
                 "args": [[None], {"frame": {"duration": 0}, "mode": "immediate"}]},
            ],
        }],
        sliders=[{
            "active": 0,
            "steps": [{"args": [[f.name], {"frame": {"duration": 0}, "mode": "immediate"}],
                       "label": str(i), "method": "animate"} for i, f in enumerate(frames)],
            "x": 0.1, "len": 0.8, "y": -0.05,
        }],
    )

    elev_fig = go.Figure()
    elev_fig.add_trace(go.Scatter(
        x=distances, y=elevations, mode="lines",
        fill="tozeroy", fillcolor="rgba(0,212,255,0.15)",
        line=dict(color="#00d4ff", width=2), name="Elevation",
    ))
    elev_fig.add_trace(go.Scatter(
        x=[distances[0]], y=[elevations[0]],
        mode="markers", marker=dict(size=10, color="#ff6b35"), name="Rover",
    ))

    elev_frames = []
    for i in range(len(path)):
        elev_frames.append(go.Frame(
            name=str(i),
            data=[
                go.Scatter(x=distances, y=elevations, mode="lines", fill="tozeroy",
                           fillcolor="rgba(0,212,255,0.15)", line=dict(color="#00d4ff", width=2)),
                go.Scatter(x=[distances[i]], y=[elevations[i]],
                           mode="markers", marker=dict(size=12, color="#ff6b35")),
            ],
        ))
    elev_fig.frames = elev_frames
    elev_fig.update_layout(
        **PLOTLY_DARK_LAYOUT,
        title="Elevation Profile Along Traverse",
        height=280,
        xaxis_title="Distance (m)",
        yaxis_title="Elevation (m)",
    )

    return map_fig, elev_fig


def build_3d_surface(dem: np.ndarray, path: Optional[List[List[int]]] = None) -> go.Figure:
    """Plotly 3D surface of crater DEM with optional path."""
    step = max(1, dem.shape[0] // 64)
    dem_ds = dem[::step, ::step]
    y, x = np.mgrid[0:dem_ds.shape[0], 0:dem_ds.shape[1]]

    fig = go.Figure(data=[go.Surface(
        z=dem_ds, x=x, y=y,
        colorscale="Greys", showscale=False,
        lighting=dict(ambient=0.6, diffuse=0.8),
    )])

    if path:
        path_ds = [(p[0] // step, p[1] // step) for p in path[::max(1, len(path) // 40)]]
        px = [p[1] for p in path_ds]
        py = [p[0] for p in path_ds]
        pz = [float(dem_ds[min(p[0], dem_ds.shape[0] - 1), min(p[1], dem_ds.shape[1] - 1)]) for p in path_ds]
        fig.add_trace(go.Scatter3d(
            x=px, y=py, z=pz, mode="lines+markers",
            line=dict(color="#ff6b35", width=6),
            marker=dict(size=3, color="#f5c842"),
            name="Traverse",
        ))

    fig.update_layout(
        **PLOTLY_DARK_LAYOUT,
        title="3D Crater Terrain",
        height=450,
        scene=dict(
            xaxis_title="Col", yaxis_title="Row", zaxis_title="Elev (m)",
            bgcolor="rgba(10,14,23,0)",
            aspectratio=dict(x=1, y=1, z=0.5),
        ),
    )
    return fig
