"""Build a single PDF submission package for BAH 2026 PS8."""

from __future__ import annotations

import re
import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import FancyArrowPatch, Rectangle


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "05-hackathon-submission-package.md"
OUTPUT = ROOT / "output" / "BAH2026_PS8_Submission_Package.pdf"


def clean_inline(text: str) -> str:
    text = text.replace("`", "")
    text = text.replace("**", "")
    text = text.replace("_", "")
    return text


def md_to_lines(section_text: str) -> list[tuple[str, str]]:
    """Convert a markdown section into display lines."""
    lines: list[tuple[str, str]] = []
    in_code = False
    code_buf: list[str] = []

    for raw in section_text.splitlines():
        line = raw.rstrip()
        if line.startswith("```"):
            if in_code:
                for code_line in code_buf:
                    lines.append(("code", code_line.rstrip()))
                code_buf = []
                in_code = False
            else:
                in_code = True
            continue
        if in_code:
            code_buf.append(line)
            continue
        if not line.strip():
            lines.append(("blank", ""))
            continue
        if line.startswith("### "):
            lines.append(("subheading", clean_inline(line[4:])))
            continue
        if line.startswith("## "):
            lines.append(("heading", clean_inline(line[3:])))
            continue
        if line.startswith("# "):
            lines.append(("title", clean_inline(line[2:])))
            continue
        if re.match(r"^[-*] ", line):
            lines.append(("bullet", clean_inline(line)))
            continue
        if re.match(r"^\d+\. ", line):
            lines.append(("number", clean_inline(line)))
            continue
        if line.startswith("|"):
            lines.append(("table", clean_inline(line)))
            continue
        lines.append(("para", clean_inline(line)))

    return lines


def wrap_line(line: str, width: int) -> list[str]:
    if not line:
        return [""]
    return textwrap.wrap(line, width=width, break_long_words=False, break_on_hyphens=False) or [""]


def add_page_header(ax, title: str, subtitle: str | None = None) -> None:
    ax.text(0.05, 0.95, title, fontsize=20, fontweight="bold", ha="left", va="top")
    if subtitle:
        ax.text(0.05, 0.91, subtitle, fontsize=10, color="#555555", ha="left", va="top")
    ax.plot([0.05, 0.95], [0.885, 0.885], color="#1f3c88", linewidth=1.2)


def draw_text_page(pdf: PdfPages, title: str, section_lines: list[tuple[str, str]], subtitle: str | None = None) -> None:
    fig = plt.figure(figsize=(8.5, 11))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    add_page_header(ax, title, subtitle)

    y = 0.85
    line_height = 0.023
    wrap_width = 92
    styles = {
        "heading": dict(fontsize=15, fontweight="bold", color="#102a43"),
        "subheading": dict(fontsize=12, fontweight="bold", color="#102a43"),
        "title": dict(fontsize=13, fontweight="bold", color="#102a43"),
        "para": dict(fontsize=10.2, color="#1f2933"),
        "bullet": dict(fontsize=10.2, color="#1f2933"),
        "number": dict(fontsize=10.2, color="#1f2933"),
        "table": dict(fontsize=8.2, color="#111827", family="monospace"),
        "code": dict(fontsize=8.2, color="#111827", family="monospace"),
    }

    for kind, raw in section_lines:
        if kind == "blank":
            y -= line_height * 0.65
            continue
        if kind in {"heading", "subheading", "title"}:
            y -= line_height * 0.5
            ax.text(0.05, y, raw, ha="left", va="top", **styles[kind])
            y -= line_height * 1.1
            continue

        prefix = ""
        body = raw
        if kind == "bullet":
            prefix = "• "
            body = raw[2:]
        elif kind == "number":
            m = re.match(r"^(\d+\.)\s+(.*)$", raw)
            if m:
                prefix = f"{m.group(1)} "
                body = m.group(2)
        wrapped = wrap_line(body, wrap_width - len(prefix))
        for i, part in enumerate(wrapped):
            text = prefix + part if i == 0 else "  " + part
            ax.text(0.06, y, text, ha="left", va="top", **styles[kind])
            y -= line_height
            if y < 0.08:
                pdf.savefig(fig, bbox_inches="tight")
                plt.close(fig)
                fig = plt.figure(figsize=(8.5, 11))
                ax = fig.add_axes([0, 0, 1, 1])
                ax.set_axis_off()
                add_page_header(ax, title, subtitle)
                y = 0.85
        y -= 0.002

    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def draw_box(ax, xy, wh, text, facecolor="#edf2ff", edgecolor="#1f3c88", fontsize=8.5):
    x, y = xy
    w, h = wh
    rect = Rectangle((x, y), w, h, facecolor=facecolor, edgecolor=edgecolor, linewidth=1.2)
    ax.add_patch(rect)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fontsize, wrap=True)


