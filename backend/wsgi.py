"""
WSGI entrypoint for production servers (e.g., gunicorn).

This module exposes the Flask application instance as `app` so that process
managers can import it without executing the development server.

This does not change API behavior; it only provides an importable entrypoint.
"""

from app import app  # noqa: F401
