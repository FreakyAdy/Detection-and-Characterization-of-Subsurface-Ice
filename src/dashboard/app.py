"""Streamlit mission control dashboard for LunarIcePath — BAH 2026 PS 8."""

from __future__ import annotations

import streamlit as st

from src.dashboard.charts import (
    build_3d_surface,
    build_cpr_dop_heatmaps,
    build_cpr_dop_histograms,
    build_landing_bar_chart,
    build_landing_radar_chart,
    build_traverse_animation,
    build_volume_ci_chart,
)
from src.dashboard.data_loader import load_mission_data
from src.dashboard.maps import build_mission_map, build_terrain_deck
from src.dashboard.theme import inject_theme, render_hero, render_kpi_row

DEMO_STEPS = [
    ("1 · Detect", "DFSAR CPR/DOP analysis identifies subsurface ice signatures in the doubly shadowed crater."),
    ("2 · Land", "Ranked landing sites balance terrain safety with proximity to the ice target."),
    ("3 · Traverse", "Optimized rover path avoids steep slopes and maximizes ice proximity."),
    ("4 · Volume", "Monte Carlo estimate quantifies subsurface ice volume with 95% confidence."),
]


def _init_session() -> None:
    if "demo_step" not in st.session_state:
        st.session_state.demo_step = 0
    if "demo_mode" not in st.session_state:
        st.session_state.demo_mode = False


def _render_sidebar(summary: dict, has_rasters: bool) -> dict:
    with st.sidebar:
        st.markdown("### Mission Control")
        st.caption(summary.get("mission_label", "Faustini DSC"))
        st.caption(summary.get("mission_coords", "87.23°S, 83.54°E"))

        st.divider()
        demo_mode = st.toggle("Present to Judges", value=st.session_state.demo_mode, key="demo_toggle")
        st.session_state.demo_mode = demo_mode

        if demo_mode:
            step = st.session_state.demo_step
            for i, (title, desc) in enumerate(DEMO_STEPS):
                active = i == step
                css_class = "demo-step-active" if active else "demo-step"
                st.markdown(
                    f'<div class="{css_class}"><strong>{title}</strong><br><small>{desc}</small></div>',
                    unsafe_allow_html=True,
                )
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("← Prev", use_container_width=True) and step > 0:
                    st.session_state.demo_step -= 1
                    st.rerun()
            with col_b:
                if st.button("Next →", use_container_width=True) and step < len(DEMO_STEPS) - 1:
                    st.session_state.demo_step += 1
                    st.rerun()

        st.divider()
        st.markdown("#### Map Layers")
        show_ice = st.checkbox("Ice probability", value=True)
        show_cpr = st.checkbox("CPR", value=False)
        show_dop = st.checkbox("DOP", value=False)
        show_slope = st.checkbox("Slope", value=False)
        overlay_opacity = st.slider("Overlay opacity", 0.2, 0.9, 0.55, 0.05)

        if demo_mode:
            step = st.session_state.demo_step
            if step == 0:
                show_ice, show_cpr, show_dop = True, True, True
            elif step == 1:
                show_ice = False

        if not has_rasters:
            st.warning("Re-run pipeline for full raster layers.")

        st.divider()
        st.caption("Run: `python scripts/run_demo_pipeline.py`")

    return {
        "show_ice": show_ice,
        "show_cpr": show_cpr,
        "show_dop": show_dop,
        "show_slope": show_slope,
        "overlay_opacity": overlay_opacity,
        "demo_mode": demo_mode,
        "demo_step": st.session_state.demo_step,
    }


