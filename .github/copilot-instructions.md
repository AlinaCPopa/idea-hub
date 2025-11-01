## Copilot Instructions / Implementation Tracker

Purpose: A living, automation‑friendly checklist + context brief so an AI assistant (and humans) can quickly understand project status, what to do next, and the definition of done. Keep concise, actionable, and free of secrets.

---
### High‑Level Project Summary
Idea Hub: Full‑stack app
* Backend: FastAPI (Python) with SQLite dev DB (`backend/dev.db`), JWT-style auth (password hashing via PBKDF2), users & ideas CRUD, health endpoint.
* Frontend: Vite + React + TypeScript + Tailwind; consumes generated OpenAPI types.
* Contract: `spec/openapi.yaml` → generates TypeScript types into `frontend/src/api/generated/types.ts`.
* Containerization: Individual `Dockerfile` per service + `docker-compose.yml` (not yet validated in this tracker).

### Current Checklist / Status
- [x] Clarify Project Requirements
- [x] Scaffold the Project
- [x] Customize the Project
- [ ] Install Required Extensions
- [x] Compile the Project (backend imports + frontend TypeScript build OK)
- [x] Create and Run Task (VS Code tasks present)
- [ ] Launch the Project (validate simultaneous backend + frontend runtime & basic E2E flows)
- [ ] Ensure Documentation is Complete

### Definition of Remaining Checklist Items
"Install Required Extensions": A curated list of recommended VS Code extensions is present below AND (optionally) a `extensions.json` recommendations file exists (TODO) – then check this.
"Launch the Project": Achieved when: (1) Backend `uvicorn` task starts with no runtime errors, (2) Frontend dev server starts with no TypeScript errors, (3) Frontend successfully calls backend health endpoint & one protected endpoint after login, (4) CORS OK.
"Ensure Documentation is Complete": Top-level `README.md` includes: architecture overview, quick start, tasks usage, type-gen, testing, environment variables, Docker & compose, auth notes, contribution pointers.

### Architecture (Concise)
Backend Layers:
* `app/api/routers`: route modules (`auth.py`, `ideas.py`, `users.py`, `health.py`).
* `app/db/models.py`: SQLAlchemy models.
* `app/schemas`: Pydantic schemas.
* `app/core/security.py`: PBKDF2 password hashing utilities.
Frontend Layers:
* Pages under `src/pages` mapping to major routes.
* API client scaffolding in `src/api/client.ts` + generated types.
* Shared UI components under `src/components`.

### Key VS Code Tasks
| Label | Purpose |
|-------|---------|
| Backend: Run API (uvicorn) | Start FastAPI with autoreload |
| Backend: Tests | Run pytest suite |
| Frontend: Dev Server | Start Vite dev server |
| Generate OpenAPI Types | Regenerate TS types from `openapi.yaml` |

### Recommended VS Code Extensions (to satisfy "Install Required Extensions")
Add these to a forthcoming `.vscode/extensions.json`:
1. ms-python.python – Python language features
2. ms-python.black-formatter – (If using Black) / or charliermarsh.ruff – Ruff linter+formatter
3. ms-azuretools.vscode-docker – Docker & compose support
4. esbenp.prettier-vscode – Prettier for TS/JS formatting
5. dbaeumer.vscode-eslint – ESLint integration
6. bradlc.vscode-tailwindcss – Tailwind IntelliSense
7. oderwat.indent-rainbow – (Optional) readability
8. usernamehw.errorlens – Inline error surfacing
9. GitHub.copilot / GitHub.copilot-chat – Pair programming

### Environment Variables (Dev Defaults / TODO for README)
If (or when) environment variables are introduced, document them. For now inferred placeholders:
* `APP_ENV` (optional) – environment name (default: `dev`)
* `SECRET_KEY` – for signing tokens (currently likely hardcoded / default; rotate for prod)
* `ACCESS_TOKEN_EXPIRE_MINUTES` – token lifetime

### OpenAPI Type Generation Flow
1. Update `spec/openapi.yaml`.
2. Run task: "Generate OpenAPI Types" (calls `npm run gen:api`).
3. Imports auto-refresh from `frontend/src/api/generated/types.ts`.

### Password Hashing Note
Using PBKDF2 for portability to avoid native module build issues (bcrypt). If migrating to a stronger hash (e.g., argon2), ensure cross-platform availability or fallback.

### Quality Gates (Minimum Before Merging)
1. Build / Import: Backend `uvicorn` starts; frontend TypeScript compile passes.
2. Tests: `pytest` all green.
3. Lint/Format: (Pending adoption) Python (Ruff/Black) + ESLint/Prettier clean.
4. Security Quick Win: No plaintext secrets committed; dependency scan (future enhancement).
5. Docs: README sections present (see Documentation Definition above).

### Assistant Operating Guidelines
Do:
* Regenerate types after changing `openapi.yaml`.
* Add/update minimal tests when adding routes.
* Keep this file concise – replace paragraphs with bullet points when it grows.
* Update checklist immediately after completing an item.
Avoid:
* Storing secrets here.
* Massive diffs due solely to reformatting.
* Divergent documentation between this file and README; this file should remain a terse tracker.

### Immediate Next Actions (As of Last Update)
1. Validate simultaneous launch (backend + frontend) & mark Launch complete.
2. Create `.vscode/extensions.json` with recommendations; check Install Required Extensions.
3. Expand `README.md` to full spec; check Ensure Documentation is Complete.

### Future Enhancements (Optional Backlog)
* Add user & idea CRUD test coverage.
* Add CI pipeline (lint, test, type-gen check, build) – GitHub Actions.
* Introduce .env file & `python-dotenv` for local env management.
* Replace SQLite with Postgres in container for prod parity.
* Add CORS fine-grained origins from config.

---
Progress Note: Backend compiled & tests pass; PBKDF2 in place; frontend deps & generated types done. Pending: Launch validation & documentation completion.

Last Updated: (update date when modifying)
