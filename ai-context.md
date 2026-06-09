# AI Context for Community Compass

This file gathers the AI patterns and integration points pulled from the referenced repositories.

## HomeMatch

- Uses an AI provider switch controlled by `AI_PROVIDER`.
- Supported providers:
  - `claude` (Anthropic)
  - `groq` (OpenAI-compatible Groq API)
  - `ollama` (local OpenAI-compatible endpoint)
- Provides a rule-based fallback assistant when no real AI key is configured.
- Includes `GROQ_API_KEY`, `GROQ_BASE_URL`, `GROQ_MODEL`, `ANTHROPIC_API_KEY`, and ElevenLabs TTS keys in config.
- Builds a system prompt with:
  - housing program context (Section 8, SRAP, HOPA, LIHTC, Fair Housing, income verification)
  - user role guidance for renters, landlords, or admins
  - site usage guidance explaining Search, Map, Feed, Save, Tour, Apply, and messaging flows
  - optional matching listings to ground recommendations and avoid hallucination
- AI service design notes:
  - keep responses short and practical
  - never give legal advice
  - answer both program questions and navigation questions
  - gracefully fall back to rule-based responses on missing keys or errors

## Future-Path

- Contains a youth intake assistant built as a decision-support workflow.
- Intake questionnaire structure uses typed question definitions with keys and options.
- Stores intake sessions and answers in SQLite tables with migration support.
- Uses risk scoring and recommendation logic to map needs to service categories.
- Recommendation engine is rules-based with:
  - `NEED_PRIORITY`
  - `NEED_TAG_MAP`
  - `RESOURCE_DEFAULT_PRIORITY`
  - `recommendation_source` labels such as `rules_recommender_v1`
- The assistant is explicit about being a decision-support tool and not a replacement for emergency services.
- Streamlit UI serves as a prototype dashboard and navigation shell for the assistant.

## KindConnect

- Community support app built with Java Spring Boot and a lightweight static frontend.
- Focuses on reminders, mood check-ins, resource finder, help requests, and volunteer support.
- AI usage is described as a "Smart Support Chat" feature that starts rule-based and may later call a real AI API.
- The chat logic is meant to guide users to resources based on keywords such as food, loneliness, or help requests.
- This repo reinforces the pattern: start with safe rule-based assistant behavior, then replace or augment with a real LLM engine later.

## FirstStep

- Civic guidance platform that turns public information into actionable resources.
- Emphasizes decision aid, not just a directory.
- Suggests the same high-level user flows we need in Community Compass:
  - filterable resource categories
  - clear action-focused guidance
  - lightweight UI and mobile-first behavior
- Useful concept: treat resource listings as structured guidance with direct next-step actions.

## Proposed Community Compass AI strategy

1. Use Groq as the primary AI provider for contextual assistant responses.
2. Add ElevenLabs for optional voice output in the floating assistant panel.
3. Keep a rule-based fallback for local/dev mode and when API keys are unavailable.
4. Ground the assistant in actual Dashboard state:
   - selected housing filters and listings
   - youth risk questionnaire results
   - current reminders and saved items
   - resource directory scope and category
5. Persist assistant notes and conversation state across pages, allowing email-to-self actions.
6. Keep the AI assistant focused on matching users with relevant community resources, not on general chit-chat.
