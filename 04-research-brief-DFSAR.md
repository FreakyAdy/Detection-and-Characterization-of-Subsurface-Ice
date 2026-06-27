# Research Brief: Chandrayaan-2 DFSAR, CPR/DOP Ice Detection & MIDAS Workflow

Pre-read guide for BAH 2026 PS 8 — complete before **July 1, 2026**.

---

## 1. Key papers and official sources (read in this order)

### Priority 1 — Must read

| # | Source | URL | Focus |
|---|--------|-----|-------|
| 1 | ISRO press release on DFSAR ice discovery | https://www.isro.gov.in/ISRO_EN/Chandrayaan2_Dual_Frequency_Synthetic_Aperture_Radar.html | Official CPR>1, DOP<0.13 criterion; Faustini crater context |
| 2 | PRL / npj Space Exploration (2026) | https://www.nature.com/articles/s44453-026-00038-9 | Full methodology; craters F2, F3, H3, S1; DOP refinement from 0.35 to 0.13 |
| 3 | MIDAS LPSC 2022 abstract | https://www.hou.usra.edu/meetings/lpsc2022/pdf/2232.pdf | Software capabilities for DFSAR polarimetry |

### Priority 2 — Supporting context

| # | Source | Focus |
|---|--------|-------|
| 4 | The Hindu coverage (Jun 2026) | https://www.thehindu.com/sci-tech/science/chandrayaan-2-detects-possible-presence-of-subsurface-ice-near-south-pole-of-moon/article71031903.ece | Public summary; lobate-rim morphology |
| 5 | VEDAS MIDAS download page | https://vedas.sac.gov.in/vcms/en/download.html | MIDAS v4.2.4 installation (841 MB, login required) |

### Priority 3 — Background polarimetry (if time permits)

- Campbell, B. A. (2012). High circular polarization ratios in PSRs — CPR ice vs. roughness ambiguity
- Fa W. & Cai Y. (2013). Dielectric properties of lunar regolith — for volume modeling (Pillar C)

---

## 2. Core science — CPR and DOP

### Circular Polarization Ratio (CPR)

```
CPR = σ_cross / σ_co
```

Where σ_cross and σ_co are cross-polarized and co-polarized backscatter coefficients from the DFSAR covariance matrix.

| CPR value | Interpretation |
|-----------|----------------|
| CPR ≈ 0.5–0.7 | Typical lunar regolith (volume + surface scatter) |
| CPR > 1 | Enhanced volumetric scattering — **candidate for subsurface ice** |
| CPR very high | Can also occur on extremely rough fresh craters (false positive) |

### Degree of Polarization (DOP)

Measures how much of the reflected radar signal retains its original polarization state.

| DOP value | Interpretation |
|-----------|----------------|
| DOP < 0.13 | Strong depolarization → **volumetric scattering (ice indicator)** |
| DOP > 0.35 | More surface-like scattering → likely rocky terrain |
| DOP 0.55–0.66 | Observed in H1 and Tooley craters — **no ice signature** |

### Combined criterion (ISRO/PRL 2026)

```
ICE_CANDIDATE = (CPR > 1.0) AND (DOP < 0.13)
```

**Why both are needed:** Young rocky craters can show CPR > 1 without ice. Low DOP distinguishes true volumetric ice scatter from roughness artifacts.

### Target crater

- **Location:** Faustini permanently shadowed region, lunar south pole
- **Feature:** 1.1 km diameter doubly shadowed crater (DSC) inside Faustini
- **Morphology:** Lobate-rim — suggests impact penetrated ice-rich subsurface
- **Also studied:** Craters F2, F3, H3, S1 in same paper

---

## 3. DFSAR instrument summary

| Parameter | L-band | S-band |
|-----------|--------|--------|
| Frequency | ~24 cm wavelength | ~12 cm wavelength |
| Penetration | Deeper subsurface | Shallower, higher resolution |
| Mode | Full + hybrid polarimetry | Full + hybrid polarimetry |
| Resolution | Up to ~2 m/pixel | Up to ~2 m/pixel |

**Hackathon implication:** Fuse L- and S-band — agreement on ice candidates increases confidence.

---

## 4. MIDAS workflow (step-by-step)

**Download:** https://vedas.sac.gov.in/vcms/en/download.html → MIDAS v4.2.4 (requires VEDAS login)

### Phase 1 — Data ingestion

1. Obtain DFSAR Level-1/2 product for target crater (ISRO-provided at hackathon)
2. Open in MIDAS GUI (Windows or Linux)
3. Verify metadata: frequency band, polarization mode, incidence angle

### Phase 2 — Radiometric calibration

1. Apply radiometric calibration to sigma-nought
2. Generate covariance matrix **C3** (3×3 complex) or coherence **T3**
3. Apply speckle filter (Lee, Refined Lee, or Wishart — test sensitivity)

### Phase 3 — Polarimetric products

