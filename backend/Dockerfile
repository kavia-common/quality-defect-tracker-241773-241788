# syntax=docker/dockerfile:1.7
#
# Deterministic backend container build.
# This avoids platform "auto-detect" buildpacks potentially hanging during build/deploy.
#
# The app is still the same Flask application; we just run it with gunicorn for
# predictable production behavior.

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install dependencies first for better layer caching
COPY requirements.txt /app/requirements.txt

# Install build essentials only if needed for dependencies (kept minimal).
# Current requirements are pure-Python / manylinux wheels, so this should stay fast.
RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt && \
    pip install gunicorn==22.0.0

# Copy app source
COPY . /app

# Runtime configuration
ENV PORT=3001
EXPOSE 3001

# Use gunicorn (production WSGI server) rather than Flask dev server.
# Keep bind port aligned to $PORT used by most deployment systems.
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT} --workers 2 --threads 4 --timeout 60 wsgi:app"]
