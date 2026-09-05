"""Deck size optimization. Removes layouts no slide uses, drops media nothing references,
and recompresses raster images. Vector logos are kept by default because they are the brand.
Measured on the sample deck: 8.5 MB to 0.70 MiB with logos kept."""
from __future__ import annotations

import io
import posixpath
import re
import zipfile
from collections import defaultdict

from PIL import Image

MAX_EDGE = 1920
JPEG_QUALITY = 85


def _relpath(part: str) -> str:
    d, b = posixpath.split(part)
    return posixpath.join(d, "_rels", b + ".rels")


def _rels(parts: dict, part: str):
    r = _relpath(part)
    if r not in parts:
        return []
    out = []
    for m in re.finditer(r"<Relationship [^>]*/>", parts[r].decode("utf8")):
        t = m.group(0)
        if 'TargetMode="External"' in t:
            continue
        rid = re.search(r'Id="([^"]+)"', t).group(1)
        tgt = re.search(r'Target="([^"]+)"', t).group(1)
        ty = re.search(r'Type="[^"]*/([^"/]+)"', t).group(1)
        out.append((rid, ty, posixpath.normpath(posixpath.join(posixpath.dirname(part), tgt))))
    return out


def optimize_pptx(data: bytes, drop_svg: bool = False) -> tuple[bytes, dict]:
    z = zipfile.ZipFile(io.BytesIO(data))
    parts = {n: z.read(n) for n in z.namelist()}
    report = {"input_bytes": len(data)}

    slides = [n for n in parts if re.match(r"ppt/slides/slide\d+\.xml$", n)]
    layouts = [n for n in parts if re.match(r"ppt/slideLayouts/slideLayout\d+\.xml$", n)]
    masters = [n for n in parts if re.match(r"ppt/slideMasters/slideMaster\d+\.xml$", n)]
    used = {t for s in slides for _, ty, t in _rels(parts, s) if ty == "slideLayout"}
    for m in masters:
        lays = [t for _, ty, t in _rels(parts, m) if ty == "slideLayout"]
        if lays and not any(l in used for l in lays):
            used.add(lays[0])
    remove = {l for l in layouts if l not in used}
    for m in masters:
        xml = parts[m].decode("utf8"); rxml = parts[_relpath(m)].decode("utf8")
        for rid, ty, t in _rels(parts, m):
            if ty == "slideLayout" and t in remove:
                xml = re.sub(r'<p:sldLayoutId [^>]*r:id="%s"[^>]*/>' % rid, "", xml)
                rxml = re.sub(r'<Relationship [^>]*Id="%s"[^>]*/>' % rid, "", rxml)
        parts[m] = xml.encode("utf8"); parts[_relpath(m)] = rxml.encode("utf8")
    for l in remove:
        parts.pop(l, None); parts.pop(_relpath(l), None)
    report["layouts_removed"] = len(remove)

    if drop_svg:
        for p in list(parts):
            if not p.endswith(".xml") or "/_rels/" in p or "svgBlip" not in parts[p].decode("utf8", "ignore"):
                continue
            xml = parts[p].decode("utf8")
            rids = re.findall(r'<asvg:svgBlip[^>]*r:embed="([^"]+)"', xml)
            xml = re.sub(r'<a:ext uri="\{96DAC541-7B7A-43D3-8B79-37D633B846F1\}">.*?</a:ext>', "", xml, flags=re.S)
            xml = re.sub(r"<a:extLst>\s*</a:extLst>", "", xml)
            parts[p] = xml.encode("utf8")
            rxml = parts[_relpath(p)].decode("utf8")
            for rid in rids:
                rxml = re.sub(r'<Relationship [^>]*Id="%s"[^>]*/>' % rid, "", rxml)
            parts[_relpath(p)] = rxml.encode("utf8")

    ref = set()
    for p in [x for x in parts if x.endswith(".rels")]:
        base = p.replace("/_rels/", "/")[:-5]
        for m in re.finditer(r'Target="([^"]+)"', parts[p].decode("utf8")):
            t = posixpath.normpath(posixpath.join(posixpath.dirname(base), m.group(1)))
            if t.startswith("ppt/media/"):
                ref.add(t)
    orphan = [x for x in parts if x.startswith("ppt/media/") and x not in ref]
    for p in orphan:
        parts.pop(p)
    report["media_removed"] = len(orphan)

    ct = parts["[Content_Types].xml"].decode("utf8")
    renames = {}
    for p in [x for x in parts if x.startswith("ppt/media/") and x.lower().endswith((".png", ".jpg", ".jpeg"))]:
        raw = parts[p]
        try:
            im = Image.open(io.BytesIO(raw)); im.load()
        except Exception:
            continue
        w, h = im.size
        if max(w, h) > MAX_EDGE:
            r = MAX_EDGE / max(w, h); im = im.resize((round(w * r), round(h * r)), Image.LANCZOS)
        has_alpha = im.mode in ("RGBA", "LA") and im.getchannel("A").getextrema()[0] < 255
        cands = [("orig", raw)]
        if p.lower().endswith(".png"):
            b = io.BytesIO()
            (im.convert("RGBA").quantize(256, method=Image.FASTOCTREE) if has_alpha else im.convert("RGB")).save(b, "PNG", optimize=True)
            cands.append(("png", b.getvalue()))
        if not has_alpha:
            b = io.BytesIO(); im.convert("RGB").save(b, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
            cands.append(("jpg", b.getvalue()))
        kind, best = min(cands, key=lambda c: len(c[1]))
        if kind == "orig":
            continue
        newp = p
        if kind == "jpg" and not p.lower().endswith((".jpg", ".jpeg")):
            newp = posixpath.splitext(p)[0] + ".jpg"; renames[p] = newp
        parts.pop(p); parts[newp] = best
    for old, new in renames.items():
        ob, nb = posixpath.basename(old), posixpath.basename(new)
        for p in [x for x in parts if x.endswith(".rels")]:
            s = parts[p].decode("utf8")
            if ob in s:
                parts[p] = re.sub(r'Target="([^"]*/)?%s"' % re.escape(ob), lambda m: 'Target="%s%s"' % (m.group(1) or "", nb), s).encode("utf8")
    if renames and 'Extension="jpg"' not in ct:
        ct = ct.replace("</Types>", '<Default Extension="jpg" ContentType="image/jpeg"/></Types>')
    for m in re.finditer(r'<Override PartName="/([^"]+)"[^>]*/>', ct):
        if m.group(1) not in parts:
            ct = ct.replace(m.group(0), "")
    parts["[Content_Types].xml"] = ct.encode("utf8")

    order = [n for n in z.namelist() if n in parts] + [n for n in parts if n not in z.namelist()]
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as o:
        for n in order:
            o.writestr(n, parts[n])
    result = out.getvalue()
    report["output_bytes"] = len(result)
    return result, report
