# DevOps Learning Hub

A small microservices application designed to be the workload for your DevOps
practice. The repository intentionally contains **application code only**.
Create the Dockerfiles, CI/CD pipelines, Kubernetes manifests, observability,
and cloud infrastructure yourself.

## Architecture

```text
Next.js UI (:3000)
       |
API Gateway (:8000)
   /             \
Catalog (:8001)  Progress (:8002)
                      |
                   SQLite
```

- `catalog-service`: serves the DevOps lab catalog.
- `progress-service`: stores a learner's completed labs.
- `api-gateway`: exposes one API to the UI and combines responses.
- `frontend`: Next.js and Tailwind dashboard.

Each Python service is independently runnable and has `/health` and
`/api/v1/info` endpoints. API documentation is available at `/docs`.

## Prerequisites

- Python 3.11+
- Node.js 20+

## Run the backend

Open three terminals from the repository root.

```bash
cd services/catalog-service
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

```bash
cd services/progress-service
python -m venv .venv
# activate the environment
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8002
```

```bash
cd services/api-gateway
python -m venv .venv
# activate the environment
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The gateway uses these defaults:

```text
CATALOG_SERVICE_URL=http://localhost:8001
PROGRESS_SERVICE_URL=http://localhost:8002
FRONTEND_ORIGIN=http://localhost:3000
```

## Run the frontend

```bash
cd frontend
npm install
copy .env.local.example .env.local
npm run dev
```

Open http://localhost:3000.

## Run backend tests

From each Python service directory:

```bash
pip install -r requirements-dev.txt
pytest
```

## Suggested DevOps exercises

1. Write a multi-stage Dockerfile for every component.
2. Run the system with Docker Compose and add health-based dependencies.
3. Add GitHub Actions for linting, tests, image builds, and security scans.
4. Create Kubernetes Deployments, Services, ConfigMaps, Secrets, and Ingress.
5. Add persistent storage for the progress database.
6. Add Prometheus metrics, Grafana dashboards, and centralized logs.
7. Configure readiness/liveness probes and horizontal autoscaling.
8. Package the manifests as a Helm chart.
9. Add blue/green or canary deployment.

