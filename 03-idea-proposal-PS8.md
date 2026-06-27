# BAH 2026 Idea Submission — Problem Statement 8

## LunarIcePath: Integrated Subsurface Ice Detection, Landing Site Selection, and Rover Traverse Planning for Doubly Shadowed Craters

**Hackathon:** Bharatiya Antariksh Hackathon 2026 (ISRO × Hack2Skill)  
**Problem Statement:** PS 8 — Detection and Characterization of Subsurface Ice in Lunar South Polar Regions Using Chandrayaan-2 Radar and Imagery Data  
**Team name:** _[Fill in]_  
**Submission deadline:** July 1, 2026

---

## 1. Executive summary

We propose **LunarIcePath**, an end-to-end exploration-planning framework for the lunar south polar region that goes beyond ice detection maps to deliver **mission-ready outputs**: validated subsurface ice probability maps, ranked landing site candidates, an optimized rover traverse path, and quantitative ice volume estimates with uncertainty bounds.

Our approach integrates Chandrayaan-2 **DFSAR** polarimetric radar analysis with **OHRC** high-resolution terrain characterization and multi-objective path optimization under terrain hazard and solar illumination constraints. The system directly supports ISRO's lunar exploration priorities: in-situ resource utilization (ISRU), safe landing site selection, and robotic traverse planning in permanently shadowed regions (PSRs).

---

## 2. Problem understanding

### 2.1 Scientific context

Water ice in lunar PSRs, especially within **doubly shadowed craters** (craters inside PSRs), represents one of the highest-priority targets for future ISRO and international lunar missions. Chandrayaan-2's DFSAR is the first fully polarimetric SAR deployed for lunar science, enabling L- and S-band subsurface probing.

