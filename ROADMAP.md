# Community Compass — MVP Roadmap

**Last Updated:** June 9, 2026  
**Status:** Phase 0 (Prototype Scaffold Complete)

---

## Current State Summary

### ✅ What We Have
- **Frontend prototype:** Complete interactive HTML/CSS/JS dashboard
- **Architecture UML asset:** Stored in `design/community_compass_architecture_uml.svg`
- **Development guidelines:** `guidelines.md` with commit/push rules, testing standards, and issue-driven development
- **AI context & patterns:** Extracted from HomeMatch, Future-Path, kindConnect, FirstStep in `ai-context.md`
- **Package & CI:** `package.json`, `.env.example`, GitHub Actions workflow
- **Test scaffold:** Basic Vitest setup with module exports for UI helpers
- **Infrastructure docs:** MVP research and pull-repos roadmap

### ⚠️ What's Missing for MVP
- Real data (housing listings, resources, news)
- Backend API or state layer
- AI provider integration (Groq + ElevenLabs)
- Email capabilities
- User authentication & session persistence
- Resource directory content
- Youth risk scoring engine
- Connected detail pages and routing
- Production deployment

---

## UML Alignment

The current prototype covers these UML components:

```
Frontend (HTML/CSS/JS)
├── Dashboard (Hero, Stats, Sections)
├── Housing Section (Map, Listings, Details)
├── Resource Directory (Search, Tabs, Cards)
├── News Feed (Categorized cards)
├── Youth Pathway (Questionnaire, Risk Score)
├── Reminders & Action Plan
└── Floating AI Assistant Panel (Notes, Suggestions, Saved Items)

Missing from UML (needed for MVP):
├── Backend API Layer (Express/FastAPI)
├── Database (SQLite/PostgreSQL)
├── AI Service (Groq integration)
├── Email Service
├── Authentication (Supabase/Auth0)
└── Data Pipeline (Resource cataloging, news feed ingestion)
```

---

## Tech Stack Decision

Based on the source repos and your preferences:

### Frontend
- **Framework:** Vanilla JS (ES modules, no build needed for MVP)
- **Styling:** CSS custom properties + grid/flexbox
- **Testing:** Vitest + JSDOM
- **Storage:** localStorage (session/notes only)
- **Accessibility:** WCAG 2.1 AA (font controls, contrast toggle, semantic HTML)

### Backend (Optional for Phase 1)
- **Language:** Python (FastAPI) — leads the backend to match the UML and the two repos we borrow most logic from
- **Rationale:** HomeMatch uses FastAPI; Future-Path uses Python; async SQLAlchemy continuity avoids a later rewrite
- **Recommendation:** Stand up FastAPI first; treat Java Spring Boot as an additive service layer per the UML, not the MVP entry point

### Data Layer
- **Primary:** SQLite (local dev) → PostgreSQL (production)
- **Pattern:** Future-Path's relational schema for resources and intakes
- **Schema:** Housing listings, resources, news items, user intakes, risk scores

### AI Provider
- **Primary:** Groq (free, OpenAI-compatible, fast)
- **Fallback:** Rule-based assistant (HomeMatch pattern)
- **Voice:** ElevenLabs optional (MVP can skip)

### Deployment
- **Frontend:** Vercel (no cost, auto-deploys from GitHub)
- **Backend:** Render or Railway (free tier available)
- **Database:** Supabase (Postgres + auth) or Railway

---

## Tech Stack Reconciliation (UML Target vs. MVP Path)

The UML architecture (`design/community_compass_architecture_uml.svg`) and pitch deck commit to a specific production stack. The current prototype intentionally uses a lighter stack to move fast. This table makes the relationship explicit so we converge on the UML target rather than drift from it.

