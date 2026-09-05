"""Karta assembly service.

Tools:
  whoami                 Confirms sign-in and Graph consent. Returns the member's name and email.
  assemble_status_deck   Approved values in; deck built, optimized, written to SharePoint as the member.

Configuration is by environment variable. Secrets arrive from Google Secret Manager at deploy time.
"""
from __future__ import annotations

import base64
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

AUTH_MODE = os.environ.get("AUTH_MODE", "entra")  # entra | none (interim, download delivery only)
MCP_PATH = os.environ.get("MCP_PATH", "/mcp")
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


def caller_identity() -> tuple[Optional[str], dict]:
    if AUTH_MODE == "none":
        return None, {}
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
    from karta_assembler.deck import DEFAULT_TEMPLATE
    if not DEFAULT_TEMPLATE.exists():
        raise RuntimeError(f"Bundled template missing at {DEFAULT_TEMPLATE}. Refusing to start.")
    # Stateless HTTP: every request stands alone, so a cold start or a new instance never turns a
    # connector's remembered session into a 404 (observed September 5, 2026 as "Connector is temporarily unavailable").
    mcp = FastMCP("Karta Assembly", auth=build_auth() if AUTH_MODE != "none" else None, stateless_http=True)

    @mcp.custom_route("/status", methods=["GET"])
    async def status(_: Request) -> JSONResponse:
        return JSONResponse({"ok": True, "service": "karta-assembly", "version": SERVICE_VERSION})

    @mcp.tool
    async def whoami() -> dict:
        """Confirm the signed-in member and that the service may act for them in Microsoft Graph."""
        upstream, claims = caller_identity()
        if AUTH_MODE == "none":
            return {"state": "ok", "auth_mode": "none", "delivery": "download", "service_version": SERVICE_VERSION,
                    "note": "Interim mode: no sign-in, decks are returned to the page for the member to save."}
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                gt = await graph.graph_token(obo_config(), upstream, client)
                profile = await graph.me(gt, client)
        except graph.GraphError as e:
            return failed(e.code, e.message, signed_in_as=member_email(claims))
        return {"state": "ok", "signed_in_as": member_email(claims, profile), "display_name": profile.get("displayName"), "graph_consent": "granted", "service_version": SERVICE_VERSION}

    @mcp.tool
    async def assemble_status_deck(approved_values: dict, base_deck: Optional[dict] = None, destination: Optional[dict] = None,
                                   delivery: str = "sharepoint", conflict_behavior: str = "rename",
                                   optimize: bool = True, drop_vector_logos: bool = False) -> dict:
        """Build the Project Status deck from approved values.

        approved_values: the approved-values document (contracts v1). Refused unless it carries a named approval and its derived fields match their inputs.
        base_deck: optional {"drive_id", "item_id"} of last week's deck. Fetched as the signed-in member. When omitted, or when the service runs without sign-in, the bundled KCG template is the base.
        destination: {"drive_id", "folder_item_id"} of the SharePoint folder, required for delivery "sharepoint".
        delivery: "sharepoint" saves the deck as the signed-in member and returns the link. "download" returns the deck bytes as base64 for the page to hand to the member. Without sign-in only "download" is possible.
        Returns a deck-job style result with state Built or Failed.
        """
        upstream, claims = caller_identity()
        started = datetime.now(timezone.utc).isoformat()
        if conflict_behavior not in ("rename", "replace", "fail"):
            return failed("bad_request", "conflict_behavior must be rename, replace, or fail.")
        if AUTH_MODE == "none":
            delivery = "download"
        if delivery not in ("sharepoint", "download"):
            return failed("bad_request", "delivery must be sharepoint or download.")
        item: dict = {}
        try:
            async with httpx.AsyncClient(timeout=120) as client:
                gt = None
                base = None
                if upstream is not None and base_deck:
                    gt = await graph.graph_token(obo_config(), upstream, client)
                    base = await graph.download_item(gt, base_deck["drive_id"], base_deck["item_id"], client)
                data, manifest = build_deck(base, approved_values)
                report = None
                if optimize:
                    data, report = optimize_pptx(data, drop_svg=drop_vector_logos)
                if delivery == "sharepoint":
                    if not destination:
                        return failed("bad_request", "destination is required to save to SharePoint.")
                    gt = gt or await graph.graph_token(obo_config(), upstream, client)
                    item = await graph.upload_file(gt, destination["drive_id"], destination["folder_item_id"], manifest.filename, data, client, conflict=conflict_behavior)
        except ApprovedValuesError as e:
            return failed("approved_values_rejected", str(e))
        except graph.GraphError as e:
            return failed(e.code, e.message)
        except KeyError as e:
            return failed("bad_request", f"Missing field {e.args[0]!r} in the request.")
        except FileNotFoundError as e:
            return failed("service_misconfigured", "The service is missing its base template. This is a deployment problem, not something in your values.")
        except Exception as e:  # never let a raw exception reach the member
            return failed("service_error", f"The deck could not be built: {type(e).__name__}. The service owner has the details.")
        deck = {
            "filename": item.get("name", manifest.filename),
            "size_bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "written_as": member_email(claims) if upstream else None,
            "base": "sharepoint_deck" if base is not None else "bundled_template",
        }
        if delivery == "sharepoint":
            deck["sharepoint_web_url"] = item.get("webUrl")
            deck["sharepoint_item_id"] = item.get("id")
        else:
            deck["content_base64"] = base64.b64encode(data).decode("ascii")
        return {
            "state": "Built",
            "delivery": delivery,
            "auth_mode": AUTH_MODE,
            "deck": deck,
            "warnings": manifest.warnings,
            "optimization": report,
            "approved_values_sha256": manifest.approved_values_sha256,
            "requested_at": started,
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "service_version": SERVICE_VERSION,
        }

    return mcp


if __name__ == "__main__":
    create_app().run(transport="http", host="0.0.0.0", port=int(os.environ.get("PORT", "8080")), path=MCP_PATH)
