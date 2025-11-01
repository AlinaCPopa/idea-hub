from fastapi import APIRouter, Depends
from datetime import datetime, timezone
from sqlalchemy import text
from sqlalchemy.orm import Session
from ...db.session import get_db

router = APIRouter()

@router.get("/health")
async def health():
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}

@router.get("/health/db")
def health_db(db: Session = Depends(get_db)):
    """Validate database connectivity & basic CRUD viability.

    Runs a trivial `SELECT 1` and reports driver URL (redacted) so that cloud
    deployments (where a 500 on /ideas may mask a missing file/migration) can
    be debugged quickly. Extend with migration status if needed.
    """
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "database_url_scheme": db.bind.url.get_backend_name() if db.bind else None,
        }
    except Exception as exc:  # pragma: no cover - diagnostics
        return {
            "status": "error",
            "error": str(exc),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
