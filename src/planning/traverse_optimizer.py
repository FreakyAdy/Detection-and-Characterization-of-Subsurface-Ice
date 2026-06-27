"""Multi-criteria rover traverse optimizer — Pillar B."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

import heapq
import numpy as np


@dataclass
class TraverseResult:
    path: List[Tuple[int, int]]
    total_cost: float
    max_slope_deg: float
    mean_ice_proximity: float


def astar_traverse(
    cost: np.ndarray,
    slope: np.ndarray,
    start: Tuple[int, int],
    goal: Tuple[int, int],
    max_slope_deg: float = 15.0,
    distance_weight: float = 1.0,
) -> TraverseResult:
    """
    Weighted A* on 8-connected grid with slope hard constraint.

    Returns empty path if no valid route exists.
    """
    h, w = cost.shape
    sr, sc = start
    gr, gc = goal

    def heuristic(r: int, c: int) -> float:
        return distance_weight * np.hypot(r - gr, c - gc)

    open_set: list = [(heuristic(sr, sc), 0.0, sr, sc)]
    came_from: dict = {}
    g_score = {(sr, sc): 0.0}
    neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    while open_set:
        _, g, r, c = heapq.heappop(open_set)
        if (r, c) == (gr, gc):
            path = _reconstruct(came_from, (r, c))
            return _summarize(path, cost, slope, ice_proxy=None)

        for dr, dc in neighbors:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < h and 0 <= nc < w):
                continue
            if slope[nr, nc] > max_slope_deg:
                continue
            step = cost[nr, nc] * (1.414 if dr and dc else 1.0)
            ng = g + step
            if ng < g_score.get((nr, nc), float("inf")):
                g_score[(nr, nc)] = ng
                came_from[(nr, nc)] = (r, c)
                heapq.heappush(open_set, (ng + heuristic(nr, nc), ng, nr, nc))

    return TraverseResult(path=[], total_cost=float("inf"), max_slope_deg=0.0, mean_ice_proximity=0.0)


def _reconstruct(came_from: dict, current: Tuple[int, int]) -> List[Tuple[int, int]]:
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def _summarize(
    path: List[Tuple[int, int]],
    cost: np.ndarray,
    slope: np.ndarray,
    ice_proxy: np.ndarray | None,
) -> TraverseResult:
    if not path:
        return TraverseResult(path=[], total_cost=float("inf"), max_slope_deg=0.0, mean_ice_proximity=0.0)
    total = sum(cost[r, c] for r, c in path)
    slopes = [slope[r, c] for r, c in path]
    ice_vals = [ice_proxy[r, c] for r, c in path] if ice_proxy is not None else [0.0] * len(path)
    return TraverseResult(
        path=path,
        total_cost=float(total),
        max_slope_deg=float(max(slopes)),
        mean_ice_proximity=float(np.mean(ice_vals)),
    )


def pareto_paths(
    cost: np.ndarray,
    slope: np.ndarray,
    ice_prob: np.ndarray,
    start: Tuple[int, int],
    goal: Tuple[int, int],
    weight_sets: List[dict],
    max_slope_deg: float = 15.0,
) -> List[TraverseResult]:
    """
    Generate Pareto candidate paths by varying cost weights.

    Each weight set reweights ice proximity vs. terrain difficulty.
    """
    results: List[TraverseResult] = []
    for w in weight_sets:
        combined = (
            w.get("slope", 2.0) * (slope / (np.nanmax(slope) + 1e-9))
            + w.get("roughness", 1.5) * 0.5
            - w.get("ice_proximity", 3.0) * ice_prob
        )
        combined = np.clip(combined, 0.01, None)
        res = astar_traverse(combined, slope, start, goal, max_slope_deg, w.get("distance", 1.0))
        if res.path:
            res.mean_ice_proximity = float(np.mean([ice_prob[r, c] for r, c in res.path]))
            results.append(res)
    return results
