"""A-SPACE inspired dark lunar UI theme for Streamlit."""

from __future__ import annotations

import streamlit as st

# Reference palette: deep black, glowing cyan-blue, navy glass cards
ACCENT = "#4da6ff"
ACCENT_GLOW = "rgba(77, 166, 255, 0.45)"
ACCENT_GOLD = "#f5c842"
BG = "#000000"
BG_NAVY = "#0a1628"
CARD = "rgba(10, 22, 40, 0.72)"
CARD_BORDER = "rgba(77, 166, 255, 0.22)"
TEXT = "#ffffff"
MUTED = "#9aa8bc"


def inject_theme() -> None:
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;600;700;800&family=Rajdhani:wght@400;500;600&display=swap');

        /* ── Base ── */
        .stApp {{
            background: {BG};
            color: {TEXT};
        }}
        .stApp::before {{
            content: "";
            position: fixed;
            inset: 0;
            background:
                radial-gradient(ellipse 80% 50% at 50% -10%, rgba(77,166,255,0.12) 0%, transparent 55%),
                radial-gradient(circle at 85% 60%, rgba(77,166,255,0.04) 0%, transparent 40%);
            pointer-events: none;
            z-index: 0;
        }}
        .block-container {{
            padding-top: 0.5rem;
            max-width: 1320px;
            position: relative;
            z-index: 1;
        }}
        #MainMenu, footer, header[data-testid="stHeader"] {{
            visibility: hidden;
        }}
        h1, h2, h3, h4 {{
            font-family: 'Orbitron', sans-serif !important;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }}
        p, span, label, .stMarkdown, .stCaption {{
            font-family: 'Rajdhani', sans-serif !important;
        }}

        /* ── Nav bar ── */
        .nav-bar {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.85rem 0;
            margin-bottom: 0.25rem;
            border-bottom: 1px solid {CARD_BORDER};
        }}
        .nav-logo {{
            font-family: 'Orbitron', sans-serif;
            font-weight: 800;
            font-size: 1.35rem;
            color: {TEXT};
            letter-spacing: 0.12em;
        }}
        .nav-logo span {{
            color: {ACCENT};
            text-shadow: 0 0 18px {ACCENT_GLOW};
        }}
        .nav-links {{
            display: flex;
            gap: 2rem;
            font-family: 'Rajdhani', sans-serif;
            font-size: 0.95rem;
            color: {MUTED};
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }}
        .nav-badge {{
            border: 1px solid {CARD_BORDER};
            border-radius: 4px;
            padding: 0.35rem 0.9rem;
            font-size: 0.85rem;
            color: {TEXT};
            background: {CARD};
        }}

        /* ── Hero ── */
        .hero-section {{
            position: relative;
            border-radius: 16px;
            overflow: hidden;
            margin: 1.25rem 0 1.5rem;
            min-height: 200px;
            background: linear-gradient(135deg, {BG_NAVY} 0%, #050a14 100%);
            border: 1px solid {CARD_BORDER};
            box-shadow: 0 0 40px rgba(77,166,255,0.08);
        }}
        .hero-section::after {{
            content: "";
            position: absolute;
            bottom: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, transparent, {ACCENT}, transparent);
            box-shadow: 0 0 12px {ACCENT_GLOW};
        }}
        .hero-inner {{
            padding: 2.5rem 2.5rem 2rem;
            position: relative;
            z-index: 1;
        }}
        .hero-eyebrow {{
            font-family: 'Rajdhani', sans-serif;
            font-size: 0.8rem;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            color: {ACCENT};
            margin-bottom: 0.5rem;
        }}
        .hero-title {{
            font-family: 'Orbitron', sans-serif;
            font-size: 2.4rem;
            font-weight: 800;
            color: {TEXT};
            line-height: 1.15;
            margin: 0;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}
        .hero-title em {{
            font-style: normal;
            color: {ACCENT};
            text-shadow: 0 0 24px {ACCENT_GLOW};
        }}
        .hero-desc {{
            color: {MUTED};
            font-size: 1.05rem;
            max-width: 620px;
            margin-top: 0.85rem;
            line-height: 1.55;
        }}

        /* ── Wave divider ── */
        .wave-divider {{
            height: 2px;
            margin: 1.5rem 0;
            background: linear-gradient(90deg,
                transparent 0%, {ACCENT} 20%, {ACCENT} 50%, transparent 80%);
            box-shadow: 0 0 16px {ACCENT_GLOW};
            opacity: 0.7;
        }}

        /* ── KPI feature cards (A-SPACE style) ── */
        .kpi-card {{
            background: {CARD};
            backdrop-filter: blur(12px);
            border: 1px solid {CARD_BORDER};
            border-radius: 12px;
            padding: 1.25rem 1rem;
            text-align: center;
            transition: border-color 0.2s, box-shadow 0.2s;
            position: relative;
            overflow: hidden;
        }}
        .kpi-card::before {{
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, {ACCENT}, transparent);
            opacity: 0.6;
        }}
        .kpi-card:hover {{
            border-color: rgba(77,166,255,0.45);
            box-shadow: 0 0 24px rgba(77,166,255,0.12);
        }}
        .kpi-icon {{
            font-size: 1.4rem;
            margin-bottom: 0.35rem;
            filter: drop-shadow(0 0 8px {ACCENT_GLOW});
        }}
        .kpi-value {{
            font-family: 'Orbitron', sans-serif;
            font-size: 1.45rem;
            color: {ACCENT};
            font-weight: 700;
            text-shadow: 0 0 12px {ACCENT_GLOW};
        }}
        .kpi-label {{
            color: {MUTED};
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.14em;
            margin-top: 0.35rem;
        }}
        .kpi-sub {{
            color: {MUTED};
            font-size: 0.7rem;
            margin-top: 0.15rem;
            opacity: 0.8;
        }}

        /* ── Plotly chart containers ── */
        div[data-testid="stPlotlyChart"] {{
            background: {CARD};
            border: 1px solid {CARD_BORDER};
            border-radius: 14px;
            padding: 0.35rem 0.5rem 0.5rem;
            margin-bottom: 0.5rem;
            position: relative;
        }}
        div[data-testid="stPlotlyChart"]::after {{
            content: "";
            position: absolute;
            bottom: 0; right: 0;
            width: 40px; height: 40px;
            border-right: 2px solid {ACCENT};
            border-bottom: 2px solid {ACCENT};
            border-radius: 0 0 14px 0;
            opacity: 0.35;
            pointer-events: none;
        }}
        div[data-testid="stPydeckChart"] {{
            background: {CARD};
            border: 1px solid {CARD_BORDER};
            border-radius: 14px;
            overflow: hidden;
        }}
        .section-label {{
            font-family: 'Rajdhani', sans-serif;
            font-size: 0.72rem;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: {ACCENT};
            margin: 0 0 0.15rem 0.25rem;
        }}
        .section-heading {{
            font-family: 'Orbitron', sans-serif;
            font-size: 1rem;
            color: {TEXT};
            margin: 0 0 0.75rem 0.25rem;
            letter-spacing: 0.08em;
        }}

        /* ── Sidebar ── */
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #050a14 0%, {BG_NAVY} 100%);
            border-right: 1px solid {CARD_BORDER};
        }}
        section[data-testid="stSidebar"] .stMarkdown h3 {{
            color: {ACCENT} !important;
            font-size: 0.95rem !important;
        }}

        /* ── Demo steps ── */
        .demo-step {{
            background: rgba(77,166,255,0.06);
            border-left: 2px solid {CARD_BORDER};
            padding: 0.65rem 0.85rem;
            border-radius: 0 8px 8px 0;
            margin: 0.4rem 0;
            font-size: 0.88rem;
        }}
        .demo-step-active {{
            background: rgba(77,166,255,0.14);
            border-left: 2px solid {ACCENT};
            box-shadow: inset 0 0 20px rgba(77,166,255,0.06);
        }}

        /* ── Tabs ── */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 6px;
            background: transparent;
            border-bottom: 1px solid {CARD_BORDER};
        }}
        .stTabs [data-baseweb="tab"] {{
            background: transparent;
            border: 1px solid transparent;
            border-radius: 8px 8px 0 0;
            color: {MUTED};
            font-family: 'Rajdhani', sans-serif;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            font-weight: 600;
            padding: 0.5rem 1rem;
        }}
        .stTabs [aria-selected="true"] {{
            background: rgba(77,166,255,0.1) !important;
            border-color: {CARD_BORDER} !important;
            border-bottom-color: transparent !important;
            color: {ACCENT} !important;
            box-shadow: 0 -2px 12px rgba(77,166,255,0.15);
        }}

        /* ── Metrics ── */
        div[data-testid="stMetric"] {{
            background: {CARD};
            border: 1px solid {CARD_BORDER};
            border-radius: 10px;
            padding: 0.65rem 0.85rem;
        }}
        div[data-testid="stMetric"] label {{
            color: {MUTED} !important;
            font-family: 'Rajdhani', sans-serif !important;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-size: 0.75rem !important;
        }}
        div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
            color: {ACCENT} !important;
            font-family: 'Orbitron', sans-serif !important;
        }}

        /* ── Buttons ── */
        .stButton > button {{
            background: linear-gradient(135deg, {ACCENT} 0%, #2d7dd2 100%);
            color: {BG} !important;
            border: none;
            border-radius: 24px;
            font-family: 'Rajdhani', sans-serif;
            font-weight: 600;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            box-shadow: 0 0 20px {ACCENT_GLOW};
        }}
        .stButton > button:hover {{
            box-shadow: 0 0 28px rgba(77,166,255,0.6);
        }}

        /* ── Toggle / checkbox accent ── */
        .stCheckbox label span {{
            color: {MUTED} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_nav(mission_label: str) -> None:
    st.markdown(
        f"""
        <div class="nav-bar">
            <div class="nav-logo">LUNAR<span>ICE</span>PATH</div>
            <div class="nav-links">
                <span>Mission</span>
                <span>Radar</span>
                <span>Terrain</span>
                <span>Traverse</span>
            </div>
            <div class="nav-badge">{mission_label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_hero(mission_label: str, mission_coords: str) -> None:
    st.markdown(
        f"""
        <div class="hero-section">
            <div class="hero-inner">
                <div class="hero-eyebrow">BAH 2026 · Problem Statement 8</div>
                <h1 class="hero-title">Explore the<br><em>Faustini Crater</em></h1>
                <p class="hero-desc">
                    Subsurface ice detection and rover traverse planning for
                    <strong>{mission_label}</strong> at {mission_coords} using
                    Chandrayaan-2 DFSAR polarimetry and OHRC terrain data.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_wave_divider() -> None:
    st.markdown('<div class="wave-divider"></div>', unsafe_allow_html=True)


def render_kpi_row(values: list[tuple[str, str, str]]) -> None:
    """Each item: (icon, label, value, optional sub) — icon + label + value."""
    cols = st.columns(len(values))
    for col, item in zip(cols, values):
        icon, label, value = item[0], item[1], item[2]
        sub = item[3] if len(item) > 3 else ""
        sub_html = f'<div class="kpi-sub">{sub}</div>' if sub else ""
        with col:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-icon">{icon}</div>
                    <div class="kpi-value">{value}</div>
                    <div class="kpi-label">{label}</div>
                    {sub_html}
                </div>
                """,
                unsafe_allow_html=True,
            )


def section_header(label: str, heading: str) -> None:
    st.markdown(
        f'<div class="section-label">{label}</div>'
        f'<div class="section-heading">{heading}</div>',
        unsafe_allow_html=True,
    )
