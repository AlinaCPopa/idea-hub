# IdeaHub Full-Stack

Spec-first full-stack application showcasing a FastAPI backend and React + TypeScript frontend with generated OpenAPI types. Designed for rapid ramp-up.

- Backend: https://ideahub-api.wonderfulsmoke-5ba33355.northeurope.azurecontainerapps.io/docs for interactive API docs.
- Frontend: https://ideahub-frontend.wonderfulsmoke-5ba33355.northeurope.azurecontainerapps.io/
- GitHub Repo: https://github.com/AlinaCPopa/idea-hub


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

### Frontend Setup
```bash
cd frontend
npm install
npm run gen:api
npm run dev
```

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

docker build -t ideahubappregistry.azurecr.io/backend:latest ./backend
docker push ideahubappregistry.azurecr.io/backend:latest
docker build -t ideahubappregistry.azurecr.io/frontend:latest ./frontend
docker push ideahubappregistry.azurecr.io/frontend:latest
docker build -t ideahubappregistry.azurecr.io/backend:rev2 ./backend
docker push ideahubappregistry.azurecr.io/backend:rev2
## Azure Deployment (Container Apps + Bicep) 🚀

Current live environment (per user-provided resources):
- Resource Group: `idea-hub-rg`
- Container Apps Environment: `ideahub-env`
- Backend Container App: `aideahub-api`
- Frontend Container App: `ideahub-frontend`
- Azure Container Registry: `ideahubappregistry`
- Log Analytics Workspace: `workspace-ideahubrg2Sa4`
- Public Frontend URL: https://ideahub-frontend.wonderfulsmoke-5ba33355.northeurope.azurecontainerapps.io/

### Infrastructure as Code
`infra/main.bicep` updates (or creates if missing) the backend & frontend Container Apps with new image tags and environment variables. It assumes existing ACR, Log Analytics, and Container Apps Environment.

### GitHub Actions CI/CD
Workflow: `.github/workflows/deploy.yml`
Flow:
1. Build backend & frontend images
2. Push to ACR (`ideahubappregistry`)
3. Deploy Bicep with new tags
4. Output URLs

Required repo secrets:
```
AZURE_CLIENT_ID
AZURE_TENANT_ID
AZURE_SUBSCRIPTION_ID
SECRET_KEY (temporary until Key Vault integration)
```

Trigger a manual run:
GitHub → Actions → Deploy to Azure Container Apps → Run workflow.

### Local One-Off Deploy (CLI)
```pwsh
$tag = (git rev-parse --short HEAD)
az acr login --name ideahubappregistry
docker build -t ideahubappregistry.azurecr.io/ideahub-backend:$tag -f backend/Dockerfile .
docker build -t ideahubappregistry.azurecr.io/ideahub-frontend:$tag -f frontend/Dockerfile .
docker push ideahubappregistry.azurecr.io/ideahub-backend:$tag
docker push ideahubappregistry.azurecr.io/ideahub-frontend:$tag
az deployment group create -g idea-hub-rg `
  --template-file infra/main.bicep `
  --parameters backendImageTag=$tag frontendImageTag=$tag secretKey=$env:SECRET_KEY `
               existingContainerAppsEnvironmentName=ideahub-env existingAcrName=ideahubappregistry existingLogAnalyticsName=workspace-ideahubrg2Sa4
```

### Image Tag Strategy
The workflow uses the short commit SHA. Consider adding a mutable `latest` tag plus an immutable SHA tag for rollback.

### Secrets & Key Vault (Next Step)
Move `SECRET_KEY` to Azure Key Vault, then replace direct secret parameterization with a Container App secret set operation:
```pwsh
az keyvault secret set -n SECRET_KEY --vault-name <vaultName> --value <value>
az containerapp secret set -g idea-hub-rg -n aideahub-api --secrets secret-key=<value>
az containerapp update -g idea-hub-rg -n aideahub-api --set-env-vars SECRET_KEY=secretref:secret-key
```
Automate this in a pre-deploy job (avoid exposing secret in template).

### Rollback
List revisions:
```pwsh
az containerapp revision list -g idea-hub-rg -n aideahub-api -o table
```
Set active revision (if multiple):
```pwsh
az containerapp revision activate -g idea-hub-rg -n aideahub-api --revision <revisionName>
```

### Scaling Tweaks
Edit scale rule in `infra/main.bicep` (concurrent requests) or add CPU based rule:
```bicep
scale: {
  minReplicas: 1
  maxReplicas: 5
  rules: [
    {
      name: 'http-concurrency'
      http: { metadata: { concurrentRequests: '50' } }
    }
  ]
}
```

### Observability
Container Logs:
```pwsh
az containerapp logs show -g idea-hub-rg -n aideahub-api --follow
```
Query via Log Analytics (Kusto):
```
ContainerAppConsoleLogs_CL | where ContainerAppName_s == "aideahub-api"
```

### Legacy App Service Section
The previous App Service deployment instructions have been removed for brevity. If you need them, retrieve from git history. Container Apps is now the primary path.

## License
MIT