| Layer | UML / Pitch Target | Phase 0–1 MVP Path | Migration Plan |
|-------|--------------------|--------------------|----------------|
| Frontend | React 18 + Vite + Tailwind + React Query | Vanilla HTML/CSS/JS prototype (`index.html`) | Port validated sections to React components; keep the navy/white/green palette + layout |
| Backend | Java Spring Boot + FastAPI microservices, REST | Single FastAPI service | Lead with FastAPI; add Spring Boot services if/when Java-side features are needed |
| Data | PostgreSQL + Supabase, async SQLAlchemy 2.0 | SQLite (local dev) | Move to Supabase Postgres; adopt async SQLAlchemy 2.0 from the start |
| AI | Groq (primary) + ElevenLabs voice, rule-based fallback | Rule-based fallback only | Wire Groq when key is ready; ElevenLabs for assistant voice |
| Geo | Leaflet + regional filtering | Static map mockup | Replace mockup with Leaflet + real listing coordinates |

**Decision:** Build the frontend prototype in vanilla JS first to validate UX cheaply, then migrate to **React 18 + Vite + Tailwind** before production so the shipped app matches the UML. Lead the backend with **FastAPI** (Python) for async-SQLAlchemy continuity with HomeMatch/Future-Path; **Java Spring Boot** is an additive service layer, not the MVP entry point.

> Note: the **File Structure (Target)** section below sketches a Node-style layout for readability; the backend modules (`routes/`, `models/`, `services/`) will be implemented as Python/FastAPI packages, not `.js` files.

---

## MVP Feature Breakdown

### Phase 1: Core MVP (Web Prototype)
**Goal:** Interactive dashboard users can sign in to, explore resources, and get AI suggestions.

#### 1.1 Authentication & Session
- [ ] Basic login/signup (email + password)
- [ ] Session persistence (JWT or cookie)
- [ ] User profile with preferences (housing type, income, age)
- **Owner:** Backend + Supabase Auth
- **Test:** Login flow, session timeout, profile save/restore

#### 1.2 Housing Section
- [ ] Backend API for listing CRUD
- [ ] Sample housing data (3-5 real listings from Delaware)
- [ ] Filter by program type (Section 8, SRAP, 55+)
- [ ] Listing detail page with landlord info and tour request
- [ ] Save/email listing functionality
- **Owner:** Backend + Frontend UI updates
- **Data source:** Borrowed pattern from HomeMatch
- **Test:** Filter logic, save persistence, detail page render

#### 1.3 Resource Directory
- [ ] Backend API for resource search/category
- [ ] Sample resources: housing, food, transit, health (50-100 items)
- [ ] Category tabs (All, Shelter, Food, Utilities, Health)
- [ ] Search by keyword
- [ ] Resource detail pages with contact + map link
- **Owner:** Backend + Frontend
- **Data source:** FirstStep + Delaware.gov pattern
- **Test:** Search, filter, category tabs

#### 1.4 Youth Pathway
- [ ] Risk questionnaire (10 questions from Future-Path)
- [ ] Risk scoring engine (rules-based, no AI yet)
- [ ] Suggested resources based on risk score
- [ ] Caseworker referral trigger
- [ ] Session persistence (save intake progress)
- **Owner:** Backend + Frontend
- **Data source:** Future-Path intake structure
- **Test:** Scoring logic, resource suggestions, persistence

#### 1.5 AI Assistant (Grounded Fallback)
- [ ] Rule-based assistant matching keywords to resources
- [ ] Context grounding (current dashboard state)
- [ ] Notes saving and email-to-self
- [ ] Panel persists across page navigation
- [ ] Fallback only until Groq key ready
- **Owner:** Frontend + optional backend for email
- **Data source:** HomeMatch rule-based fallback pattern
- **Test:** Keyword matching, note persistence, email draft

#### 1.6 News Feed
- [ ] Sample state news (5-10 real items from Delaware)
- [ ] Category badges (Housing, Food, Health, Employment)
- [ ] Optional: Auto-refresh from RSS or API
- **Owner:** Backend static data or scraper
- **Data source:** HUD, DSHA, local news feeds
- **Test:** Feed render, category display

