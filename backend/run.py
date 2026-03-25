"""
Flask backend entrypoint.

This backend is intentionally "demo-safe":
- No required external integrations
- Stable health check at `/`
- Stable OpenAPI + Swagger UI under `/docs`
"""

import os

from app import app


if __name__ == "__main__":
    # Demo-safe defaults: bind all interfaces and default to port 3001.
    # The orchestrator/environment may supply PORT.
    port = int(os.environ.get("PORT", "3001"))
    app.run(host="0.0.0.0", port=port)
