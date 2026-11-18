# Dockerfile — packages app.py into a container image Kubernetes can run.
#
# Security choices baked in:
#   - a slim, pinned base image (smaller attack surface, reproducible)
#   - runs as a NON-root user (so a container breakout has fewer privileges)
#   - no extra packages (stdlib only), so nothing to patch or scan

FROM python:3.12-slim

# Create an unprivileged user to run the app.
RUN useradd --create-home --uid 10001 appuser

WORKDIR /app
COPY app/app.py /app/app.py

# Drop to the non-root user.
USER appuser

EXPOSE 8080
ENV PORT=8080

CMD ["python", "/app/app.py"]
