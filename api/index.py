from fastapi import FastAPI, Query, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI(
    title="Minimal PyPI Stats API Wrapper",
    description="A lightweight FastAPI proxy for fetching PyPI download statistics.",
    version="1.0.0"
)

# ---------------------------------
# CORS FIX (works with Vercel + React)
# ---------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # allow all for now, you can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Vercel preflight handler
@app.options("/{rest_of_path:path}", include_in_schema=False)
async def preflight_handler(rest_of_path: str):
    response = Response()
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

# ---------------------------------
# YOUR ORIGINAL CODE (unchanged)
# ---------------------------------

BASE_EXTERNAL_API = "https://pypistats.org/api"


async def forward_request(endpoint: str, params: dict):
    """Forward the request to the real PyPI Stats API."""
    url = f"{BASE_EXTERNAL_API}/{endpoint}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    if response.status_code != 200:
        try:
            detail = response.json()
        except Exception:
            detail = response.text
        raise HTTPException(status_code=response.status_code, detail=detail)

    return response.json()


@app.get("/", tags=["Root"], summary="API Root Info")
async def root():
    """Return basic API information."""
    return {
        "message": "Minimal PyPI Stats API Wrapper",
        "docs": "/docs",
        "routes": {
            "recent": "/api/packages/{package}/recent",
            "overall": "/api/packages/{package}/overall",
            "python_major": "/api/packages/{package}/python_major",
            "python_minor": "/api/packages/{package}/python_minor",
            "system": "/api/packages/{package}/system",
        }
    }


@app.get("/api/packages/{package}/recent", tags=["Downloads"], summary="Recent download totals")
async def recent(package: str, period: str | None = Query(None, description="day, week, month", example="month")):
    params = {"period": period} if period else {}
    return await forward_request(f"packages/{package}/recent", params)


@app.get("/api/packages/{package}/overall", tags=["Downloads"], summary="Daily overall downloads")
async def overall(package: str, mirrors: str | None = Query(None, description="true/false", example="false")):
    params = {"mirrors": mirrors} if mirrors else {}
    return await forward_request(f"packages/{package}/overall", params)


@app.get("/api/packages/{package}/python_major", tags=["Breakdown"], summary="Downloads by Python major version")
async def python_major(package: str, version: str | None = Query(None, example="3")):
    params = {"version": version} if version else {}
    return await forward_request(f"packages/{package}/python_major", params)


@app.get("/api/packages/{package}/python_minor", tags=["Breakdown"], summary="Downloads by Python minor version")
async def python_minor(package: str, version: str | None = Query(None, example="3.10")):
    params = {"version": version} if version else {}
    return await forward_request(f"packages/{package}/python_minor", params)


@app.get("/api/packages/{package}/system", tags=["Breakdown"], summary="Downloads by operating system")
async def system(package: str, os: str | None = Query(None, example="Windows")):
    params = {"os": os} if os else {}
    return await forward_request(f"packages/{package}/system", params)
