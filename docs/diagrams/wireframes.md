# LunarIcePath Wireframes and Mock Diagrams

These wireframes describe the proposed Streamlit mission-control dashboard for BAH 2026 PS8.

## 1. Main Dashboard

```text
+--------------------------------------------------------------------------------+
| LUNARICEPATH                         Mission | Radar | Terrain | Traverse       |
| Faustini DSC | 87.23 S, 83.54 E                                      PS8 Demo  |
+--------------------------------------------------------------------------------+
| Ice Pixels        | Volume Estimate     | Water Mass         | Traverse Length  |
| 1,245             | 93,200 m3           | 93,200,000 kg      | 1,260 m          |
+--------------------------------------------------------------------------------+
| Sidebar                       | Mission Map                                  |
| ----------------------------- | -------------------------------------------- |
| Present to Judges toggle      | Hillshade / OHRC base layer                  |
| Demo step list                | Ice probability overlay                      |
| Map layer checkboxes          | Landing ellipse markers                      |
| Overlay opacity slider        | Rover traverse line                          |
| Run instruction               | Legend: CPR, DOP, slope, ice probability     |
+--------------------------------------------------------------------------------+
```

## 2. Ice Science Tab

```text
+--------------------------------------------------------------------------------+
| Radar Analysis: DFSAR Polarimetric Products                                     |
+--------------------------------------------------------------------------------+
| CPR Heatmap                         | DOP Heatmap                               |
| Threshold line: CPR > 1             | Threshold line: DOP < 0.13                |
+--------------------------------------------------------------------------------+
| CPR Histogram                       | DOP Histogram                             |
| Candidate pixels highlighted        | Candidate pixels highlighted              |
+--------------------------------------------------------------------------------+
| Mean Ice Probability | Max CPR | Min DOP in Ice Region | Threshold Status      |
+--------------------------------------------------------------------------------+
```

## 3. Landing Site Tab

```text
+--------------------------------------------------------------------------------+
| Landing Sites: Ranked Safety Analysis                                          |
+--------------------------------------------------------------------------------+
| Rank | Site ID | Mean Slope | Roughness | Distance to Target | Final Score      |
| 1    | LZ-01   | 4.2 deg    | Low       | 1.1 km             | 0.91             |
| 2    | LZ-02   | 5.0 deg    | Low       | 1.4 km             | 0.84             |
| 3    | LZ-03   | 6.3 deg    | Medium    | 1.2 km             | 0.76             |
+--------------------------------------------------------------------------------+
| Bar chart: score by landing site     | Radar chart: safety/science trade-off    |
+--------------------------------------------------------------------------------+
```

## 4. Rover Traverse Tab

```text
+--------------------------------------------------------------------------------+
| Rover Path: Optimized Traverse                                                  |
+--------------------------------------------------------------------------------+
| Waypoints               | Max Slope Along Path        | Mean Ice Proximity      |
+--------------------------------------------------------------------------------+
| Animated map of rover path from selected landing site to ice-rich target        |
| Elevation profile below map: distance vs terrain height                         |
| Constraint badges: slope <= 15 deg, roughness accepted, path connected          |
+--------------------------------------------------------------------------------+
```

## 5. Volume Tab

```text
+--------------------------------------------------------------------------------+
| Resource Estimate: Subsurface Ice Volume                                       |
+--------------------------------------------------------------------------------+
| Monte Carlo Distribution Chart                                                  |
| Mean volume, lower 95 percent CI, upper 95 percent CI, assumed depth            |
+--------------------------------------------------------------------------------+
| Interpretation panel: volume is planning-grade, not a direct mining claim       |
+--------------------------------------------------------------------------------+
```

## 6. 3D Terrain Tab

```text
+--------------------------------------------------------------------------------+
| Terrain Model: 3D Crater Visualization                                          |
+--------------------------------------------------------------------------------+
| 3D surface plot with crater morphology        | PyDeck terrain/hazard view       |
| Rover path draped over terrain                | Landing site and target markers  |
+--------------------------------------------------------------------------------+
```
