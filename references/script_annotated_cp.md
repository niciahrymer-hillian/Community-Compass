# script.js — Annotated Reference Copy

## Purpose
This file contains the browser-side interaction logic for the Community Compass prototype.
It is intentionally kept small and focused on UI behavior, accessibility, and local note persistence.

## Sections

### 1. Constants
- `noteStorageKey`: localStorage key for persisted assistant notes.

### 2. Exported testable helpers
These are exported so Vitest can import and unit-test them without rendering the full page.
They look up DOM nodes **at call time** (not at import time) so the module stays import-safe in
Node and operates against whatever `document` the test has set up.
- `setFontSize(delta)`: adjusts the `html` root font size, clamped to a 14–22px range. Reads the
  current size via `window.getComputedStyle` (the test stubs `global.window`, so bare
  `getComputedStyle` is not available — using the `window.` form works in both browser and JSDOM).
- `calculateRiskPercentage(score)`: pure function converting the youth risk score (0–18) into a
  10–100 visual percentage. Extracted from the old inline `updateRiskScore()` math so it can be
  tested directly.
- `saveNotes()`: persists the `#noteText` textarea content to localStorage.
- `loadNotes()`: restores saved note content from localStorage into `#noteText`.

### 3. Browser wiring — `init()`
- All DOM element lookups and `addEventListener` wiring live inside `init()` so that importing the
  module in Node (for tests) does **not** execute browser-only code.
- Contains the font/contrast controls, panel tabs, listing filter pills, listing detail/tour/email/
  save actions, the resource tabs, and a local `updateRiskScore()` that delegates the math to the
  exported `calculateRiskPercentage()` (single source of truth).
- The `saveNote` button calls the exported `saveNotes()` then shows a confirmation alert.

### 4. Bootstrap guard
- `if (typeof document !== 'undefined' && document.getElementById('decrease-font')) init();`
- In the browser the dashboard markup is present, so `init()` runs. Under a bare Node import the
  guard is false, so no wiring executes and the exported helpers can be tested in isolation.
- `index.html` loads this file as `<script type="module">` because the file now uses ES `export`
  statements, which a classic `<script>` cannot parse.

### Why this structure
- Separating exported helpers from `init()` bootstrapping makes the code testable without a full DOM.
- The module stays compatible with both browser execution and Node/JSDOM unit tests.
- The persisted notes feature mirrors the assistant-side persistent panel concept from the
  referenced repos (HomeMatch/kindConnect).
