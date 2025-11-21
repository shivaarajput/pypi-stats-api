from fastapi import FastAPI, Query, HTTPException
import httpx

app = FastAPI(
    title="Minimal PyPI Stats API Wrapper",
    description="A lightweight FastAPI proxy for fetching PyPI download statistics.",
    version="1.0.0"
)

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

# -------------------------
# Routes
# -------------------------

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

@app.get(
    "/api/packages/{package}/recent",
    tags=["Downloads"],
    summary="Recent download totals"
)
async def recent(
    package: str,
    period: str | None = Query(
        None,
        description="Time period: 'day', 'week', or 'month'",
        example="month"
    )
):
    """
    Retrieve aggregate download totals for the last 1/7/30 days.
    Mirrors are excluded.
    """
    params = {"period": period} if period else {}
    return await forward_request(f"packages/{package}/recent", params)


@app.get(
    "/api/packages/{package}/overall",
    tags=["Downloads"],
    summary="Daily overall downloads"
)
async def overall(
    package: str,
    mirrors: str | None = Query(
        None,
        description="Include mirror downloads? Options: 'true', 'false'",
        example="false"
    )
):
    """Retrieve the aggregate *daily* download time series."""
    params = {"mirrors": mirrors} if mirrors else {}
    return await forward_request(f"packages/{package}/overall", params)


@app.get(
    "/api/packages/{package}/python_major",
    tags=["Breakdown"],
    summary="Downloads by Python major version"
)
async def python_major(
    package: str,
    version: str | None = Query(
        None,
        description="Major Python version (e.g. '3')",
        example="3"
    )
):
    """Retrieve daily download stats grouped by Python *major* version."""
    params = {"version": version} if version else {}
    return await forward_request(f"packages/{package}/python_major", params)


@app.get(
    "/api/packages/{package}/python_minor",
    tags=["Breakdown"],
    summary="Downloads by Python minor version"
)
async def python_minor(
    package: str,
    version: str | None = Query(
        None,
        description="Minor Python version (e.g. '3.10')",
        example="3.10"
    )
):
    """Retrieve daily download stats grouped by Python *minor* version."""
    params = {"version": version} if version else {}
    return await forward_request(f"packages/{package}/python_minor", params)


@app.get(
    "/api/packages/{package}/system",
    tags=["Breakdown"],
    summary="Downloads by operating system"
)
async def system(
    package: str,
    os: str | None = Query(
        None,
        description="Operating system filter (e.g. 'Windows', 'Linux', 'Darwin')",
        example="Windows"
    )
):
    """Retrieve daily download stats grouped by operating system."""
    params = {"os": os} if os else {}
    return await forward_request(f"packages/{package}/system", params)