1. Compute **Stokes parameters** (S0, S1, S2, S3)
2. Derive **CPR** map from cross/co-pol channels
3. Derive **DOP** map from Stokes parameters
4. Optional decompositions: Pauli, Yamaguchi, H/A/Alpha (for surface vs. volume scatter context)

### Phase 4 — Ice mapping

1. Threshold: CPR > 1.0 AND DOP < 0.13
2. Mask to doubly shadowed crater interior (from OHRC/illumination model)
3. Compare pixel count with published Supplementary Fig. counts (F2 has ~6× more CPR-elevated pixels than F3)
4. Export GeoTIFF for Python pipeline

### Phase 5 — Validation

1. Overlay OHRC imagery — check lobate-rim correlation
2. Flag high-CPR + high-roughness regions as false positives
3. Cross-check L-band vs S-band agreement

### MIDAS modules reference (from LPSC 2022 abstract)

- Covariance/coherence matrix generation
- Speckle filtering
- Stokes parameters & CPR
- Polarimetric decompositions (Pauli, Yamaguchi, H-A-Alpha)
- Wishart classification (ROI-based)

---

## 5. Python fallback pipeline (when MIDAS unavailable)

Our scaffold in `src/dfsar/` implements:

```
process_dfsar.py  → Load GeoTIFF / ENVI bands, build covariance proxy
cpr_dop.py        → Compute CPR, DOP, fused ice probability
```

**Inputs expected:** Co-pol and cross-pol backscatter rasters (or SHH, SHV, VVH, VVV components)

**Outputs:** `cpr.tif`, `dop.tif`, `ice_probability.tif`

---

## 6. OHRC terrain analysis checklist

| Step | Method | Tool |
|------|--------|------|
| Slope map | DEM derivative or shadow-based proxy | GDAL, `src/terrain/ohrc_analysis.py` |
| Roughness | Std dev of elevation in moving window | SciPy |
| Boulder detection | Texture analysis / Canny edges on OHRC | OpenCV |
| Landing ellipses | Flat areas: slope < 8°, low roughness | Custom scoring |
| PSR boundary | Illumination model or provided mask | Skyfield |

---

## 7. Rover traverse constraints (from PS document)

- Avoid slopes exceeding rover mobility limit (baseline: **15°**; tune per mentor guidance)
- Minimize traversal through boulder fields
- Maintain solar exposure at periodic waypoints (south pole: peaks of eternal light nearby)
- Path must connect landing site → ice target floor without discontinuities

**Algorithm options:**

| Method | Pros | Cons |
|--------|------|------|
| Weighted A* | Fast, deterministic | Single objective unless weighted sum |
| RRT* | Handles complex constraints | Slower, stochastic |
| Pareto A* (multi-run) | Shows trade-offs | More compute |

Our scaffold uses **weighted A*** with configurable weights in `config/default.yaml`.

---

## 8. Ice volume estimation (Pillar C)

### Dielectric mixing model (simplified)

```
ε_eff = (1 - f_ice) × ε_regolith + f_ice × ε_ice
```

| Parameter | Typical value |
|-------------|---------------|
| ε_regolith | ~2.5–3.5 |
| ε_ice | ~3.15 |
| f_ice | Derived from CPR/DOP calibration or assumed 5–30% for candidates |
| Depth | Top 5 m (per PS requirement) |

### Monte Carlo uncertainty

Perturb: f_ice ± 10%, depth ± 2 m, region boundary ± 1 pixel erosion/dilation

Report: **mean volume, 95% CI, equivalent water mass (kg)**

---

## 9. Pre-reading checklist

- [ ] Read ISRO press release (10 min)
- [ ] Skim npj paper abstract + Figs 3–4 (CPR/DOP maps) (30 min)
- [ ] Read MIDAS LPSC abstract (15 min)
- [ ] Install MIDAS from VEDAS OR verify Python fallback runs (`python -m src.dfsar.cpr_dop`)
- [ ] Review PS 8 expected outcomes in `PROBLEM STATEMENT 1.txt` lines 616–672
- [ ] Attend explainer session with questions from `02-explainer-session-prep.md`

---

## 10. Glossary

| Term | Definition |
|------|------------|
| PSR | Permanently Shadowed Region — never receives direct sunlight |
| DSC | Doubly Shadowed Crater — crater inside a PSR, doubly shielded |
| DFSAR | Dual-Frequency Synthetic Aperture Radar (Chandrayaan-2) |
| OHRC | Orbiter High Resolution Camera |
| CPR | Circular Polarization Ratio |
| DOP | Degree of Polarization |
| ISRU | In-Situ Resource Utilization |
| MIDAS | MIcrowave Data Analysis Software (SAC/ISRO) |
| Faustini | Parent crater containing target 1.1 km DSC at south pole |

---

## 11. Questions to resolve at explainer session

See [`02-explainer-session-prep.md`](02-explainer-session-prep.md) — update this section with answers.

**Answer log:**

| Topic | Mentor answer |
|-------|---------------|
| CPR/DOP thresholds fixed or tunable? | _Pending_ |
| MIDAS mandatory? | _Pending_ |
| DEM provided? | _Pending_ |
