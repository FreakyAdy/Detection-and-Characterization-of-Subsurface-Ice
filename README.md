# LunarIcePath — BAH 2026 PS 8 Demo Scaffold

Pre-build scaffold for the 30-hour Grand Finale (Aug 6–7, 2026). Run locally to validate pipeline before shortlist announcement (Jul 20).

## Quick start

```bash
cd C:\Users\FreakyAdy\Documents\BAH2026-PS8
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# Generate synthetic demo data and run full pipeline
python scripts/run_demo_pipeline.py

# Launch dashboard (use python -m if streamlit is not on PATH)
python -m streamlit run src/dashboard/app.py
# Opens at http://localhost:8501 — use sidebar "Present to Judges" for guided demo
```

## Project structure

```
BAH2026-PS8/
├── 01-registration-checklist.md
├── 02-explainer-session-prep.md
├── 03-idea-proposal-PS8.md
├── 04-research-brief-DFSAR.md
├── config/default.yaml
├── requirements.txt
├── scripts/run_demo_pipeline.py
├── data/demo/                  # Synthetic rasters (auto-generated)
├── output/                     # Pipeline outputs
└── src/
    ├── dfsar/                  # CPR/DOP ice detection
    ├── terrain/                # OHRC slope, roughness, landing sites
    ├── planning/               # Rover traverse optimizer
    ├── volume/                 # Ice volume + Monte Carlo CI
    └── dashboard/              # Streamlit 3D/map viewer
```

## Replacing demo data with ISRO data

1. Place DFSAR co/cross-pol GeoTIFFs in `data/dfsar/`
2. Place OHRC DEM or imagery in `data/ohrc/`
3. Update paths in `config/default.yaml`
4. Re-run `python scripts/run_demo_pipeline.py`

## Team workflow (30h finale)

| Hours | Activity |
|-------|----------|
| 0–4 | Data ingest, MIDAS export, config |
| 4–12 | Pillar A (ice maps) + Pillar B terrain (parallel) |
| 12–18 | Landing sites + traverse optimization |
| 18–22 | Volume estimation + validation |
| 22–28 | Dashboard polish + demo rehearsal |
| 28–30 | Report + submission |

## References

- Idea proposal: [`03-idea-proposal-PS8.md`](03-idea-proposal-PS8.md)
- Research brief: [`04-research-brief-DFSAR.md`](04-research-brief-DFSAR.md)
