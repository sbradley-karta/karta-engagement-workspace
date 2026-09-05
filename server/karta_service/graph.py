"""Microsoft Graph access on behalf of the signed-in member.

The service never holds a Microsoft credential of its own beyond the Entra app's client secret.
Every Graph call runs with a token obtained by on-behalf-of exchange from the member's own
sign-in token, so files are written as the member.
"""
from __future__ import annotations

import hashlib
import time
import urllib.parse
from dataclasses import dataclass
from typing import Optional

import httpx

GRAPH = "https://graph.microsoft.com/v1.0"
SIMPLE_UPLOAD_LIMIT = 4 * 1024 * 1024
CHUNK = 5 * 320 * 1024  # Graph requires multiples of 320 KiB


class GraphError(RuntimeError):
    def __init__(self, code: str, message: str, status: Optional[int] = None):
        super().__init__(message)
        self.code, self.status = code, status


@dataclass
class OboConfig:
    tenant_id: str
    client_id: str
    client_secret: str
    scopes: tuple[str, ...] = ("User.Read", "Files.ReadWrite.All")

    @property
    def token_endpoint(self) -> str:
        return f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"

    def obo_form(self, assertion: str) -> dict:
        return {
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "assertion": assertion,
            "scope": " ".join(f"https://graph.microsoft.com/{s}" for s in self.scopes),
            "requested_token_use": "on_behalf_of",
        }


_cache: dict[str, tuple[str, float]] = {}


async def graph_token(cfg: OboConfig, upstream_token: str, client: Optional[httpx.AsyncClient] = None) -> str:
    """Exchange the member's API token for a Graph token. Cached until a minute before expiry."""
    key = hashlib.sha256(upstream_token.encode()).hexdigest()
    hit = _cache.get(key)
    if hit and hit[1] > time.time() + 60:
        return hit[0]
    own = client is None
    client = client or httpx.AsyncClient(timeout=30)
    try:
        r = await client.post(cfg.token_endpoint, data=cfg.obo_form(upstream_token))
    finally:
        if own:
            await client.aclose()
    if r.status_code != 200:
        body = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
        err = body.get("error", "obo_failed")
        desc = body.get("error_description", r.text[:300])
        if err in ("invalid_grant", "interaction_required") or "AADSTS65001" in desc:
            raise GraphError("consent_required", "Your Microsoft sign-in has not granted the service permission to write files. Sign out of the Karta Assembly connector and sign in again, accepting the file permission.", r.status_code)
        raise GraphError("obo_failed", f"Microsoft would not issue a Graph token: {err}. {desc}", r.status_code)
    tok = r.json()
    _cache[key] = (tok["access_token"], time.time() + int(tok.get("expires_in", 3600)))
    return tok["access_token"]


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def upload_url(drive_id: str, folder_item_id: str, filename: str, conflict: str = "rename") -> str:
    name = urllib.parse.quote(filename, safe="")
    return f"{GRAPH}/drives/{drive_id}/items/{folder_item_id}:/{name}:/content?@microsoft.graph.conflictBehavior={conflict}"


def session_url(drive_id: str, folder_item_id: str, filename: str) -> str:
    name = urllib.parse.quote(filename, safe="")
    return f"{GRAPH}/drives/{drive_id}/items/{folder_item_id}:/{name}:/createUploadSession"


async def me(token: str, client: httpx.AsyncClient) -> dict:
    r = await client.get(f"{GRAPH}/me?$select=displayName,mail,userPrincipalName", headers=_auth(token))
    _raise(r, "read your profile")
    return r.json()


async def download_item(token: str, drive_id: str, item_id: str, client: httpx.AsyncClient) -> bytes:
    r = await client.get(f"{GRAPH}/drives/{drive_id}/items/{item_id}/content", headers=_auth(token), follow_redirects=True)
    _raise(r, "read the base deck")
    return r.content


async def upload_file(token: str, drive_id: str, folder_item_id: str, filename: str, data: bytes,
                      client: httpx.AsyncClient, conflict: str = "rename") -> dict:
    if len(data) <= SIMPLE_UPLOAD_LIMIT:
        r = await client.put(upload_url(drive_id, folder_item_id, filename, conflict), headers={**_auth(token), "Content-Type": "application/vnd.openxmlformats-officedocument.presentationml.presentation"}, content=data)
        _raise(r, "save the deck to SharePoint")
        return r.json()
    r = await client.post(session_url(drive_id, folder_item_id, filename), headers=_auth(token),
                          json={"item": {"@microsoft.graph.conflictBehavior": conflict, "name": filename}})
    _raise(r, "start the SharePoint upload")
    url = r.json()["uploadUrl"]
    total = len(data)
    pos = 0
    last = None
    while pos < total:
        end = min(pos + CHUNK, total)
        last = await client.put(url, headers={"Content-Range": f"bytes {pos}-{end - 1}/{total}", "Content-Length": str(end - pos)}, content=data[pos:end])
        if last.status_code not in (200, 201, 202):
            _raise(last, "upload the deck to SharePoint")
        pos = end
    return last.json()


def _raise(r: httpx.Response, doing: str) -> None:
    if r.status_code < 400:
        return
    code = {401: "graph_unauthorized", 403: "graph_forbidden", 404: "graph_not_found", 423: "graph_locked", 429: "graph_throttled"}.get(r.status_code, "graph_error")
    try:
        detail = r.json().get("error", {}).get("message", "")
    except Exception:
        detail = r.text[:200]
    friendly = {
        "graph_forbidden": f"Microsoft would not let your account {doing}. Check that you have edit access to the engagement folder.",
        "graph_not_found": f"Could not {doing}: the SharePoint drive or folder in the engagement configuration was not found.",
        "graph_locked": f"Could not {doing}: the file is locked, usually because someone has it open.",
        "graph_throttled": f"Microsoft is rate limiting requests. Try again in a minute.",
    }.get(code, f"Could not {doing}. Microsoft said: {detail}")
    raise GraphError(code, friendly, r.status_code)
