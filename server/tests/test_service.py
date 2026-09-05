import asyncio
import os

import pytest

os.environ.setdefault("AZURE_CLIENT_ID", "00000000-0000-0000-0000-000000000000")
os.environ.setdefault("AZURE_TENANT_ID", "11111111-1111-1111-1111-111111111111")
os.environ.setdefault("AZURE_CLIENT_SECRET", "test-secret-not-real")
os.environ.setdefault("BASE_URL", "https://example.test")

from karta_service import graph  # noqa: E402
from karta_service.app import create_app, failed, member_email  # noqa: E402


def test_obo_form_targets_graph_scopes():
    cfg = graph.OboConfig("t", "c", "s", scopes=("User.Read", "Files.ReadWrite.All"))
    f = cfg.obo_form("tok")
    assert f["requested_token_use"] == "on_behalf_of" and f["assertion"] == "tok"
    assert f["scope"] == "https://graph.microsoft.com/User.Read https://graph.microsoft.com/Files.ReadWrite.All"
    assert cfg.token_endpoint.endswith("/t/oauth2/v2.0/token")


def test_upload_url_encodes_filename_and_conflict():
    u = graph.upload_url("d1", "f1", "KCG_Status TestCo 9-4-2026.pptx")
    assert u.endswith("/drives/d1/items/f1:/KCG_Status%20TestCo%209-4-2026.pptx:/content?@microsoft.graph.conflictBehavior=rename")
    assert graph.upload_url("d", "f", "a.pptx", "replace").endswith("=replace")


def test_member_email_prefers_graph_profile_then_claims():
    assert member_email({"preferred_username": "a@k.com"}) == "a@k.com"
    assert member_email({"preferred_username": "a@k.com"}, {"mail": "b@k.com"}) == "b@k.com"
    assert member_email({}, {"userPrincipalName": "c@k.com"}) == "c@k.com"


def test_failed_shape_carries_owner_and_route():
    r = failed("x", "plain words")
    assert r["state"] == "Failed" and r["error"]["owner"] and r["error"]["support_route"] and r["error"]["message"] == "plain words"


def test_app_constructs_and_exposes_tools():
    from fastmcp import Client
    app = create_app()

    async def names():
        async with Client(app) as c:
            return sorted(t.name for t in await c.list_tools())

    assert asyncio.run(names()) == ["assemble_status_deck", "whoami"]


def test_none_mode_builds_from_bundled_template_and_returns_bytes(monkeypatch):
    import asyncio, base64, importlib, sys
    monkeypatch.setenv("AUTH_MODE", "none")
    sys.modules.pop("karta_service.app", None)
    app_mod = importlib.import_module("karta_service.app")
    app = app_mod.create_app()
    sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2] / "assembler" / "tests"))
    from test_deck import approved
    from fastmcp import Client

    async def run():
        async with Client(app) as c:
            who = await c.call_tool("whoami", {})
            r = await c.call_tool("assemble_status_deck", {"approved_values": approved()})
            return who.data, r.data

    who, res = asyncio.run(run())
    assert who["auth_mode"] == "none"
    assert res["state"] == "Built" and res["delivery"] == "download" and res["deck"]["base"] == "bundled_template"
    raw = base64.b64decode(res["deck"]["content_base64"])
    assert raw[:2] == b"PK" and len(raw) == res["deck"]["size_bytes"] and len(raw) < 1_500_000
    sys.modules.pop("karta_service.app", None)
