"""End-to-end demo pipeline — synthetic data through all three pillars."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.dfsar.cpr_dop import IceDetectionConfig, run_ice_detection
from src.dfsar.process_dfsar import build_synthetic_dfsar, save_geotiff
from src.planning.traverse_optimizer import astar_traverse
from src.terrain.ohrc_analysis import (
    build_synthetic_dem,
    compute_roughness,
    compute_slope,
    score_landing_sites,
    terrain_cost_surface,
)
from src.dashboard.hillshade import compute_hillshade
from src.volume.ice_volume import estimate_ice_volume


def load_config() -> dict:
    with open(ROOT / "config" / "default.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main() -> None:
    cfg = load_config()
    demo = cfg["demo"]
    size = demo["grid_size"]
    px = demo["pixel_size_m"]
    seed = demo["seed"]

    out_dir = ROOT / "output"
    data_dir = ROOT / "data" / "demo"
    data_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=== LunarIcePath demo pipeline ===")

    # Synthetic DFSAR
    co_pol, cross_pol, profile = build_synthetic_dfsar(size, px, seed)
    save_geotiff(data_dir / "co_pol.tif", co_pol, profile)
    save_geotiff(data_dir / "cross_pol.tif", cross_pol, profile)

    # Synthetic OHRC DEM
    dem = build_synthetic_dem(size, px, seed)
    save_geotiff(data_dir / "dem.tif", dem, profile)
    slope = compute_slope(dem, px)
    roughness = compute_roughness(dem, cfg["terrain"]["roughness_window"])

    # Pillar A
    ice_cfg = IceDetectionConfig(
        cpr_threshold=cfg["ice_detection"]["cpr_threshold"],
        dop_threshold=cfg["ice_detection"]["dop_threshold"],
        morphology_boost=cfg["ice_detection"]["morphology_boost"],
        morphology_penalty=cfg["ice_detection"]["morphology_penalty"],
    )
    cpr, dop, ice_prob = run_ice_detection(co_pol, cross_pol, roughness, ice_cfg)
    save_geotiff(out_dir / "cpr.tif", cpr, profile)
    save_geotiff(out_dir / "dop.tif", dop, profile)
    save_geotiff(out_dir / "ice_prob.tif", ice_prob, profile)
    hillshade = compute_hillshade(dem, px)

    np.save(out_dir / "ice_prob.npy", ice_prob)
    np.save(out_dir / "cpr.npy", cpr)
    np.save(out_dir / "dop.npy", dop)
    np.save(out_dir / "dem.npy", dem)
    np.save(out_dir / "slope.npy", slope)
    np.save(out_dir / "roughness.npy", roughness)
    np.save(out_dir / "hillshade.npy", hillshade)

    # Landing sites
    sites = score_landing_sites(slope, roughness, cfg["terrain"]["max_landing_slope_deg"])
    top_sites = [
        {"rank": i + 1, "row": s.row, "col": s.col, "score": round(s.score, 3),
         "slope_deg": round(s.mean_slope_deg, 2), "roughness": round(s.mean_roughness, 4)}
        for i, s in enumerate(sites[:5])
    ]

    # Pillar B — traverse from best landing site to ice centroid
    ice_mask = ice_prob >= cfg["volume"]["ice_probability_threshold"]
    if ice_mask.any():
        ice_coords = np.argwhere(ice_mask)
        goal = tuple(ice_coords[len(ice_coords) // 2])
    else:
        goal = (size // 2, size // 2)

    start = (sites[0].row, sites[0].col) if sites else (10, 10)
    cost = terrain_cost_surface(slope, roughness, ice_prob, cfg["traverse"]["weights"])
    traverse = astar_traverse(
        cost, slope, start, goal,
        max_slope_deg=cfg["terrain"]["max_traverse_slope_deg"],
        distance_weight=cfg["traverse"]["weights"].get("distance", 1.0),
    )
    if traverse.path:
        traverse.mean_ice_proximity = float(np.mean([ice_prob[r, c] for r, c in traverse.path]))

    # Pillar C — volume
    vol = estimate_ice_volume(
        ice_prob, px,
        depth_m=cfg["volume"]["regolith_depth_m"],
        ice_fraction=cfg["volume"]["default_ice_fraction"],
        threshold=cfg["volume"]["ice_probability_threshold"],
        n_samples=cfg["volume"]["monte_carlo_samples"],
        seed=seed,
    )

    crater_center = (size // 2, size // 2)
    traverse_dist_m = (
        len(traverse.path) * px * 0.707 if traverse.path else 0.0
    )

    summary = {
        "mission_label": "Faustini DSC",
        "mission_coords": "87.23°S, 83.54°E",
        "grid_size": size,
        "cpr_threshold": ice_cfg.cpr_threshold,
        "dop_threshold": ice_cfg.dop_threshold,
        "mean_ice_prob": float(np.nanmean(ice_prob)),
        "max_cpr": float(np.nanmax(cpr)),
        "min_dop_ice": float(np.nanmin(dop[ice_mask])) if ice_mask.any() else None,
        "ice_pixel_count": vol.ice_pixel_count,
        "landing_sites": top_sites,
        "traverse_path": traverse.path,
        "traverse_cost": traverse.total_cost,
        "traverse_distance_m": round(traverse_dist_m, 1),
        "max_slope_deg": traverse.max_slope_deg,
        "mean_ice_proximity": traverse.mean_ice_proximity,
        "start_rc": [int(start[0]), int(start[1])],
        "goal_rc": [int(goal[0]), int(goal[1])],
        "crater_center_rc": [int(crater_center[0]), int(crater_center[1])],
        "volume_mean_m3": vol.mean_m3,
        "volume_ci_low": vol.ci_lower_m3,
        "volume_ci_high": vol.ci_upper_m3,
        "water_kg": vol.mean_water_kg,
        "depth_m": cfg["volume"]["regolith_depth_m"],
        "ice_fraction": cfg["volume"]["default_ice_fraction"],
        "pixel_size_m": px,
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"  Ice pixels: {vol.ice_pixel_count}")
    print(f"  Volume: {vol.mean_m3:,.0f} m³ [{vol.ci_lower_m3:,.0f} – {vol.ci_upper_m3:,.0f}]")
    print(f"  Traverse waypoints: {len(traverse.path)}")
    print(f"  Output: {out_dir}")
    print("  Dashboard: python -m streamlit run src/dashboard/app.py")


if __name__ == "__main__":
    main()