def draw_arrow(ax, start, end):
    arrow = FancyArrowPatch(start, end, arrowstyle="->", mutation_scale=12, linewidth=1.2, color="#1f3c88")
    ax.add_patch(arrow)


def draw_process_flow(pdf: PdfPages) -> None:
    fig = plt.figure(figsize=(11, 8.5))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    add_page_header(ax, "Process Flow Diagram", "Detection to mission-ready output")

    boxes = {
        "a": ((0.05, 0.74), (0.19, 0.08), "DFSAR + OHRC\nInputs"),
        "b": ((0.30, 0.74), (0.19, 0.08), "Preprocess\nand calibrate"),
        "c": ((0.55, 0.74), (0.19, 0.08), "CPR / DOP\nice evidence"),
        "d": ((0.80, 0.74), (0.15, 0.08), "Ice probability"),
        "e": ((0.15, 0.52), (0.20, 0.08), "Landing site\nranking"),
        "f": ((0.42, 0.52), (0.20, 0.08), "Traverse\noptimizer"),
        "g": ((0.69, 0.52), (0.20, 0.08), "Volume +\nuncertainty"),
        "h": ((0.36, 0.28), (0.30, 0.08), "Streamlit dashboard\nand final outputs"),
    }
    for x, y, w, h, label in [(*v[0], *v[1], v[2]) for v in boxes.values()]:
        draw_box(ax, (x, y), (w, h), label)

    draw_arrow(ax, (0.24, 0.78), (0.30, 0.78))
    draw_arrow(ax, (0.49, 0.78), (0.55, 0.78))
    draw_arrow(ax, (0.74, 0.78), (0.80, 0.78))
    draw_arrow(ax, (0.64, 0.74), (0.64, 0.60))
    draw_arrow(ax, (0.25, 0.74), (0.25, 0.60))
    draw_arrow(ax, (0.52, 0.74), (0.52, 0.60))
    draw_arrow(ax, (0.79, 0.74), (0.50, 0.36))
    draw_arrow(ax, (0.25, 0.52), (0.42, 0.36))
    draw_arrow(ax, (0.52, 0.52), (0.50, 0.36))
    draw_arrow(ax, (0.79, 0.52), (0.64, 0.36))

    ax.text(0.05, 0.14, "Flow: input data -> radar/terrain analysis -> fusion and ranking -> rover planning -> dashboard delivery",
            fontsize=10.5, color="#1f2933")
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def draw_use_case(pdf: PdfPages) -> None:
    fig = plt.figure(figsize=(11, 8.5))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    add_page_header(ax, "Use Case Diagram", "Actors and system interactions")

    draw_box(ax, (0.34, 0.72), (0.32, 0.13), "LunarIcePath System", facecolor="#f3f7ff", fontsize=12)
    actor_positions = [
        (0.05, 0.80, "Scientist"),
        (0.05, 0.55, "Planner"),
        (0.05, 0.30, "Rover Team"),
        (0.83, 0.80, "Judge"),
    ]
    for x, y, label in actor_positions:
        draw_box(ax, (x, y), (0.12, 0.08), label, facecolor="#f8fafc", fontsize=9.5)

    use_cases = [
        (0.38, 0.50, "Generate\nice maps"),
        (0.58, 0.50, "Rank\nlanding sites"),
        (0.38, 0.28, "Plan rover\ntraverse"),
        (0.58, 0.28, "Estimate\nvolume"),
    ]
    for x, y, label in use_cases:
        draw_box(ax, (x, y), (0.14, 0.09), label, facecolor="#edf7ee", edgecolor="#2f855a", fontsize=9)

    draw_arrow(ax, (0.17, 0.84), (0.34, 0.79))
    draw_arrow(ax, (0.17, 0.59), (0.38, 0.55))
    draw_arrow(ax, (0.17, 0.34), (0.38, 0.32))
    draw_arrow(ax, (0.83, 0.84), (0.66, 0.79))
    draw_arrow(ax, (0.50, 0.72), (0.45, 0.59))
    draw_arrow(ax, (0.50, 0.72), (0.65, 0.59))
    draw_arrow(ax, (0.45, 0.50), (0.45, 0.37))
    draw_arrow(ax, (0.65, 0.50), (0.65, 0.37))
    draw_arrow(ax, (0.52, 0.37), (0.52, 0.15))

    ax.text(0.34, 0.12, "The system converts radar and terrain data into planning outputs that can be reviewed by scientists, planners, rover operators, and judges.",
            fontsize=10.2, color="#1f2933")
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def draw_architecture(pdf: PdfPages) -> None:
    fig = plt.figure(figsize=(11, 8.5))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    add_page_header(ax, "Architecture Diagram", "Input, processing, storage, and presentation layers")

    for x, y, w, h, label, fc, ec in [
        (0.05, 0.74, 0.25, 0.10, "Input Data\nDFSAR / OHRC / Config", "#f8fafc", "#334155"),
        (0.33, 0.74, 0.30, 0.10, "Processing Layer\nCalibration, terrain, fusion, planning", "#eef2ff", "#1f3c88"),
        (0.66, 0.74, 0.29, 0.10, "Storage\nGeoTIFF, NumPy, JSON", "#f0fdf4", "#2f855a"),
        (0.24, 0.42, 0.24, 0.10, "Analytics\nCPR / DOP / slope / roughness", "#fff7ed", "#c2410c"),
        (0.52, 0.42, 0.24, 0.10, "Decision Engines\nLanding, traverse, volume", "#f5f3ff", "#6d28d9"),
        (0.36, 0.16, 0.30, 0.12, "Presentation Layer\nStreamlit dashboard + charts", "#eff6ff", "#2563eb"),
    ]:
        draw_box(ax, (x, y), (w, h), label, facecolor=fc, edgecolor=ec, fontsize=9)

    draw_arrow(ax, (0.17, 0.74), (0.42, 0.64))
    draw_arrow(ax, (0.48, 0.74), (0.65, 0.64))
    draw_arrow(ax, (0.80, 0.74), (0.65, 0.64))
    draw_arrow(ax, (0.45, 0.42), (0.48, 0.28))
    draw_arrow(ax, (0.64, 0.42), (0.52, 0.28))
    draw_arrow(ax, (0.48, 0.22), (0.48, 0.28))
    draw_arrow(ax, (0.48, 0.16), (0.48, 0.05))

    ax.text(0.05, 0.05, "The codebase already maps to this architecture: src/dfsar, src/terrain, src/planning, src/volume, and src/dashboard.",
            fontsize=10.0, color="#1f2933")
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def draw_wireframes(pdf: PdfPages) -> None:
    fig = plt.figure(figsize=(11, 8.5))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    add_page_header(ax, "Wireframes and Mock Diagrams", "Dashboard layout for the hackathon demo")

    # Main dashboard mock
    draw_box(ax, (0.05, 0.62), (0.90, 0.22), "Main dashboard layout\n\nHeader with mission identity\nSidebar with layer toggles and judge mode\nLarge mission map panel\nKPI strip above the map", facecolor="#f8fafc", edgecolor="#475569", fontsize=9)
    # Lower panels
    draw_box(ax, (0.05, 0.26), (0.28, 0.24), "Ice science tab\nCPR heatmap\nDOP heatmap\nHistograms", facecolor="#eef2ff", edgecolor="#1f3c88", fontsize=9)
    draw_box(ax, (0.36, 0.26), (0.28, 0.24), "Landing sites tab\nRanked safety table\nScore chart\nRadar trade-off view", facecolor="#ecfdf5", edgecolor="#2f855a", fontsize=9)
    draw_box(ax, (0.67, 0.26), (0.28, 0.24), "Traverse and volume tabs\nRover path animation\nElevation profile\nMonte Carlo CI chart", facecolor="#fff7ed", edgecolor="#c2410c", fontsize=9)
    ax.text(0.05, 0.16, "These are the same screens implemented in src/dashboard/app.py, presented here as a single-page mock for the submission PDF.", fontsize=10.0)
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(f"Missing source markdown: {SOURCE}")

    text = SOURCE.read_text(encoding="utf-8")
    sections = re.split(r"^##\s+", text, flags=re.M)
    intro = sections[0].strip()
    body_sections = {}
    for part in sections[1:]:
        title, _, body = part.partition("\n")
        body_sections[title.strip()] = body.strip()

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with PdfPages(OUTPUT) as pdf:
        # Title page
        fig = plt.figure(figsize=(8.5, 11))
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_axis_off()
        ax.text(0.08, 0.90, "BAH 2026 PS8", fontsize=18, fontweight="bold", color="#1f3c88")
        ax.text(0.08, 0.84, "LunarIcePath", fontsize=28, fontweight="bold")
        ax.text(0.08, 0.79, "Integrated subsurface ice detection, landing site selection, rover traverse planning, and volume estimation",
                fontsize=11.5, color="#374151")
        ax.text(0.08, 0.72, "Single-file submission package", fontsize=12, fontweight="bold", color="#111827")
        ax.text(0.08, 0.62, "This PDF bundles the written idea, technology stack, feature list, diagrams, wireframes, and implementation cost for Hack2Skill BAH 2026.",
                fontsize=11, wrap=True)
        ax.text(0.08, 0.48, "Included sections:", fontsize=11, fontweight="bold")
        for i, item in enumerate([
            "Problem statement and project fit",
            "Brief about the idea",
            "Problem being solved",
            "Technology stack",
            "Features offered",
            "Process flow, use case, architecture, and wireframe diagrams",
            "Estimated implementation cost",
        ]):
            ax.text(0.10, 0.44 - i * 0.035, f"- {item}", fontsize=10.5)
        ax.text(0.08, 0.16, "Source files remain available in the repo, but this PDF is the single submission artifact.",
                fontsize=10, color="#4b5563")
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        draw_text_page(pdf, "Which Problem Statement", md_to_lines("## Which Problem Statement\n" + body_sections["Which Problem Statement"]), "BAH 2026 PS8")
        draw_text_page(pdf, "Brief About Your Idea", md_to_lines("## Brief About Your Idea\n" + body_sections["Brief About Your Idea"]), "LunarIcePath")
        draw_text_page(pdf, "What Problem We Are Trying To Solve", md_to_lines("## What Problem We Are Trying To Solve\n" + body_sections["What Problem We Are Trying To Solve"]), "Mission planning gap for lunar south-pole ice")
        draw_text_page(pdf, "Technology Stack", md_to_lines("## Technology Stack\n" + body_sections["Technology Stack"]), "Implementation and deployment stack")
        draw_text_page(pdf, "List Of Features", md_to_lines("## List Of Features Offered By The Solution\n" + body_sections["List Of Features Offered By The Solution"]), "Product and demo capabilities")

        draw_process_flow(pdf)
        draw_use_case(pdf)
        draw_wireframes(pdf)
        draw_architecture(pdf)

        draw_text_page(pdf, "Estimated Implementation Cost", md_to_lines("## Estimated Implementation Cost\n" + body_sections["Estimated Implementation Cost"]), "Prototype cost for the hackathon build")
        draw_text_page(pdf, "Final Submission Summary", md_to_lines("## Final Submission Summary\n" + body_sections["Final Submission Summary"]), "Closing page")

        fig = plt.figure(figsize=(8.5, 11))
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_axis_off()
        add_page_header(ax, "Source References", "Included for judge verification")
        refs = [
            "Hackathon event page: https://hack2skill.com/event/bah2026/",
            "Project repository sections: 03-idea-proposal-PS8.md, 04-research-brief-DFSAR.md, config/default.yaml",
            "Summary output: output/summary.json",
            "Dashboard entry point: src/dashboard/app.py",
        ]
        y = 0.82
        for ref in refs:
            ax.text(0.06, y, f"- {ref}", fontsize=10.5)
            y -= 0.05
        ax.text(0.06, 0.56, "Note: the diagram pages are rendered as editable vector shapes and the text pages are laid out from the submission markdown.",
                fontsize=10, color="#4b5563", wrap=True)
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    main()
