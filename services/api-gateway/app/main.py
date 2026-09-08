import os
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

CATALOG_SERVICE_URL = os.getenv("CATALOG_SERVICE_URL", "http://localhost:8001")
PROGRESS_SERVICE_URL = os.getenv("PROGRESS_SERVICE_URL", "http://localhost:8002")
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")


class ProgressUpdate(BaseModel):
    completed: bool


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = httpx.AsyncClient(timeout=5.0)
    yield
    await app.state.http_client.aclose()


app = FastAPI(
    title="DevOps Learning Hub API Gateway",
    version="1.0.0",
    description="Single public API that coordinates the application services.",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["GET", "PUT"],
    allow_headers=["*"],
)


async def service_request(
    request: Request, method: str, url: str, **kwargs
) -> httpx.Response:
    try:
        response = await request.app.state.http_client.request(method, url, **kwargs)
        response.raise_for_status()
        return response
    except httpx.TimeoutException as error:
        raise HTTPException(status_code=504, detail="Downstream service timed out") from error
    except httpx.HTTPStatusError as error:
        detail = error.response.json().get("detail", "Downstream service error")
        raise HTTPException(status_code=error.response.status_code, detail=detail) from error
    except httpx.RequestError as error:
        raise HTTPException(status_code=503, detail="Downstream service unavailable") from error


@app.get("/health")
async def health(request: Request, response: Response) -> dict:
    services = {}
    for name, base_url in (
        ("catalog", CATALOG_SERVICE_URL),
        ("progress", PROGRESS_SERVICE_URL),
    ):
        try:
            result = await request.app.state.http_client.get(f"{base_url}/health")
            services[name] = result.json().get("status", "unknown")
        except (httpx.RequestError, ValueError):
            services[name] = "unavailable"
    healthy = all(status == "healthy" for status in services.values())
    if not healthy:
        response.status_code = 503
    return {
        "status": "healthy" if healthy else "degraded",
        "service": "api-gateway",
        "dependencies": services,
    }


@app.get("/api/v1/info")
def info() -> dict[str, str]:
    return {"name": "api-gateway", "version": "1.0.0"}


@app.get("/api/v1/labs")
async def labs(request: Request) -> list[dict]:
    catalog_response = await service_request(
        request, "GET", f"{CATALOG_SERVICE_URL}/api/v1/labs"
    )
    progress_response = await service_request(
        request, "GET", f"{PROGRESS_SERVICE_URL}/api/v1/progress"
    )
    progress_by_lab = {
        item["lab_id"]: item for item in progress_response.json()
    }
    return [
        {
            **lab,
            "completed": progress_by_lab.get(lab["id"], {}).get("completed", False),
        }
        for lab in catalog_response.json()
    ]


@app.put("/api/v1/labs/{lab_id}/progress")
async def update_progress(
    lab_id: int, payload: ProgressUpdate, request: Request
) -> dict:
    catalog_response = await service_request(
        request, "GET", f"{CATALOG_SERVICE_URL}/api/v1/labs/{lab_id}"
    )
    progress_response = await service_request(
        request,
        "PUT",
        f"{PROGRESS_SERVICE_URL}/api/v1/progress/{lab_id}",
        json=payload.model_dump(),
    )
    return {
        "lab": catalog_response.json(),
        "progress": progress_response.json(),
    }

