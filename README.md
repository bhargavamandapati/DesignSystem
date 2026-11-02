# Aurora — Android Automotive OS (AAOS) IVI Design System

Purple (Material 3, seed `#6750A4`) design system for in-vehicle infotainment on a **10″ 1920×1080** display (1280×720 dp @1.5×), following Android for Cars, Car UI Library and driver-distraction guidelines.
Car UI Library and automotive driver-distraction guidelines (NHTSA, SAE J2364, ISO 15008, WCAG 2.2).

## View (works offline)
Open **`index.html`** in any browser — a single self-contained file (CSS, JS, icons and Roboto fonts are inlined; no network needed).
Top-bar toggles: **Night/Day** theme and **Parked/Driving** UX-restriction simulation.

## Rebuild
Edit files in `src/` (`tokens.json`, `styles.css`, `part1-3.html`, `app.js`) then run `python3 build.py`.
Token export (Android `colors.xml`, `themes.xml` + Car UI RRO, CSS, JSON, Compose) is generated inside the page.

Fonts: Roboto / Roboto Mono (Apache 2.0, from @fontsource).

## Layout
Top status bar (56 dp) · right app bar (120 dp) · bottom HVAC bar (96 dp) · app area 1160×568 dp. Full-screen mode dismisses all bars (app area 1280×720 dp).

## Icons
196 automotive IVI icons in `icons/*.svg` and Android VectorDrawables in `icons/android/ic_*.xml` (also downloadable from the Iconography section).
Regenerate with `python3 tools/icons_src.py` (or `python3 build.py`).

## Android colors
`android/res/values*/colors*.xml` — every role + tonal palette per theme (`aurora_<role>`, drive modes `aurora_eco_<role>` …). Also downloadable from the Developers → Token export section.
