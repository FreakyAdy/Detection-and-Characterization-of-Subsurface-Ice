# LunarIcePath - BAH 2026 PS 8 Demo

LunarIcePath is a Streamlit mission-control dashboard for detecting likely subsurface lunar ice, ranking safe landing zones, planning a rover traverse, and estimating extractable ice volume for BAH 2026 Problem Statement 8.

The repo includes a synthetic demo pipeline so the dashboard can run without external ISRO data while the real DFSAR/OHRC inputs are being prepared.

## Quick Start

Run these commands from the repository root.

### Windows PowerShell

```powershell
cd C:\Users\FreakyAdy\Documents\BAH2026-PS8
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/run_demo_pipeline.py
python -m streamlit run src/dashboard/app.py
```

### macOS / Linux

```bash
git clone <your-repo-url>
cd BAH2026-PS8
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/run_demo_pipeline.py
python -m streamlit run src/dashboard/app.py
```

Open the local URL printed by Streamlit, usually:

```text
http://localhost:8501
```

Use the sidebar toggle **Present to Judges** for the guided demo flow.

## Required Run Order

1. Install dependencies with `pip install -r requirements.txt`.
2. Generate demo outputs with `python scripts/run_demo_pipeline.py`.
3. Start the dashboard with `python -m streamlit run src/dashboard/app.py`.

The dashboard reads generated files from `output/`, especially `output/summary.json` and the `.npy` raster arrays. If those files are missing, the app will ask you to run the pipeline first.

## Free Deployment

Recommended free host: **Streamlit Community Cloud**.

Official docs:

- Streamlit Community Cloud: https://docs.streamlit.io/deploy/streamlit-community-cloud
- Deploy guide: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
- Dependency guide: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies

### Prepare the GitHub Repo

1. Run the demo pipeline locally:

```bash
python scripts/run_demo_pipeline.py
```

2. Commit the app, dependencies, config, and generated demo outputs:

```bash
git add README.md requirements.txt config scripts src output
git commit -m "Prepare Streamlit deployment"
git push origin main
```

Keep the generated `output/` files in the repo for deployment. Streamlit Community Cloud starts the app with `streamlit run`; it will not automatically run `scripts/run_demo_pipeline.py` before launch.

### Deploy on Streamlit Community Cloud

1. Go to https://share.streamlit.io/.
2. Sign in with GitHub.
3. Click **Create app**.
4. Select this repository and branch.
5. Set the main file path to:

```text
src/dashboard/app.py
```

6. In **Advanced settings**, use Python 3.12 unless you have tested another version.
7. Click **Deploy**.

After deployment, Streamlit gives you a public `*.streamlit.app` URL that you can share for free.

## Troubleshooting

### ImportError after editing files

If Streamlit shows an old import error after a code change, stop the running server with `Ctrl+C` and restart:

```bash
python -m streamlit run src/dashboard/app.py
```

Streamlit can keep an older module state alive until the process is restarted.

### No pipeline output found

Run:

```bash
python scripts/run_demo_pipeline.py
```

Then restart or refresh the dashboard.

### Port already in use

Run Streamlit on another port:

```bash
python -m streamlit run src/dashboard/app.py --server.port 8502
```

## Project Structure

```text
BAH2026-PS8/
|-- 01-registration-checklist.md
|-- 02-explainer-session-prep.md
|-- 03-idea-proposal-PS8.md
|-- 04-research-brief-DFSAR.md
|-- config/default.yaml
|-- requirements.txt
|-- scripts/run_demo_pipeline.py
|-- data/demo/                 # Synthetic GeoTIFF inputs generated locally
|-- output/                    # Dashboard-ready generated outputs
`-- src/
    |-- dfsar/                 # CPR/DOP ice detection
    |-- terrain/               # OHRC slope, roughness, landing sites
    |-- planning/              # Rover traverse optimizer
    |-- volume/                # Ice volume and Monte Carlo CI
    `-- dashboard/             # Streamlit app, charts, maps, theme
```

## Replacing Demo Data with ISRO Data

1. Place DFSAR co-pol and cross-pol GeoTIFFs in `data/dfsar/`.
2. Place OHRC DEM or imagery in `data/ohrc/`.
3. Update paths and thresholds in `config/default.yaml`.
4. Re-run `python scripts/run_demo_pipeline.py`.
5. Launch `python -m streamlit run src/dashboard/app.py`.

## Team Workflow

| Hours | Activity |
| --- | --- |
| 0-4 | Data ingest, MIDAS export, config |
| 4-12 | Pillar A ice maps and Pillar B terrain analysis |
| 12-18 | Landing site ranking and traverse optimization |
| 18-22 | Volume estimation and validation |
| 22-28 | Dashboard polish and demo rehearsal |
| 28-30 | Report and final submission |

## References

- Idea proposal: [03-idea-proposal-PS8.md](03-idea-proposal-PS8.md)
- Research brief: [04-research-brief-DFSAR.md](04-research-brief-DFSAR.md)
