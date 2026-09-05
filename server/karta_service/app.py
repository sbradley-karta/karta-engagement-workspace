"""Karta assembly service.

Tools:
  whoami                 Confirms sign-in and Graph consent. Returns the member's name and email.
  assemble_status_deck   Approved values in; deck built, optimized, written to SharePoint as the member.

Configuration is by environment variable. Secrets arrive from Google Secret Manager at deploy time.
"""
from __future__ import annotations

import hashlib
import os
from datetime import datetime, timezone
from typing import Any, Optional

import httpx
from fastmcp import FastMCP
from fastmcp.server.auth.providers.azure import AzureProvider
from fastmcp.server.dependencies import get_access_token
from starlette.requests import Request
from starlette.responses import JSONResponse

from karta_assembler.deck import SERVICE_VERSION, ApprovedValuesError, build_deck
from karta_assembler.optimize import optimize_pptx

from . import graph

OWNER = os.environ.get("SUPPORT_OWNER", "Karta AI strategy")
SUPPORT = os.environ.get("SUPPORT_ROUTE", "Message Sean Bradley")


def build_auth() -> AzureProvider:
    """Microsoft Entra sign-in for the connector. Requires the Entra app to expose a custom scope
    (default 'assemble') and to have the Graph delegated permissions listed in GRAPH_SCOPES."""
    storage = None
    if os.environ.get("OAUTH_STORAGE", "memory") == "memory":
        from key_value.aio.stores.memory import MemoryStore
        storage = MemoryStore()
    graph_scopes = os.environ.get("GRAPH_SCOPES", "User.Read Files.ReadWrite.All").split()
    return AzureProvider(
        client_id=os.environ["AZURE_CLIENT_ID"],
        client_secret=os.environ["AZURE_CLIENT_SECRET"],
        tenant_id=os.environ["AZURE_TENANT_ID"],
        base_url=os.environ["BASE_URL"],
        required_scopes=[os.environ.get("REQUIRED_SCOPE", "assemble")],
        additional_authorize_scopes=graph_scopes + ["offline_access"],
        jwt_signing_key=os.environ.get("JWT_SIGNING_KEY") or None,
        client_storage=storage,
    )


def obo_config() -> graph.OboConfig:
    return graph.OboConfig(
        tenant_id=os.environ["AZURE_TENANT_ID"],
        client_id=os.environ["AZURE_CLIENT_ID"],
        client_secret=os.environ["AZURE_CLIENT_SECRET"],
        scopes=tuple(os.environ.get("GRAPH_SCOPES", "User.Read Files.ReadWrite.All").split()),
    )


def caller_identity() -> tuple[str, dict]:
    tok = get_access_token()
    if tok is None:
        raise PermissionError("No signed-in member on this request.")
    claims = tok.claims or {}
    return tok.token, claims


def member_email(claims: dict, profile: Optional[dict] = None) -> str:
    return (profile or {}).get("mail") or (profile or {}).get("userPrincipalName") or claims.get("preferred_username") or claims.get("upn") or ""


def failed(code: str, message: str, **extra: Any) -> dict:
    return {"state": "Failed", "error": {"code": code, "message": message, "owner": OWNER, "support_route": SUPPORT}, "service_version": SERVICE_VERSION, **extra}


def create_app() -> FastMCP:
    mcp = FastMCP("Karta Assembly", auth=build_auth())

    @mcp.custom_route("/healthz", methods=["GET"])
    async def healthz(_: Request) -> JSONResponse:
        return JSONResponse({"ok": True, "service": "karta-assembly", "version": SERVICE_VERSION})

    @mcp.tool
    async def whoami() -> dict:
        """Confirm the signed-in member and that the service may act for them in Microsoft Graph."""
        upstream, claims = caller_identity()
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                gt = await graph.graph_token(obo_config(), upstream, client)
                profile = await graph.me(gt, client)
        except graph.GraphError as e:
            return failed(e.code, e.message, signed_in_as=member_email(claims))
        return {"state": "ok", "signed_in_as": member_email(claims, profile), "display_name": profile.get("displayName"), "graph_consent": "granted", "service_version": SERVICE_VERSION}

    @mcp.tool
    async def assemble_status_deck(approved_values: dict, base_deck: dict, destination: dict,
                                   conflict_behavior: str = "rename", optimize: bool = True, drop_vector_logos: bool = False) -> dict:
        """Build the Project Status deck from approved values and save it to the engagement's SharePoint folder as the signed-in member.

        approved_values: the approved-values document (contracts v1). Refused unless it carries a named approval and its derived fields match their inputs.
        base_deck: {"drive_id", "item_id"} of last week's deck or the template to build from.
        destination: {"drive_id", "folder_item_id"} of the folder to save into.
        Returns a deck-job style result with state Built or Failed, the SharePoint link, size, hash, and warnings.
        """
        upstream, claims = caller_identity()
        started = datetime.now(timezone.utc).isoformat()
        if conflict_behavior not in ("rename", "replace", "fail"):
            return failed("bad_request", "conflict_behavior must be rename, replace, or fail.")
        try:
            async with httpx.AsyncClient(timeout=120) as client:
                gt = await graph.graph_token(obo_config(), upstream, client)
                base = await graph.download_item(gt, base_deck["drive_id"], base_deck["item_id"], client)
                data, manifest = build_deck(base, approved_values)
                report = None
                if optimize:
                    data, report = optimize_pptx(data, drop_svg=drop_vector_logos)
                item = await graph.upload_file(gt, destination["drive_id"], destination["folder_item_id"], manifest.filename, data, client, conflict=conflict_behavior)
        except ApprovedValuesError as e:
            return failed("approved_values_rejected", str(e))
        except graph.GraphError as e:
            return failed(e.code, e.message)
        except KeyError as e:
            return failed("bad_request", f"Missing field {e.args[0]!r} in the request.")
        return {
            "state": "Built",
            "deck": {
                "filename": item.get("name", manifest.filename),
                "size_bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
                "sharepoint_web_url": item.get("webUrl"),
                "sharepoint_item_id": item.get("id"),
                "written_as": member_email(claims),
            },
            "warnings": manifest.warnings,
            "optimization": report,
            "approved_values_sha256": manifest.approved_values_sha256,
            "requested_at": started,
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "service_version": SERVICE_VERSION,
        }

    return mcp


if __name__ == "__main__":
    create_app().run(transport="http", host="0.0.0.0", port=int(os.environ.get("PORT", "8080")), path="/mcp")