Recent ISRO/PRL research ([ISRO announcement](https://www.isro.gov.in/ISRO_EN/Chandrayaan2_Dual_Frequency_Synthetic_Aperture_Radar.html); [npj Space Exploration, 2026](https://www.nature.com/articles/s44453-026-00038-9)) established a refined diagnostic criterion:

- **CPR (Circular Polarization Ratio) > 1** — indicates volumetric scattering
- **DOP (Degree of Polarization) < 0.13** — distinguishes ice from rough rocky terrain

A 1.1 km crater within **Faustini crater** shows particularly strong evidence, supported by lobate-rim morphology suggestive of ice-rich subsurface penetration.

### 2.2 Hackathon gap we address

Most teams will produce standalone CPR heatmaps. **LunarIcePath** closes the loop from detection to **actionable exploration**:

| Standard approach | LunarIcePath |
|-------------------|--------------|
| Binary ice/non-ice map | Probabilistic ice map + morphology validation |
| No landing analysis | Ranked landing ellipses with safety scoring |
| Shortest-path traverse | Multi-criteria Pareto-optimal rover path |
| Point volume estimate | Volume with Monte Carlo confidence intervals |

---

## 3. Proposed methodology — three pillars

### Pillar A: Robust subsurface ice detection

**Objective:** Generate high-confidence ice probability maps for the target doubly shadowed crater using DFSAR polarimetry with false-positive mitigation.

**Method:**

1. **Radiometric calibration & polarimetric decomposition** of DFSAR L- and S-band data using MIDAS ([VEDAS download](https://vedas.sac.gov.in/vcms/en/download.html)) and/or Python/GDAL pipeline (see `src/dfsar/`).
2. Compute **CPR** and **DOP** per pixel; flag candidates meeting CPR > 1 AND DOP < 0.13.
3. **Cross-validate with OHRC morphology:**
   - Lobate-rim and smooth floor textures → increase ice confidence
   - Boulder fields and high roughness → decrease confidence (known CPR false-positive source)
4. **Fuse L- and S-band** signatures — agreement across frequencies increases posterior ice probability.
5. Output: **ice probability raster** (0–1) with uncertainty layer, not binary mask.

**Innovation:** Bayesian fusion of radar polarimetry + morphological priors reduces rocky-terrain false positives that plague CPR-only methods.

---

### Pillar B: Multi-criteria traverse optimizer

**Objective:** Design a safe, scientifically optimal rover traverse from landing site to the ice-rich doubly shadowed crater floor.

**Method:**

1. **Terrain cost surface** from OHRC DEM derivatives:
   - Slope (reject > 15° for rover mobility baseline)
   - Surface roughness (standard deviation of elevation in 3×3 window)
   - Boulder hazard density (OHRC texture / manual annotation if needed)
2. **Solar illumination model** — compute sun-exposure windows along candidate paths (critical for south-pole operations outside PSR).
3. **Multi-objective optimization** using weighted A* or RRT*:
   - Minimize: traversal distance, cumulative slope, roughness exposure
   - Maximize: ice proximity, sun-exposure time at waypoints
   - Hard constraints: no-go zones (slopes > threshold, crater rims)
4. Output: **Pareto front of 3–5 candidate paths** with trade-off visualization (science vs. safety vs. energy).

**Innovation:** Explicit Pareto trade-off dashboard — planners choose path based on mission priority, not a single black-box optimum.

---

### Pillar C: Ice volume with confidence intervals

**Objective:** Estimate subsurface ice volume within the top ~5 m of regolith at the target crater with quantified uncertainty.

**Method:**

1. Define ice-bearing region from Pillar A probability map (threshold ≥ 0.7 or mentor-specified cutoff).
2. Apply **dielectric mixing model** (e.g., Maxwell-Garnett or Birchak et al.) relating CPR/DOP to ice fraction in regolith.
3. Assume depth distribution: uniform ice fraction to 5 m (sensitivity analysis for 2–5 m range).
4. **Monte Carlo simulation** (N = 1000): perturb dielectric assumptions, CPR/DOP measurement noise, and region boundary → volume distribution.
5. Output: **mean volume ± 95% CI** in m³ and equivalent water mass.

**Innovation:** First student hackathon deliverable to pair ISRO's new CPR/DOP criterion with formal uncertainty propagation for mission planning.

---

## 4. Landing site selection

Between ice target and safe approach corridor, we will:

1. Identify 5–10 candidate landing ellipses (500 m radius) within 2 km of target crater rim.
2. Score each site on: mean slope, roughness, distance to traverse start, Earth visibility, solar availability.
3. Rank and present top 3 with justification maps.

---

## 5. Expected deliverables

### Idea phase (Jul 1, 2026)

- This written proposal + architecture diagram
- Preliminary literature review ([`04-research-brief-DFSAR.md`](04-research-brief-DFSAR.md))

### Grand finale (30 hours, if shortlisted)

| Deliverable | Format |
|-------------|--------|
| Ice probability map (CPR/DOP + fusion) | GeoTIFF + legend |
| Landing site ranking | Table + map overlay |
| Optimized rover traverse | GeoJSON path + 3D animation |
| Ice volume estimate | Report with CI |
| Interactive dashboard | Streamlit + PyDeck/Cesium (see `src/dashboard/`) |
| Methodology report | ≤ 3 pages |

---

## 6. System architecture

```
┌─────────────────┐     ┌─────────────────┐
│  Chandrayaan-2  │     │  Chandrayaan-2  │
│     DFSAR       │     │      OHRC       │
│  (L + S band)   │     │  (Hi-res image) │
└────────┬────────┘     └────────┬────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│ Pillar A:       │     │ Terrain layer:  │
│ CPR/DOP + fusion│     │ slope, roughness│
│ + morphology    │     │ boulder map     │
└────────┬────────┘     └────────┬────────┘
         │                       │
         └───────────┬───────────┘
                     ▼
         ┌───────────────────────┐
         │  Landing site ranker  │
         └───────────┬───────────┘
                     ▼
         ┌───────────────────────┐
         │ Pillar B: Traverse    │
         │ optimizer (Pareto)    │
         └───────────┬───────────┘
                     ▼
         ┌───────────────────────┐
         │ Pillar C: Volume + CI │
         └───────────┬───────────┘
                     ▼
         ┌───────────────────────┐
         │  Streamlit dashboard  │
         └───────────────────────┘
```

---

## 7. Datasets

| Dataset | Source | Use |
|---------|--------|-----|
| DFSAR L/S-band polarimetric | Provided by ISRO (Faustini DSC) | CPR, DOP, ice detection |
| OHRC imagery | Provided by ISRO | Morphology, roughness, landing sites |
| Illumination model | Derived from DEM + ephemeris (SPICE/Skyfield) | Solar constraints |
| Published PRL criteria | [ISRO DFSAR ice paper](https://www.nature.com/articles/s44453-026-00038-9) | Validation baseline |

---

## 8. Tools and technologies

| Component | Tools |
|-----------|-------|
| Radar processing | MIDAS v4.2.4, Python, GDAL, Rasterio, NumPy |
| Terrain analysis | QGIS, scikit-image, SciPy |
| Path planning | NetworkX, custom A*/RRT*, OR-Tools (optional) |
| Volume modeling | NumPy, Monte Carlo |
| Dashboard | Streamlit, PyDeck, Plotly |
| Ephemeris | Skyfield or SPICE |

Code scaffold: [`src/`](src/) in this repository folder.

---

## 9. Team roles (30-hour parallel workflow)

| Member | Primary responsibility | Skills leveraged |
|--------|------------------------|------------------|
| **Member 1** | DFSAR ingestion, MIDAS/GDAL pipeline, CPR/DOP maps, L/S fusion | Remote sensing, radar polarimetry |
| **Member 2** | OHRC terrain: DEM, slope, roughness, landing ellipse scoring | Planetary geology, GIS |
| **Member 3** | Traverse optimizer, illumination model, path validation | Algorithms, physics, time-series |
| **Member 4** | Dashboard integration, demo narrative, report | Full-stack, visualization |

**Overlap:** All members cross-validate ice map ↔ terrain consistency during integration hour 20–24.

---

## 10. Validation plan

| Component | Metric | Target |
|-----------|--------|--------|
| Ice detection | Agreement with published CPR>1 & DOP<0.13 pixels | > 85% overlap |
| Ice detection | Morphology consistency (lobate-rim regions) | Qualitative ISRO mentor review |
| Landing sites | Mean slope at top-3 sites | < 8° |
| Traverse | Max segment slope | < 15° |
| Traverse | Path connectivity | 100% (no gaps) |
| Volume | CI width / mean ratio | Report honestly; prioritize methodology |
| Dashboard | End-to-end demo time | < 5 minutes |

---

## 11. Timeline

| Phase | Dates | Activities |
|-------|-------|------------|
| Registration + idea | By Jul 1 | Submit this proposal |
| Explainer sessions | Jun 15–16 | Clarify eval weights; refine scope |
| Pre-build (optional) | Jul 1–20 | MIDAS familiarization; scaffold testing |
| Shortlist | Jul 20 | If selected, finalize data prep |
| Induction | Jul 21 | Mentor sync |
| **Grand finale** | **Aug 6–7** | **30-hour build + demo** |

---

## 12. National relevance and ISRO alignment

- Supports **Chandrayaan programme** science exploitation and future south-pole lander/rover missions
- Enables **ISRU** site selection for water extraction
- Demonstrates indigenous toolchain use (**MIDAS**, ISRO-provided DFSAR/OHRC)
- Aligns with India's space exploration roadmap and Atmanirbhar Bharat in planetary data analysis

---

## 13. Risks and mitigations

| Risk | Mitigation |
|------|------------|
| CPR false positives from rough terrain | Morphology cross-check + L/S band fusion (Pillar A) |
| No DEM from OHRC stereo in 30h | Use slope proxy from radar + OHRC shadow analysis |
| MIDAS learning curve | Pre-build Python CPR/DOP pipeline as fallback (`src/dfsar/`) |
| Illumination model complexity | Use simplified sun-elevation at discrete time steps |
| Volume uncertainty dominates | Report CI transparently; emphasize methodology over point estimate |

---

## 14. References

1. ISRO (2026). Chandrayaan-2 DFSAR Observations Reveal Subsurface Ice in Lunar South Polar Regions. https://www.isro.gov.in/ISRO_EN/Chandrayaan2_Dual_Frequency_Synthetic_Aperture_Radar.html
2. PRL Team (2026). Subsurface ice in doubly shadowed craters as revealed by Chandrayaan-2 dual frequency synthetic aperture radar. *npj Space Exploration*. https://www.nature.com/articles/s44453-026-00038-9
3. Tarun M. et al. (2022). A Software Tool to Process & Analyse Chandrayaan-2 Polarimetric DFSAR Data (MIDAS). LPSC Abstract #2232. https://www.hou.usra.edu/meetings/lpsc2022/pdf/2232.pdf
4. VEDAS SAC/ISRO. MIDAS v4.2.4. https://vedas.sac.gov.in/vcms/en/download.html

---

## 15. Appendix — Copy-paste fields for Hack2skill form

**Project title:** LunarIcePath — Integrated Ice Detection & Rover Traverse Planning for Faustini Doubly Shadowed Crater

**One-line description:** Geospatial AI framework combining Chandrayaan-2 DFSAR polarimetry and OHRC terrain data to detect subsurface ice, rank landing sites, optimize rover traverses, and estimate ice volume with confidence intervals.

**Keywords:** Chandrayaan-2, DFSAR, lunar south pole, subsurface ice, CPR, DOP, rover path planning, ISRU, PSR

---

_Copy content into the official Hack2skill template. Adjust team names and institution details before submission._
