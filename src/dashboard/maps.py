"""Mission map and PyDeck 3D terrain builders."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import numpy as np
import plotly.graph_objects as go

from src.dashboard.colormaps import (
    CPR_CMAP,
    DOP_CMAP,
    HILLSHADE_CMAP,
    ICE_CMAP,
    PLOTLY_DARK_LAYOUT,
    PLOTLY_LEGEND_BOTTOM,
    SLOPE_CMAP,
)


def build_mission_map(
    hillshade: np.ndarray,
    ice_prob: Optional[np.ndarray] = None,
    cpr: Optional[np.ndarray] = None,
    dop: Optional[np.ndarray] = None,
    slope: Optional[np.ndarray] = None,
    summary: Optional[Dict[str, Any]] = None,
    show_ice: bool = True,
    show_cpr: bool = False,
    show_dop: bool = False,
    show_slope: bool = False,
    overlay_opacity: float = 0.55,
) -> go.Figure:
    """Unified 2D mission map with toggleable science layers."""
    size = hillshade.shape[0]
    summary = summary or {}
    fig = go.Figure()

    fig.add_trace(go.Heatmap(
        z=hillshade,
        colorscale=HILLSHADE_CMAP,
        showscale=False,
        hoverinfo="skip",
        name="Terrain",
    ))

    if show_ice and ice_prob is not None:
        fig.add_trace(go.Heatmap(
            z=ice_prob,
            colorscale=ICE_CMAP,
            zmin=0, zmax=1,
            opacity=overlay_opacity,
            colorbar=dict(title="Ice Prob", x=1.02, len=0.45, y=0.75),
            name="Ice probability",
        ))

    if show_cpr and cpr is not None:
        fig.add_trace(go.Heatmap(
            z=cpr,
            colorscale=CPR_CMAP,
            zmin=0, zmax=min(3.0, float(np.nanmax(cpr))),
            opacity=overlay_opacity,
            colorbar=dict(title="CPR", x=1.02, len=0.45, y=0.25),
            name="CPR",
        ))

    if show_dop and dop is not None:
        fig.add_trace(go.Heatmap(
            z=dop,
            colorscale=DOP_CMAP,
            zmin=0, zmax=1,
            opacity=overlay_opacity,
            colorbar=dict(title="DOP", x=1.12, len=0.45, y=0.75),
            name="DOP",
        ))

    if show_slope and slope is not None:
        fig.add_trace(go.Heatmap(
            z=slope,
            colorscale=SLOPE_CMAP,
            zmin=0, zmax=25,
            opacity=overlay_opacity,
            colorbar=dict(title="Slope °", x=1.12, len=0.45, y=0.25),
            name="Slope",
        ))

    path = summary.get("traverse_path", [])
    if path:
        rows = [p[0] for p in path]
        cols = [p[1] for p in path]
        fig.add_trace(go.Scatter(
            x=cols, y=rows, mode="lines",
            line=dict(color="#4da6ff", width=3),
            name="Traverse",
        ))

    sites = summary.get("landing_sites", [])
    if sites:
        site_cols = [s["col"] for s in sites]
        site_rows = [s["row"] for s in sites]
        colors = ["#f5c842" if s["rank"] == 1 else "#4da6ff" for s in sites]
        fig.add_trace(go.Scatter(
            x=site_cols, y=site_rows, mode="markers+text",
            marker=dict(size=[16 if s["rank"] == 1 else 11 for s in sites], color=colors, symbol="circle",
                        line=dict(width=1, color="#ffffff")),
            text=[f"L{s['rank']}" for s in sites],
            textposition="top center",
            textfont=dict(color="#ffffff", size=10, family="Rajdhani"),
            name="Landing sites",
        ))

    goal = summary.get("goal_rc")
    if goal:
        fig.add_trace(go.Scatter(
            x=[goal[1]], y=[goal[0]], mode="markers+text",
            marker=dict(size=18, color="#f5c842", symbol="star"),
            text=["ICE TARGET"], textposition="bottom center",
            textfont=dict(color="#f5c842", size=11),
            name="Ice target",
        ))

    crater = summary.get("crater_center_rc")
    if crater:
        fig.add_trace(go.Scatter(
            x=[crater[1]], y=[crater[0]], mode="markers",
            marker=dict(size=10, color="rgba(255,255,255,0.4)", symbol="circle-open", line=dict(width=2)),
            name="Crater center",
        ))

    cpr_th = summary.get("cpr_threshold", 1.0)
    dop_th = summary.get("dop_threshold", 0.13)

    fig.update_layout(
        **PLOTLY_DARK_LAYOUT,
        title=dict(
            text="Mission Map",
            font=dict(family="Orbitron, sans-serif", size=16, color="#ffffff"),
            x=0.02,
            xanchor="left",
        ),
        annotations=[dict(
            text=f"CPR &gt; {cpr_th} · DOP &lt; {dop_th}",
            xref="paper", yref="paper",
            x=0.02, y=1.0,
            showarrow=False,
            font=dict(size=11, color="#9aa8bc", family="Rajdhani, sans-serif"),
            xanchor="left",
        )],
        height=560,
        xaxis=dict(range=[0, size], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(range=[size, 0], scaleanchor="x", scaleratio=1, showgrid=False, zeroline=False, showticklabels=False),
        legend=PLOTLY_LEGEND_BOTTOM,
        dragmode="pan",
    )
    return fig


def build_terrain_deck(
    dem: np.ndarray,
    slope: np.ndarray,
    summary: Dict[str, Any],
    pixel_size_m: float = 10.0,
):
    """PyDeck 3D view with elevation grid and slope-colored path."""
    import pydeck as pdk

    target_size = 48
    step = max(1, dem.shape[0] // target_size)
    dem_ds = dem[::step, ::step]
    h, w = dem_ds.shape

    grid_data = []
    for r in range(h):
        for c in range(w):
            grid_data.append({
                "row": r * step,
                "col": c * step,
                "elevation": float(dem_ds[r, c]),
                "color": [
                    int(80 + dem_ds[r, c] * 2) % 200,
                    int(90 + dem_ds[r, c]) % 180,
                    int(100 + dem_ds[r, c] * 1.5) % 200,
                    180,
                ],
            })

    path = summary.get("traverse_path", [])
    path_segments = []
    if len(path) > 1:
        for i in range(len(path) - 1):
            r0, c0 = path[i]
            r1, c1 = path[i + 1]
            seg_slope = float(slope[min(r0, slope.shape[0] - 1), min(c0, slope.shape[1] - 1)])
            t = min(1.0, seg_slope / 15.0)
            color = [
                int(46 + t * 209),
                int(204 - t * 100),
                int(113 - t * 80),
            ]
            path_segments.append({
                "path": [
                    [c0 * pixel_size_m / 500.0, r0 * pixel_size_m / 500.0, float(dem[min(r0, dem.shape[0]-1), min(c0, dem.shape[1]-1)])],
                    [c1 * pixel_size_m / 500.0, r1 * pixel_size_m / 500.0, float(dem[min(r1, dem.shape[0]-1), min(c1, dem.shape[1]-1)])],
                ],
                "color": color,
            })

    site_data = []
    for s in summary.get("landing_sites", [])[:3]:
        site_data.append({
            "position": [
                s["col"] * pixel_size_m / 500.0,
                s["row"] * pixel_size_m / 500.0,
                float(dem[min(s["row"], dem.shape[0]-1), min(s["col"], dem.shape[1]-1)]) + 2,
            ],
            "rank": s["rank"],
        })

    grid_layer = pdk.Layer(
        "GridCellLayer",
        data=grid_data,
        get_position="[col, row, elevation]",
        cell_size=pixel_size_m * step,
        elevation_scale=1.0,
        get_fill_color="color",
        pickable=True,
        extruded=True,
    )

    layers = [grid_layer]

    if path_segments:
        path_layer = pdk.Layer(
            "PathLayer",
            data=path_segments,
            get_path="path",
            get_color="color",
            get_width=4,
            width_min_pixels=2,
            pickable=True,
        )
        layers.append(path_layer)

    if site_data:
        scatter_layer = pdk.Layer(
            "ScatterplotLayer",
            data=site_data,
            get_position="position",
            get_fill_color=[245, 200, 66, 220],
            get_radius=8,
            pickable=True,
        )
        layers.append(scatter_layer)

    center_r = dem.shape[0] // 2
    center_c = dem.shape[1] // 2
    view = pdk.ViewState(
        latitude=center_r * pixel_size_m / 500.0,
        longitude=center_c * pixel_size_m / 500.0,
        zoom=11,
        pitch=45,
        bearing=-20,
    )

    return pdk.Deck(
        layers=layers,
        initial_view_state=view,
        map_style=None,
        tooltip={"text": "Elev: {elevation}"},
    )
