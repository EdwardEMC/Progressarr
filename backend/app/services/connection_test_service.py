import httpx
from pydantic import BaseModel, Field


class ConnectionTestRequest(BaseModel):
    url: str = Field(min_length=1)
    api_key: str = Field(min_length=1)


class ConnectionTestResponse(BaseModel):
    success: bool
    message: str


async def test_connection(
    *,
    url: str,
    api_key: str,
    service: str,
) -> ConnectionTestResponse:
    base_url = url.rstrip("/")

    try:
        async with httpx.AsyncClient(
            timeout=10.0,
        ) as client:
            response = await client.get(
                f"{base_url}/api/v3/system/status",
                headers={
                    "X-Api-Key": api_key,
                },
            )

            if response.status_code == 401:
                return ConnectionTestResponse(
                    success=False,
                    message=f"{service} rejected the API key.",
                )

            response.raise_for_status()

            return ConnectionTestResponse(
                success=True,
                message=f"Successfully connected to {service}.",
            )

    except httpx.ConnectError:
        return ConnectionTestResponse(
            success=False,
            message=f"Unable to connect to {service}.",
        )

    except httpx.TimeoutException:
        return ConnectionTestResponse(
            success=False,
            message=f"{service} connection timed out.",
        )

    except httpx.HTTPStatusError as exc:
        return ConnectionTestResponse(
            success=False,
            message=(f"{service} returned HTTP {exc.response.status_code}."),
        )

    except httpx.HTTPError:
        return ConnectionTestResponse(
            success=False,
            message=f"Unable to communicate with {service}.",
        )


async def test_jellyfin_connection(
    *,
    url: str,
    api_key: str,
) -> ConnectionTestResponse:
    base_url = url.rstrip("/")

    try:
        async with httpx.AsyncClient(
            timeout=10.0,
        ) as client:
            response = await client.get(
                f"{base_url}/System/Info",
                headers={
                    "X-Emby-Token": api_key,
                },
            )

            if response.status_code in {401, 403}:
                return ConnectionTestResponse(
                    success=False,
                    message="Jellyfin rejected the API key.",
                )

            response.raise_for_status()

            return ConnectionTestResponse(
                success=True,
                message="Successfully connected to Jellyfin.",
            )

    except httpx.ConnectError:
        return ConnectionTestResponse(
            success=False,
            message="Unable to connect to Jellyfin.",
        )

    except httpx.TimeoutException:
        return ConnectionTestResponse(
            success=False,
            message="Jellyfin connection timed out.",
        )

    except httpx.HTTPStatusError as exc:
        return ConnectionTestResponse(
            success=False,
            message=(f"Jellyfin returned HTTP {exc.response.status_code}."),
        )

    except httpx.HTTPError:
        return ConnectionTestResponse(
            success=False,
            message="Unable to communicate with Jellyfin.",
        )


async def test_seerr_connection(
    *,
    url: str,
    api_key: str,
) -> ConnectionTestResponse:
    base_url = url.rstrip("/")

    try:
        async with httpx.AsyncClient(
            timeout=10.0,
        ) as client:
            response = await client.get(
                f"{base_url}/api/v1/status",
                headers={
                    "X-Api-Key": api_key,
                },
            )

            if response.status_code in {401, 403}:
                return ConnectionTestResponse(
                    success=False,
                    message="Seerr rejected the API key.",
                )

            response.raise_for_status()

            return ConnectionTestResponse(
                success=True,
                message="Successfully connected to Seerr.",
            )

    except httpx.ConnectError:
        return ConnectionTestResponse(
            success=False,
            message="Unable to connect to Seerr.",
        )

    except httpx.TimeoutException:
        return ConnectionTestResponse(
            success=False,
            message="Seerr connection timed out.",
        )

    except httpx.HTTPStatusError as exc:
        return ConnectionTestResponse(
            success=False,
            message=f"Seerr returned HTTP {exc.response.status_code}.",
        )

    except httpx.HTTPError:
        return ConnectionTestResponse(
            success=False,
            message="Unable to communicate with Seerr.",
        )
