"""
PHISHGUARD//NEXUS - FastAPI Application Factory & Main Entrypoint
"""

from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from backend.app.core.config import settings
from backend.app.db.session import init_db
from backend.app.api.routes import scan, history, system, model, report


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize SQLite tables
    init_db()
    yield
    # Shutdown


app = FastAPI(
    title="PHISHGUARD//NEXUS API",
    description="Explainable AI Phishing & Scam Detection Platform",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if isinstance(settings.CORS_ORIGINS, list) else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Evaluation Artifacts
project_root = Path(__file__).resolve().parent.parent.parent
eval_dir = project_root / "models" / "eval"
if not eval_dir.exists():
    eval_dir = Path("models/eval")
try:
    eval_dir.mkdir(parents=True, exist_ok=True)
except OSError:
    pass
if eval_dir.exists():
    app.mount("/static/eval", StaticFiles(directory=str(eval_dir)), name="eval_static")

# Include API Routers under /api and root
for prefix in ["/api", ""]:
    app.include_router(scan.router, prefix=prefix)
    app.include_router(history.router, prefix=prefix)
    app.include_router(system.router, prefix=prefix)
    app.include_router(model.router, prefix=prefix)
    app.include_router(report.router, prefix=prefix)


def _get_dashboard_response():
    index_file = Path(__file__).resolve().parent / "static" / "index.html"
    if index_file.exists():
        from fastapi.responses import HTMLResponse
        return HTMLResponse(content=index_file.read_text(encoding="utf-8"), status_code=200)
    return {
        "service": "PHISHGUARD//NEXUS API",
        "status": "online",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }


@app.get("/")
@app.get("/app")
def root_get():
    return _get_dashboard_response()


@app.api_route("/api/index", methods=["GET", "POST", "OPTIONS"])
@app.api_route("/api/index.py", methods=["GET", "POST", "OPTIONS"])
async def root_index(request: Request):
    if request.method == "POST":
        return JSONResponse(content={
            "debug": True,
            "scope_path": request.scope.get("path"),
            "headers": dict(request.headers)
        })
    return _get_dashboard_response()


@app.middleware("http")
async def vercel_path_rewrite_middleware(request: Request, call_next):
    matched = (
        request.headers.get("x-matched-path")
        or request.headers.get("x-forwarded-uri")
        or request.headers.get("x-rewrite-url")
    )
    if matched:
        clean_path = matched.split("?")[0]
        if clean_path and not clean_path.startswith("/api/index"):
            request.scope["path"] = clean_path
    response = await call_next(request)
    return response


@app.get("/{full_path:path}")
def catch_all_get(full_path: str):
    if not full_path.startswith("api/") and not full_path.startswith("static/"):
        return _get_dashboard_response()
    return JSONResponse(status_code=404, content={"detail": "Not Found"})


# Standard Error Envelope Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": str(exc),
                "detail": None
            }
        }
    )