def main() -> None:
    st.set_page_config(
        page_title="LunarIcePath",
        layout="wide",
        page_icon="🌙",
        initial_sidebar_state="expanded",
    )
    inject_theme()
    _init_session()

    data = load_mission_data()
    if data is None:
        st.warning("No pipeline output found. Run: `python scripts/run_demo_pipeline.py`")
        st.stop()

    summary = data.summary
    ui = _render_sidebar(summary, data.has_rasters)

    render_hero(
        summary.get("mission_label", "Faustini DSC"),
        summary.get("mission_coords", "87.23°S, 83.54°E"),
    )

    path_len = len(summary.get("traverse_path", []))
    render_kpi_row([
        ("Ice Pixels", f"{summary.get('ice_pixel_count', 0):,}"),
        ("Volume (m³)", f"{summary.get('volume_mean_m3', 0):,.0f}"),
        ("Water (kg)", f"{summary.get('water_kg', 0):,.0f}"),
        ("Traverse (m)", f"{summary.get('traverse_distance_m', path_len * summary.get('pixel_size_m', 10)):.0f}"),
    ])

    tab_mission, tab_science, tab_traverse, tab_volume, tab_3d = st.tabs([
        "Mission Map",
        "Ice Science",
        "Rover Traverse",
        "Volume Estimate",
        "3D Terrain",
    ])

    with tab_mission:
        if data.has_rasters:
            fig = build_mission_map(
                data.hillshade,
                ice_prob=data.ice_prob,
                cpr=data.cpr,
                dop=data.dop,
                slope=data.slope,
                summary=summary,
                show_ice=ui["show_ice"],
                show_cpr=ui["show_cpr"],
                show_dop=ui["show_dop"],
                show_slope=ui["show_slope"],
                overlay_opacity=ui["overlay_opacity"],
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Raster arrays missing. Re-run `python scripts/run_demo_pipeline.py` for the full mission map.")

    with tab_science:
        if data.cpr is not None and data.dop is not None:
            c1, c2 = st.columns(2)
            with c1:
                st.plotly_chart(
                    build_cpr_dop_heatmaps(
                        data.cpr, data.dop,
                        summary.get("cpr_threshold", 1.0),
                        summary.get("dop_threshold", 0.13),
                    ),
                    use_container_width=True,
                )
            with c2:
                st.plotly_chart(
                    build_cpr_dop_histograms(
                        data.cpr, data.dop,
                        summary.get("cpr_threshold", 1.0),
                        summary.get("dop_threshold", 0.13),
                    ),
                    use_container_width=True,
                )
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Mean ice prob", f"{summary.get('mean_ice_prob', 0):.3f}")
            m2.metric("Max CPR", f"{summary.get('max_cpr', 0):.2f}")
            m3.metric("Min DOP (ice)", f"{summary.get('min_dop_ice', 0):.4f}" if summary.get("min_dop_ice") else "—")
            m4.metric("CPR threshold", summary.get("cpr_threshold", 1.0))
        else:
            st.info("CPR/DOP arrays not found. Re-run the pipeline.")

        if ui["demo_mode"] and ui["demo_step"] == 1:
            sites = summary.get("landing_sites", [])
            c1, c2 = st.columns(2)
            with c1:
                st.plotly_chart(build_landing_bar_chart(sites), use_container_width=True)
            with c2:
                st.plotly_chart(build_landing_radar_chart(sites), use_container_width=True)
        elif not ui["demo_mode"]:
            with st.expander("Landing site analysis"):
                sites = summary.get("landing_sites", [])
                c1, c2 = st.columns(2)
                with c1:
                    st.plotly_chart(build_landing_bar_chart(sites), use_container_width=True)
                with c2:
                    st.plotly_chart(build_landing_radar_chart(sites), use_container_width=True)

    with tab_traverse:
        path = summary.get("traverse_path", [])
        t1, t2, t3 = st.columns(3)
        t1.metric("Waypoints", len(path))
        t2.metric("Max slope", f"{summary.get('max_slope_deg', 0):.1f}°")
        t3.metric("Mean ice proximity", f"{summary.get('mean_ice_proximity', 0):.3f}")

        if data.dem is not None and data.slope is not None and path:
            map_anim, elev_anim = build_traverse_animation(
                path, data.dem, data.slope,
                pixel_size_m=summary.get("pixel_size_m", 10.0),
            )
            st.plotly_chart(map_anim, use_container_width=True)
            st.plotly_chart(elev_anim, use_container_width=True)
        else:
            st.info("Traverse animation requires dem.npy and slope.npy from pipeline.")

        if ui["demo_mode"] and ui["demo_step"] == 2:
            st.success("Rover traverse connects landing site to ice target — press **Play** on the animation above.")

    with tab_volume:
        st.plotly_chart(build_volume_ci_chart(summary), use_container_width=True)
        v1, v2, v3, v4 = st.columns(4)
        v1.metric("Mean volume", f"{summary.get('volume_mean_m3', 0):,.0f} m³")
        v2.metric("CI lower", f"{summary.get('volume_ci_low', 0):,.0f} m³")
        v3.metric("CI upper", f"{summary.get('volume_ci_high', 0):,.0f} m³")
        v4.metric("Regolith depth", f"{summary.get('depth_m', 5)} m")

        if ui["demo_mode"] and ui["demo_step"] == 3:
            st.success(
                f"Estimated subsurface ice: **{summary.get('volume_mean_m3', 0):,.0f} m³** "
                f"({summary.get('water_kg', 0):,.0f} kg water equivalent) within top {summary.get('depth_m', 5)} m."
            )

    with tab_3d:
        if data.dem is not None:
            c1, c2 = st.columns([1, 1])
            with c1:
                st.plotly_chart(
                    build_3d_surface(data.dem, summary.get("traverse_path")),
                    use_container_width=True,
                )
            with c2:
                try:
                    deck = build_terrain_deck(
                        data.dem,
                        data.slope if data.slope is not None else data.dem * 0,
                        summary,
                        summary.get("pixel_size_m", 10.0),
                    )
                    st.pydeck_chart(deck, use_container_width=True)
                except Exception as exc:
                    st.caption(f"PyDeck 3D view: {exc}")
        else:
            st.info("DEM not available. Re-run the pipeline.")

    if ui["demo_mode"]:
        step = ui["demo_step"]
        titles = [s[0] for s in DEMO_STEPS]
        st.markdown(
            f"**Judge demo:** Step {step + 1}/4 — {titles[step]}. "
            "Use sidebar **Next →** to advance."
        )


if __name__ == "__main__":
    main()
