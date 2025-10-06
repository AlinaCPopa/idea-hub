# IdeaHub Full-Stack

Spec-first full-stack application showcasing a FastAPI backend and React + TypeScript frontend with generated OpenAPI types. Designed for rapid ramp-up.

## Tech Stack
- Backend: FastAPI, SQLAlchemy, JWT auth (python-jose), Pydantic v2
- Frontend: React 18, Vite, TypeScript, React Query, TailwindCSS, Axios
- Spec: OpenAPI 3.1 (see `spec/openapi.yaml`) with type generation via `openapi-typescript`
- DX: Hot reload both sides, type-safe API calls, simple seed data

## Key Features / Talking Points
1. Spec-driven workflow: The contract in `spec/openapi.yaml` drives generated TS types.
2. Clean layering: `schemas` (Pydantic) vs `models` (SQLAlchemy) vs `routers` (FastAPI) separation.
3. Security: JWT-based auth, password hashing (bcrypt), protected routes.
4. Extensibility: Add routes by updating spec then generating types.
5. Performance/Basics: Async-ready (could swap DB), CORS configured for frontend.
6. Frontend data layer: React Query for caching + optimistic possibilities.
7. Maintainability: Central `api/client.ts` with auth token injection.
8. Minimal infra: `docker-compose.yml` for one-command multi-service startup.

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- (Optional) `uv` for fast Python dependency management

### Backend Setup
```powershell
cd backend
python -m venv .venv
.# On PowerShell
./.venv/Scripts/Activate.ps1
pip install -e .[dev]
# Seed (run as module to avoid relative import issue)
python -m app.db.init_db
uvicorn app.main:app --reload
```
Visit https://ideahub-api.wonderfulsmoke-5ba33355.northeurope.azurecontainerapps.io/docs for interactive API docs.

### Frontend Setup
```bash
cd frontend
npm install
npm run gen:api
npm run dev
```
Visit https://ideahub-frontend.wonderfulsmoke-5ba33355.northeurope.azurecontainerapps.io/

### Generate Types (after spec change)
```bash
cd frontend
npm run gen:api
```
Or use PowerShell script:
```pwsh
pwsh shared/scripts/generate-types.ps1
```

### Demo Credentials
Seed user: `demo` / `demo`

### Typical Flow (Spec-First)
1. Modify `spec/openapi.yaml` (add route/schema) 
2. Regenerate types (`npm run gen:api`) 
3. Implement backend router + Pydantic schema 
4. Use new typed endpoints in frontend.

## Testing
Backend sample test: `pytest` (health endpoint). Frontend placeholder test TBD (add Vitest / RTL for component tests).

### Password Hashing Note
For portability on Windows, the backend uses `pbkdf2_sha256` (Passlib) instead of native `bcrypt` to avoid environment-specific backend issues. Swap to `bcrypt` or `argon2` in production if desired.

## Next Ideas
- Add Alembic migrations & Postgres
- Introduce CI (GitHub Actions) for lint + test
- Add Vitest + React Testing Library tests
- Add rate limiting & caching
- Add OpenAPI codegen client abstraction layer
 - Replace pbkdf2 with bcrypt/argon2 + proper password policy

## Environment Variables
Copy `.env.example` to `.env` and adjust secrets (especially `JWT_SECRET`).

## Azure Container Deployment (App Service) 🛰️

The project can be deployed as two Linux container apps (backend + frontend) using your existing Azure resources:

Prerequisites:
- Resource Group: `idea-hub-rg`
- Container Registry: `ideahubappregistry` (login server: `ideahubappregistry.azurecr.io`)
- App Service Plan: `idea-hub-service-plan` (Linux, e.g. B1/Sku of choice)
- Custom domain

### 1. Build & Push Images
Backend:
```pwsh
az acr login --name ideahubappregistry
docker build -t ideahubappregistry.azurecr.io/backend:latest ./backend
docker push ideahubappregistry.azurecr.io/backend:latest
```

Frontend:
```pwsh
docker build -t ideahubappregistry.azurecr.io/frontend:latest ./frontend
docker push ideahubappregistry.azurecr.io/frontend:latest
```

### 2. Create Container Apps (If not already)
```pwsh
az containerapp create `
	--resource-group idea-hub-rg `
	--plan idea-hub-service-plan `
	--name idea-hub-api `
	--deployment-container-image-name ideahubappregistry.azurecr.io/backend:latest

az containerapp create `
	--resource-group idea-hub-rg `
	--plan idea-hub-service-plan `
	--name idea-hub-frontend `
	--deployment-container-image-name ideahubappregistry.azurecr.io/frontend:latest
```

### 3. Configure App Settings
Backend settings:
```pwsh
az webapp config appsettings set -g idea-hub-rg -n idea-hub-api --settings `
	JWT_SECRET="<secure-random>" `
	DATABASE_URL="sqlite:///./dev.db" `
	CORS_ORIGINS="https://idea-hub.azurewebsites.net"
```

Frontend settings (point API base to backend):
```pwsh
az webapp config appsettings set -g idea-hub-rg -n idea-hub-frontend --settings `
	VITE_API_BASE="https://idea-hub-api.azurewebsites.net"
```

### 4. Enable ACR Pull (if Managed Identity not automatic)
```pwsh
az webapp config container set -g idea-hub-rg -n idea-hub-api \
	--docker-custom-image-name ideahubappregistry.azurecr.io/backend:latest \
	--docker-registry-server-url https://ideahubappregistry.azurecr.io

az webapp config container set -g idea-hub-rg -n idea-hub-frontend \
	--docker-custom-image-name ideahubappregistry.azurecr.io/frontend:latest \
	--docker-registry-server-url https://ideahubappregistry.azurecr.io
```

If using ACR admin user (not recommended for prod):
```pwsh
$acrUser = az acr credential show -n ideahubappregistry --query username -o tsv
$acrPass = az acr credential show -n ideahubappregistry --query passwords[0].value -o tsv
az webapp config container set -g idea-hub-rg -n idea-hub-api `
	--docker-custom-image-name ideahubappregistry.azurecr.io/backend:latest `
	--docker-registry-server-user $acrUser `
	--docker-registry-server-password $acrPass
```

### 5. Redeploy (New Version)
```pwsh
docker build -t ideahubappregistry.azurecr.io/backend:rev2 ./backend
docker push ideahubappregistry.azurecr.io/backend:rev2
az webapp config container set -g idea-hub-rg -n idea-hub-api --docker-custom-image-name ideahubappregistry.azurecr.io/backend:rev2
```

### 6. Health Checks
Backend health: `/health` (ensure Easy Auth/firewalls allow it).

### 7. Security To-Do for Production
- Rotate `JWT_SECRET` into Azure Key Vault + reference via Key Vault reference
- Use Postgres (Azure Flexible Server) instead of local SQLite
- Add HTTPS-only, custom domain + managed cert
- Enable logging & diagnostics (`az webapp log config`)

## License
MIT
