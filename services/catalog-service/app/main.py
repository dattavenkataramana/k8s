from typing import Literal

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


class Lab(BaseModel):
    id: int
    title: str
    description: str
    category: str
    difficulty: Literal["Beginner", "Intermediate", "Advanced"]
    duration_minutes: int
    tools: list[str]


LABS = [
    Lab(
        id=1,
        title="Containerize a FastAPI service",
        description="Create a secure multi-stage image and run it as a non-root user.",
        category="Containers",
        difficulty="Beginner",
        duration_minutes=45,
        tools=["Docker", "Python"],
    ),
    Lab(
        id=2,
        title="Compose the microservices",
        description="Connect the gateway, services, frontend, and persistent storage.",
        category="Containers",
        difficulty="Beginner",
        duration_minutes=60,
        tools=["Docker Compose", "Networking"],
    ),
    Lab(
        id=3,
        title="Deploy to Kubernetes",
        description="Write Deployments and Services with resource requests and limits.",
        category="Kubernetes",
        difficulty="Intermediate",
        duration_minutes=90,
        tools=["Kubernetes", "kubectl"],
    ),
    Lab(
        id=4,
        title="Configure probes and autoscaling",
        description="Add health probes and an HPA driven by application demand.",
        category="Kubernetes",
        difficulty="Intermediate",
        duration_minutes=75,
        tools=["Kubernetes", "HPA"],
    ),
    Lab(
        id=5,
        title="Build a CI/CD pipeline",
        description="Test, scan, build, publish, and deploy every service independently.",
        category="CI/CD",
        difficulty="Intermediate",
        duration_minutes=120,
        tools=["GitHub Actions", "Trivy"],
    ),
    Lab(
        id=6,
        title="Observe the platform",
        description="Collect metrics and logs, then build a useful service dashboard.",
        category="Observability",
        difficulty="Advanced",
        duration_minutes=120,
        tools=["Prometheus", "Grafana", "Loki"],
    ),
]

app = FastAPI(
    title="Catalog Service",
    version="1.0.0",
    description="Owns the DevOps lab catalog.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy", "service": "catalog-service"}


@app.get("/api/v1/info")
def info() -> dict[str, str]:
    return {"name": "catalog-service", "version": "1.0.0"}


@app.get("/api/v1/labs", response_model=list[Lab])
def list_labs(
    category: str | None = Query(default=None),
    difficulty: str | None = Query(default=None),
) -> list[Lab]:
    labs = LABS
    if category:
        labs = [lab for lab in labs if lab.category.lower() == category.lower()]
    if difficulty:
        labs = [lab for lab in labs if lab.difficulty.lower() == difficulty.lower()]
    return labs


@app.get("/api/v1/labs/{lab_id}", response_model=Lab)
def get_lab(lab_id: int) -> Lab:
    lab = next((item for item in LABS if item.id == lab_id), None)
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found")
    return lab

