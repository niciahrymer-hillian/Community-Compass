# script.js — Annotated Reference Copy

## Purpose
This file contains the browser-side interaction logic for the Community Compass prototype.
It is intentionally kept small and focused on UI behavior, accessibility, and local note persistence.

## Sections

### 1. Constants and state keys
- `noteStorageKey`: localStorage key for notes
- `isBrowser`: feature detection for safe module import in tests

### 2. UI helper functions
- `setFontSize(delta)`: adjusts the `html` root font size within a safe range.
- `calculateRiskPercentage(score)`: converts the youth risk score into a visual percentage.
- `toggleHighContrast()`: toggles high-contrast theme mode on the root element.
- `filterListings(filter)`: hides or shows listing cards based on a selected category.
- `selectListingDetails(title, score)`: populates the detail card with the selected listing data.
- `saveNotes()`: persists the note textarea content to localStorage.
- `loadNotes()`: loads saved note content from localStorage.

### 3. Application bootstrap
- `initializeApp()`: finds the DOM elements, attaches event listeners, and restores persisted state.
- The module uses `DOMContentLoaded` to run only in a real browser context.

### 4. Testing strategy
- This file exports core helpers so they can be unit tested without rendering the full page.
- The tests focus on small pure functions and local state persistence.

### Why this structure
- Separating helpers from bootstrapping makes the code easier to test and evolve.
- The module remains compatible with both browser execution and Node/JSDOM unit tests.
- The persisted notes feature mirrors the assistant-side persistent panel concept from the referenced repos.
