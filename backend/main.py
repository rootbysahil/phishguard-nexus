"""
PHISHGUARD//NEXUS - Convenience Runner
Run with: python backend/main.py
"""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import uvicorn
from backend.app.core.config import settings

if __name__ == "__main__":
    print(f"[*] Starting PHISHGUARD//NEXUS on http://localhost:{settings.PORT}")
    print(f"[*] UI Dashboard: http://localhost:{settings.PORT}/")
    print(f"[*] OpenAPI Docs: http://localhost:{settings.PORT}/docs")
    uvicorn.run("backend.app.main:app", host=settings.HOST, port=settings.PORT, reload=False)
