# MVP Infrastructure and Implementation Plan

This document captures the infrastructure and MVP strategy derived from the referenced repos.

## What we pulled from the source repos

- **HomeMatch**
  - AI provider config patterns: `AI_PROVIDER`, `GROQ_API_KEY`, `ELEVENLABS_*`.
  - Rule-based fallback for missing AI keys.
  - Prompt construction with domain context and user profile grounding.
  - Separate backend and frontend service boundaries.
  - GitHub-style conventions for dev/test and issue-driven work.

- **Future-Path**
  - Youth intake questionnaire structure and risk scoring rules.
  - Recommendation engine with category tags, priorities, and matching logic.
  - Test suite layout under `tests/`.
  - Streamlit-style dashboard flows for AI-assisted intake.

- **kindConnect**
  - Smart Support Chat concept for guided resource navigation.
  - Resource finder plus reminder and mood check support.
  - Safe, rule-based AI-style behavior before real AI integration.

- **FirstStep**
  - Focus on civic guidance and resource actionability.
  - Lightweight frontend with clear categories and decision aid.

## MVP implementation choices for Community Compass

- Keep the current static HTML/CSS/JS prototype as the user-facing MVP shell.
- Add a root Node package with `npm test` and `dev` scripts to make the repo shareable and runnable.
- Add a basic CI workflow to validate tests on every push.
- Introduce a local `.env.example` for AI provider and ElevenLabs settings.
- Keep AI assistant behavior grounded in listing, youth, and reminder context.
- Use a small `tests/` suite to verify UI helper functions and local storage integration.

## Next infrastructure steps

1. Add a lightweight backend or API proxy if we need live Groq/ElevenLabs integration.
2. Add a stable data format for resources and listings (JSON or SQLite) from FirstStep and Future-Path.
3. Add user session state and assistant persistence using browser storage or a simple backend.
4. Add issue-driven feature authoring using `guidelines.md` and commit/push after each feature.