### Phase 2: Production Readiness (After MVP Sign-Off)
- [ ] Groq + ElevenLabs integration for AI voice
- [ ] Real email delivery (SendGrid/Mailgun)
- [ ] User data encryption (sensitive fields)
- [ ] Rate limiting and CORS
- [ ] Metrics and error logging
- [ ] Mobile app (Capacitor PWA)

### Phase 3: Advanced Features (Post-MVP)
- [ ] Landlord dashboard for listing management
- [ ] Caseworker portal for intake review
- [ ] Integrated calendar for tour scheduling
- [ ] Admin panel for resource curation
- [ ] Multi-language support

---

## Work-by-Phase Checklist

### Phase 1: MVP Sprint (Est. 2-3 weeks)

#### Week 1: Backend Setup + Auth
- [ ] Initialize Express/Node backend
- [ ] Set up PostgreSQL on Render or local
- [ ] Implement Supabase Auth or JWT
- [ ] Create user model + session table
- [ ] Write login/signup endpoint tests
- **Commit after each feature completes**

#### Week 2: Core Data & APIs
- [ ] Create housing listings table + seed 5 samples
- [ ] Create resources table + seed 50-100 samples
- [ ] Create news_items table + seed 10 samples
- [ ] Build search/filter endpoints
- [ ] Wire frontend to backend APIs (replace mock data)
- [ ] Write endpoint tests
- **Commit after each feature completes**

#### Week 3: Youth Intake + Assistant
- [ ] Create intake_sessions + intake_answers tables (Future-Path schema)
- [ ] Implement risk scoring engine (rules-based)
- [ ] Build recommendation matching logic
- [ ] Wire youth questionnaire to backend
- [ ] Implement rule-based assistant grounding
- [ ] Write scoring + matching tests
- **Commit after each feature completes**

#### Week 4: Polish & Deploy
- [ ] Add email-to-self for notes (SendGrid)
- [ ] Set up CI/CD (GitHub Actions → Vercel/Render)
- [ ] Add error handling and logging
- [ ] Security audit: CORS, XSS, SQLi prevention
- [ ] Load testing and optimization
- [ ] Deploy to production
- **Final commit + tag release**

---

## Data Models (from source repos)

### Users
```
- id (UUID)
- email
- password_hash
- profile: { role, income_type, housing_type, age_range }
- created_at
- updated_at
```

### Housing Listings
```
- id
- title
- address, city, state, zip
- bedrooms, bathrooms
- rent_amount
- programs: [section8, srap, hopa, lihtc]
- description
- landlord_name, phone, email
- created_at
```

### Resources
```
- id
- name, category (shelter, food, transit, health)
- description
- need_tags: [housing, employment, food, ...]
- contact_phone, contact_email, website
- address, city, state, hours
- created_at
```

### Intake Sessions (Youth Pathway)
```
- id
- youth_id or candidate_id
- profile_type: youth | candidate
- questions_answered: { key → answer_value }
- risk_score
- recommended_resources: [resource_id, ...]
- status: in_progress | completed
- created_at
```

### Assistant Conversations
```
- id
- user_id
- messages: [{ role: user|assistant, content: string, timestamp }]
- notes: string (user-editable)
- saved_items: [resource_id, listing_id, ...]
- updated_at
```

---

## File Structure (Target)

