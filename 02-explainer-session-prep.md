# PS 8 Explainer Session Prep — Jun 15 & 16, 2026

Attend **at least one** explainer session for Problem Statement 8. Use this document during the session.

---

## Session logistics

- **Dates:** June 15 and 16, 2026 (links on Hack2skill dashboard / Discord)
- **Goal:** Clarify evaluation weights, data access, and scope boundaries before idea submission (Jul 1)
- **Team prep:** Assign one member to take notes; one to ask technical questions; one to ask evaluation questions

---

## Questions for ISRO mentors (priority order)

### Evaluation weights

1. How are the four deliverables weighted in shortlisting vs. finale scoring?
   - Ice detection (CPR/DOP maps)
   - Landing site feasibility
   - Rover traverse path
   - Ice volume estimate (top ~5 m)
2. How are **false-positive ice detections** penalized vs. missed detections?
3. Is **landing site safety** weighted equally to **scientific ice volume** estimates?
4. Does cross-validation with **OHRC morphology** (lobate-rim, boulder fields) count toward ice detection scoring?
5. Is **uncertainty quantification** (confidence intervals on volume) explicitly evaluated?

### Data access

6. Will DFSAR and OHRC data for the Faustini doubly shadowed crater be provided at idea phase or only after shortlisting?
7. What file formats will be supplied (GeoTIFF, ENVI, PDS, MIDAS-native)?
8. Is **MIDAS** the required processing toolchain, or are Python/GDAL custom pipelines acceptable?
9. Will illumination models or pre-computed slope/aspect rasters be provided?

### Scope boundaries

10. Can we use **published PRL/ISRO CPR > 1 & DOP < 0.13 criteria** as baseline and innovate on top (uncertainty, fusion, path planning)?
11. For rover traverse: must the path optimize **solar power constraints** explicitly, or is terrain safety alone sufficient?
12. Is a **live 3D visualization demo** expected at the finale, or are static maps + report sufficient?
13. What compute/GPU resources will be available during the 30-hour finale?

### Shortlisting

14. Approximately how many teams per problem statement advance to the finale?
15. For idea submission: what sections are mandatory in the official template?

---

## Answers log (fill during session)

| Question | Mentor answer | Action item |
|----------|---------------|-------------|
| Evaluation weights | | |
| False positive penalty | | |
| Data format / access timing | | |
| MIDAS vs custom pipeline | | |
| Shortlist quota | | |
| Template requirements | | |

---

## Talking points if asked "What is your approach?"

**30-second pitch:**

> We are building **LunarIcePath** — an integrated exploration-planning system for the Faustini doubly shadowed crater. We combine Chandrayaan-2 DFSAR polarimetry (CPR/DOP with uncertainty maps), OHRC terrain safety analysis, and a multi-criteria rover traverse optimizer that balances ice proximity, slope, roughness, and sun-exposure windows. We deliver a 3D dashboard for landing site comparison and ice volume estimates with confidence intervals using a dielectric mixing model.

**Differentiation (vs. generic ice maps):**

- Not just detection — **actionable mission planning** (landing + traverse + volume)
- **Morphology cross-check** (lobate-rim, roughness) to reduce CPR false positives from rocky terrain
- **Pareto-optimal paths**, not shortest-path heuristics

---

## Post-session action items

- [ ] Update [`03-idea-proposal-PS8.md`](03-idea-proposal-PS8.md) with any scope/eval clarifications
- [ ] Revise [`04-research-brief-DFSAR.md`](04-research-brief-DFSAR.md) if data format changes
- [ ] Adjust demo scaffold in `src/` if mentors specify required outputs
- [ ] Submit final idea proposal before **Jul 1, 2026**

---

## Backup trigger (switch to PS 4)

If mentors confirm any of the following, discuss switching to PS 4 with the team:

- No DFSAR data until finale day
- Evaluation is 80%+ ice detection with no credit for traverse/volume
- Shortlist quota for PS 8 is < 5 teams nationally

See [`01-registration-checklist.md`](01-registration-checklist.md) for PS 4 backup steps.
