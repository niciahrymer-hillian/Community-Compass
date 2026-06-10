# Community Compass — User Stories

## Project Vision
Community Compass is an AI-assisted housing and support-matching platform that
helps users find housing and critical resources based on eligibility, risk
level, location, and personal needs. It also gives support teams a dashboard to
prioritize urgent cases and recommend services faster.

> **AI intake bot:** the assistant asks what the user is looking for and asks the
> proper follow-up questions to gauge their resource need — producing structured
> data such as a caseworker intake form, a transportation request form, etc. The
> AI supports intake; it does **not** make final decisions.

---

## 1. User Intake
**As a person looking for housing or support, I want to complete a guided intake
form, so that the system can understand my situation and recommend housing and
resources that fit me.**

Example inputs: age, location, housing status, income range, employment status,
education status, family size, transportation needs, food access needs,
health/wellness needs, safety concerns, ID/document status, housing assistance
type (Section 8, SRAP, 55+, income-restricted).

Acceptance: user can complete + save/submit intake; required fields validated;
answers stored in DB; intake data feeds the matching and risk-scoring systems.

## 2. AI-Assisted Intake
**As a user who may not know what services I need, I want an AI assistant to ask
simple questions, so that I can explain my situation naturally and still produce
structured data.**

Acceptance: AI asks clear, supportive questions; responses convert to structured
intake fields; user reviews answers before submitting; AI does not make final
decisions; structured results are stored. *(Connects to Future-Path's AI intake.)*

## 3. Housing Eligibility Matching
**As a renter, I want to see housing options I may qualify for, so that I do not
waste time applying to places that do not fit.**

Factors: income, age, family size, location, housing-assistance status,
disability/senior eligibility, program type, urgency. Acceptance: system compares
intake vs program rules; matches ranked by fit; each result explains why it
matched and includes contact info, website, phone, location. *(Heart of HomeMatch.)*

## 4. Risk / Priority Scoring
**As a caseworker, I want the system to calculate a clear risk score, so that I
can identify users who need help most urgently.**

Factors: homelessness/unstable housing, youth age-out timeline, lack of income,
lack of transportation, food insecurity, health needs, missing ID/documents,
safety concerns, no current support connection. Acceptance: score is calculated +
explainable; high-risk users flagged; score updates when intake changes;
dashboard filters by risk level. *(Future-Path explainable risk scoring.)*

## 5. Resource Recommendation Engine
**As a user, I want recommended resources based on my needs, so that I can
quickly connect with the right services.**

Categories: housing, education, employment, food access, transportation, health
& wellness, mentorship, ID/documents, safety, financial literacy, legal aid,
youth services. Acceptance: recommendations ranked by need/location/urgency; each
includes contact info + why recommended; caseworker can assign resources to a user.

## 6. Map-Based Resource Search
**As a user, I want to view nearby housing and support resources on a map, so
that I understand what is available close to me.**

Acceptance: resources on a map; filterable by category; click for details
(address, contact, service type); caseworkers can use it during support planning.
Tech fit: React + Leaflet + Leaflet-Geoman.

## 7. User Dashboard
**As a user, I want a simple dashboard showing my matches, assigned resources,
and next steps, so that I know what to do after intake.**

Acceptance: shows housing matches, recommended resources, assigned
caseworker/contact, next steps; user can update intake when their situation changes.

## 8. Caseworker Dashboard
**As a caseworker, I want to see users, risk levels, intake summaries, and
recommendations, so that I can make faster support decisions.**

Features: total users served, high-risk users, housing-urgent users, youth aging
out soon, users missing documents, users needing employment/transportation,
resource-assignment status. Acceptance: view all users; filter by risk + need;
open a user profile; view AI intake summary; assign resources; add notes/status.
*(Future-Path operational dashboard.)*

## 9. User Profile / Case View
**As a caseworker, I want to open a user profile, so that I can understand their
needs, risk level, matches, and support history.**

Acceptance: shows intake summary, risk score, recommended housing/resources,
assigned resources, case notes, updated status. Statuses: new intake, needs
review, high priority, resources assigned, contact attempted, in progress,
stabilized, closed.

## 10. Admin Resource Management
**As an admin, I want to add and update housing programs and resources, so that
the system stays accurate.**

Acceptance: add/edit/deactivate resources; categorize; add eligibility rules;
add contact info + location.

## 11. Data Cleaning & Validation Pipeline
**As a developer, I want a pipeline that cleans and validates housing/resource
data, so that the platform uses reliable information.**

Acceptance: Python scripts clean raw JSON/CSV; invalid records flagged; missing
fields reported; clean data loaded into DB; testable with sample data.
*(Anitra's Python validator + Shocka's cleaning pipeline.)*

## 12. Backend API
**As a frontend developer, I want REST APIs for intake, users, resources, housing
matches, and dashboard data, so that the frontend connects to real services.**

Areas: user intake, housing matching, resource recommendation, risk scoring,
caseworker dashboard, admin resource, authentication. Acceptance: JSON responses;
cURL-testable; validation; PostgreSQL-backed. Tech: Java 17 + Spring Boot **and/or**
FastAPI + SQLAlchemy (team may split services).

## 13. Authentication & Roles
**As a platform user, I want secure login and role-based access, so that users,
caseworkers, and admins only see what they are allowed to.**

Roles: user/client, caseworker, admin, developer/test. Acceptance: secure login;
role-gated access; caseworkers see assigned users; admins manage resources;
private info protected. *(Supabase Auth / Spring Security / custom.)*

## 14. Privacy & Data Protection
**As a user sharing personal info, I want my data protected, so that I can trust
the platform.**

Acceptance: sensitive data encrypted where needed; role-based access; users see
only their own info; caseworkers see only authorized cases; minimal PII exposure.
Tech: Fernet encryption, Supabase RLS, backend authorization.

## 15. Testing & Smoke Checks
**As a developer, I want automated + manual tests, so that we can prove the
project works and avoid regressions.**

Acceptance: APIs cURL-testable; Python validator has test cases; frontend
component tests; matching + risk-scoring test scenarios; demo data works every
time. Tech: pytest, Vitest, cURL, Maven tests, smoke-check scripts.

---

## Suggested MVP Flow
1. User completes intake (form or AI-guided).
2. Backend validates + stores data in PostgreSQL.
3. System calculates risk score (housing, income, transport, food, health, safety…).
4. Matching engine recommends housing programs + support services.
5. User sees recommended housing + resources + next steps.
6. Caseworker sees dashboard of high-priority users + recommendations.
7. Caseworker assigns resources and tracks progress.

## Team Fit by Feature
- **React / Vite / Tailwind / React Query / Leaflet:** intake form, user dashboard, caseworker dashboard, resource cards, map view, API integration.
- **Java Spring Boot:** REST APIs, user records, caseworker dashboard API, resource management, matching endpoints, PostgreSQL integration. *(→ kindConnect: dashboard + newsfeed.)*
- **Python (FastAPI):** data cleaning, validation, synthetic data, risk scoring, resource matching. *(→ HomeMatch map/housing; Future-Path caseworker/risk/intake.)*
- **PostgreSQL / Supabase:** users, intake responses, housing programs, resources, risk scores, recommendations, case notes, RBAC.
- **AI tools:** AI-assisted intake, intake summary, recommendation explanation, caseworker support notes, next-step suggestions.

## One-Sentence Pitch
Community Compass combines housing eligibility matching, AI-assisted intake, risk
scoring, resource recommendations, and caseworker dashboards into one platform
that helps people find the support they qualify for and helps support teams act faster.