```
Community-Compass/
├── frontend/                    (current root becomes this)
│   ├── index.html
│   ├── styles.css
│   ├── script.js
│   ├── pages/
│   │   ├── housing-detail.html
│   │   ├── resource-detail.html
│   │   ├── profile.html
│   │   └── admin.html              (Phase 2)
│   ├── tests/
│   │   └── script.test.js
│   └── references/
│
├── backend/                     (new)
│   ├── app.js
│   ├── config.js
│   ├── routes/
│   │   ├── auth.js
│   │   ├── listings.js
│   │   ├── resources.js
│   │   ├── intakes.js
│   │   └── assistant.js
│   ├── models/
│   │   ├── user.js
│   │   ├── listing.js
│   │   ├── resource.js
│   │   ├── intake.js
│   │   └── conversation.js
│   ├── services/
│   │   ├── ai_service.js        (Groq + rule-based fallback)
│   │   ├── email_service.js
│   │   ├── scoring_service.js   (risk + recommendations)
│   │   └── news_service.js
│   ├── tests/
│   │   ├── test_auth.js
│   │   ├── test_listings.js
│   │   ├── test_intakes.js
│   │   └── test_scoring.js
│   ├── db/
│   │   ├── schema.sql
│   │   ├── seeds/
│   │   │   ├── listings.json
│   │   │   ├── resources.json
│   │   │   └── news.json
│   │   └── migrations/          (Alembic or Node migrations)
│   ├── package.json
│   ├── .env.example
│   └── server.js
│
├── design/
│   └── community_compass_architecture_uml.svg
│
├── research/
│   ├── mvp-infrastructure.md
│   ├── ai-context.md
│   └── pull-repos.md
│
├── guidelines.md
├── README.md
├── package.json
├── .env.example
└── .github/
    └── workflows/
        └── ci.yml
```

---

## Success Criteria for MVP

### Functional
- [ ] Users can sign in and see personalized dashboard
- [ ] Housing filter and detail pages work end-to-end
- [ ] Resource search and category tabs work
- [ ] Youth questionnaire calculates risk and suggests resources
- [ ] Assistant can save notes and draft emails
- [ ] All pages load in <2s on broadband

### Technical
- [ ] 80%+ unit test coverage for business logic
- [ ] Zero security vulnerabilities (OWASP top 10)
- [ ] All API endpoints documented (OpenAPI/Swagger)
- [ ] CI passes on every commit
- [ ] Error logging via console or Sentry

### UX
- [ ] Accessibility: WCAG 2.1 AA compliant
- [ ] Mobile responsive (tested on iPhone 12, Android)
- [ ] No console errors
- [ ] Onboarding flow clear to new users

---

## How This Aligns with Your Source Repos

| Repo | What We Borrowed | Where It Shows |
|------|------------------|-----------------|
| HomeMatch | AI provider pattern, fallback assistant, context grounding, deployment strategy | `ai-context.md`, `script.js`, backend architecture |
| Future-Path | Youth intake structure, risk scoring rules, recommendation engine, test patterns | Youth Pathway, `data models`, test scaffold |
| kindConnect | Smart Support Chat logic, resource finder, reminder UI pattern | Assistant fallback, Resource Directory |
| FirstStep | Civic guidance focus, resource actionability, decision aid UX | Resource detail pages, category structure |

---

## Next Steps When You Resume

1. **Read this roadmap** and confirm the phases align with your vision.
2. **Set up the backend** following Phase 1 Week 1 (Express + Auth).
3. **Create the first GitHub issue** for backend setup.
4. **Follow guidelines.md:** Issue-driven, test-first, commit/push after each feature.
5. **Reference `ai-context.md`** when wiring the AI assistant.
6. **Use the data models** above as schema templates.

---

## Questions to Consider Before Resuming

1. **Backend framework:** Express (Node) or FastAPI (Python)? Node is lighter for MVP.
2. **Database:** Local SQLite now, Postgres on Render later, or go straight to Supabase?
3. **Authentication:** Supabase Auth (easiest) or roll your own JWT?
4. **Email provider:** SendGrid (free tier), Mailgun, or local SMTP for dev?
5. **Groq key:** Will you have this before starting backend? If not, rule-based fallback is fine for MVP.
6. **Team size:** Solo work or assigning tasks to others? Affects branch strategy.

---

**This roadmap is your north star. Revisit it before each sprint, and update it as priorities shift.**
