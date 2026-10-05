import os

import httpx
from mcp.server import MCPServer

API_BASE_URL = os.getenv(
    "LUXURY_WATCH_API_BASE_URL",
    "https://api.dcanguven.workers.dev",
)

API_KEY = os.getenv("LUXURY_WATCH_API_KEY")

mcp = MCPServer("Luxury Watch Market Data")


def get_headers() -> dict[str, str]:
    if not API_KEY:
        raise RuntimeError(
            "LUXURY_WATCH_API_KEY environment variable is required."
        )

    return {
        "X-API-Key": API_KEY,
    }


async def get_json(
    path: str,
    *,
    authenticated: bool = False,
    params: dict | None = None,
) -> dict:
    headers = get_headers() if authenticated else None

    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(
            f"{API_BASE_URL}{path}",
            headers=headers,
            params=params,
        )

        response.raise_for_status()

        return response.json()


@mcp.tool()
async def search_watches(
    brand: str | None = None,
    model: str | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
    sort: str | None = None,
    order: str | None = None,
) -> dict:
    """Search historical luxury watch market records."""

    params = {
        "brand": brand,
        "model": model,
        "min_price": min_price,
        "max_price": max_price,
        "sort": sort,
        "order": order,
    }

    filtered_params = {
        key: value
        for key, value in params.items()
        if value is not None
    }

    return await get_json(
        "/api/v1/watches",
        authenticated=True,
        params=filtered_params,
    )


@mcp.tool()
async def get_watch(watch_id: int) -> dict:
    """Retrieve a single luxury watch market record by ID."""

    return await get_json(
        f"/api/v1/watches/{watch_id}",
        authenticated=True,
    )


@mcp.tool()
async def list_brands() -> dict:
    """List available luxury watch brands."""

    return await get_json(
        "/api/web/brands",
    )


@mcp.tool()
async def list_models(brand: str) -> dict:
    """List available watch models for a brand."""

    return await get_json(
        "/api/web/models",
        params={
            "brand": brand,
        },
    )


if __name__ == "__main__":
    mcp.run()