"""
python-pptx helpers for the browser (claude.ai) build of weekly-status-deck.

This is the python-pptx equivalent of the desktop skill's
pptx-com-helpers.ps1. It exists because claude.ai's code-execution
sandbox has no PowerShell and no PowerPoint COM -- python-pptx (plus, for
cross-presentation slide copies, direct XML manipulation via lxml, which
python-pptx is built on) is what's actually available there.

Import style matches the PowerShell file's spirit: one flat module of
small, single-purpose functions, each documented with the gotcha it
exists to work around. Read the whole file before using it -- several
functions exist specifically because the obvious python-pptx approach
silently does the wrong thing.

Indexing gotcha up front, because it WILL bite a straight port of the
PowerShell skill: python-pptx is 0-indexed everywhere (table.cell(0, 0),
prs.slides[0]), while the COM helpers this was ported from are 1-indexed
(tbl.Cell(1,1), Slides.Item(1)). Every row/column/slide number quoted in
the browser SKILL.md's "known-good" tables is written 1-indexed to match
the original deck inspection notes -- subtract 1 before indexing into
python-pptx collections.
"""

import copy
from pptx.util import Emu
from pptx.enum.shapes import MSO_CONNECTOR
from pptx.oxml.ns import qn


def find_shape_by_exact_text(slide, text):
    """Returns the first shape on `slide` whose text, stripped, exactly
    equals `text`. python-pptx equivalent of Get-ShapeByExactText."""
    for shape in slide.shapes:
        if shape.has_text_frame and shape.text_frame.text.strip() == text:
            return shape
    return None


def _shape_contains_text(shape, substring):
    if shape.has_text_frame and substring in shape.text_frame.text:
        return True
    if shape.shape_type == 6:  # MSO_SHAPE_TYPE.GROUP
        for child in shape.shapes:
            if _shape_contains_text(child, substring):
                return True
    return False


def get_leaf_shapes_containing_text(slide, substring):
    """Recurses into groups and returns the actual text-holding leaf
    shapes containing `substring` -- python-pptx equivalent of
    Get-LeafShapesContainingText. Use this (not a group shape) when you
    intend to edit the text in place."""
    found = []

    def _walk(shape):
        if shape.has_text_frame and substring in shape.text_frame.text:
            found.append(shape)
        if shape.shape_type == 6:
            for child in shape.shapes:
                _walk(child)

    for top in slide.shapes:
        _walk(top)
    return found


def replace_text_in_run(shape, find, replace):
    """Replaces the first occurrence of `find` with `replace`, preserving
    that run's own formatting -- IF the target string lives entirely
    inside a single run.

    Gotcha: unlike COM's TextRange.Find (which searches across run
    boundaries transparently), python-pptx runs are the atomic unit --
    if PowerPoint split "Week of 8/10" across two runs (common after any
    manual edit in the desktop app touches part of a text box), a
    substring search per-run will miss it even though shape.text_frame.text
    shows the full string. If this returns False, fall back to reading
    paragraph.runs directly, or accept that you'll rebuild the whole
    paragraph (losing per-run formatting) via set_cell_text-style
    whole-text replacement instead.
    """
    if not shape.has_text_frame:
        return False
    for para in shape.text_frame.paragraphs:
        for run in para.runs:
            if find in run.text:
                run.text = run.text.replace(find, replace, 1)
                return True
    return False


def set_cell_text(table, row_1indexed, col_1indexed, text):
    """Sets a table cell's text, 1-indexed to match the desktop skill's
    SKILL.md (which quotes COM's 1-indexed Cell(r,c) throughout).
    This replaces the cell's ENTIRE text and default-formats it --
    it does not preserve an existing run's bold/color the way
    replace_text_in_run does. Use for full-value overwrites (a date, a
    status word), not for edits inside a longer formatted sentence."""
    table.cell(row_1indexed - 1, col_1indexed - 1).text = text


def get_cell_text_frame(table, row_1indexed, col_1indexed):
    """Returns the cell's text_frame for paragraph-level editing (the
    accomplishments/planned bulleted lists need this, not set_cell_text)."""
    return table.cell(row_1indexed - 1, col_1indexed - 1).text_frame


def rewrite_bulleted_cell(text_frame, items, bold_first=False):
    """Replaces a cell's bulleted paragraph list with `items`, keeping the
    cell's existing bullet/paragraph formatting (font size, indent,
    bullet character) by re-using paragraph 1's XML as the template for
    every paragraph instead of creating fresh ones from scratch.

    python-pptx equivalent of the desktop skill's "Step 3: bulleted text
    -- safe pattern" (set paragraph 1 directly, delete the rest from the
    end backwards, then clone paragraph 1's <a:pPr> for each new one).
    Mirrors that same delete-from-the-end order for the same reason: the
    template's own paragraph list still needs trimming down to `len(items)`
    paragraphs, and deleting from the front shifts indices under you.

    Set bold_first=True to bold the ENTIRE first item (matches the
    template's bold inline-label convention) -- bolds only after all
    paragraphs are in place, same reasoning as the PowerShell version:
    bolding paragraph 1 before using it as the clone source for
    InsertAfter-equivalents would make every subsequent item bold too.
    """
    paragraphs = text_frame.paragraphs
    template_pPr = None
    p0 = paragraphs[0]._p
    pPr = p0.find(qn('a:pPr'))
    if pPr is not None:
        template_pPr = copy.deepcopy(pPr)

    # Trim extra paragraphs from the end, keep paragraph 1 as the template.
    txBody = text_frame._txBody
    while len(text_frame.paragraphs) > 1:
        last_p = text_frame.paragraphs[-1]._p
        txBody.remove(last_p)

    # Set paragraph 1's text via its first run (clears existing runs first
    # so we don't leave stale runs with old formatting sitting alongside).
    p = text_frame.paragraphs[0]
    for r in list(p.runs):
        r._r.getparent().remove(r._r)
    run = p.add_run()
    run.text = items[0]

    # Clone paragraph 1's XML (now holding item 1's text+pPr) for every
    # remaining item, then overwrite each clone's run text.
    template_p = copy.deepcopy(p._p)
    for item in items[1:]:
        new_p = copy.deepcopy(template_p)
        txBody.append(new_p)
        # find the run inside the freshly appended paragraph and set its text
        for r_el in new_p.findall(qn('a:r')):
            t_el = r_el.find(qn('a:t'))
            t_el.text = item
            break

    if bold_first:
        for r in text_frame.paragraphs[0].runs:
            r.font.bold = True


def copy_slide_from_external(dest_prs, src_prs, src_slide_index_0based, layout_index=6):
    """Copies one whole slide from `src_prs` into `dest_prs`, appended at
    the end. Returns the new slide.

    python-pptx has NO built-in cross-presentation slide copy (unlike
    COM's Slides.Item(n).Copy() / Paste()) -- this is the single biggest
    mechanical gap vs. the desktop skill, and the reason this function
    exists instead of a one-liner. Approach: add a blank slide off
    `layout_index` (default 6 = usually "Blank" -- verify against the
    actual template's slide_layouts before relying on this), strip
    whatever placeholder shapes that layout injected, then deep-copy each
    top-level shape's XML from the source slide onto the new one.

    Handles, by shape type:
    - Tables (graphicFrame): self-contained XML, deep-copy works as-is.
    - Text boxes, autoshapes, groups: self-contained XML, deep-copy works.
    - Pictures: NOT self-contained -- a picture shape's XML only holds an
      r:embed relationship ID, which is meaningless copied into a
      different package. This function re-adds the image part to
      dest_prs's package and rewrites the copied shape's relationship ID
      to point at it. If a slide has pictures nested inside a GROUP
      shape, this only fixes top-level picture shapes -- check for that
      case on the actual template before trusting this blindly (Cinemark's
      real logo lives as a plain top-level Picture, not grouped, as of
      the 2026-08 builds, but re-verify per client).

    Untested end-to-end in a real claude.ai sandbox as of first-write
    (2026-08-20) -- there is no Python on the machine this was authored
    on. Validate against a real Design Document / previous-deck file
    before trusting this on a client-facing build; see "Verification
    before calling it done" in SKILL.md.
    """
    src_slide = src_prs.slides[src_slide_index_0based]
    blank_layout = dest_prs.slide_layouts[layout_index]
    dest_slide = dest_prs.slides.add_slide(blank_layout)

    # Strip placeholder shapes the layout auto-populated onto the new slide.
    for shape in list(dest_slide.shapes):
        shape._element.getparent().remove(shape._element)

    for shape in src_slide.shapes:
        new_el = copy.deepcopy(shape._element)
        dest_slide.shapes._spTree.append(new_el)

        if shape.shape_type == 13:  # MSO_SHAPE_TYPE.PICTURE
            image_part = shape.image
            new_image_part, new_rId = dest_slide.part.get_or_add_image_part(
                image_part.blob
            ) if hasattr(dest_slide.part, "get_or_add_image_part") else (None, None)
            if new_rId is None:
                # Fallback for python-pptx versions without get_or_add_image_part
                # on the slide part directly -- go through the package's
                # image parts collection instead.
                image_parts = dest_prs.part.package.image_parts
                new_image_part = image_parts.get_or_add_image_part(image_part.blob)
                new_rId = dest_slide.part.relate_to(new_image_part,
                    "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image")
            blip = new_el.find('.//' + qn('a:blip'))
            if blip is not None:
                blip.set(qn('r:embed'), new_rId)

    return dest_slide


def add_position_marker(slide, left_emu, top_emu, bottom_emu, rgb=(0x21, 0xa1, 0x99)):
    """Adds a vertical dashed straight connector spanning top_emu..bottom_emu
    at horizontal position left_emu. python-pptx equivalent of the
    desktop skill's Slide 3 "today" marker (AddConnector + Line.DashStyle
    = msoLineDash + Line.ForeColor.RGB).

    Gotcha: python-pptx's LineFormat has no public `.dash_style` setter in
    all released versions -- if `connector.line.dash_style = ...` isn't
    available in whatever version the sandbox has, set the OOXML
    <a:prstDash val="dash"/> element directly instead (done below via
    oxml so this works regardless of python-pptx version).

    rgb defaults to the template's "Yellow" status color used elsewhere
    in this deck (RGB int 2204889 in the COM skill == (0x21, 0xa1, 0x99)
    little-endian-decoded -- reuse RGBColor(0x21, 0xa1, 0x99) rather than
    a new literal, matching the desktop skill's own rule to reuse that
    constant.
    """
    from pptx.util import Pt

    height = bottom_emu - top_emu
    connector = slide.shapes.add_connector(
        MSO_CONNECTOR.STRAIGHT, left_emu, top_emu, left_emu, top_emu + height
    )
    connector.line.color.rgb.__class__  # no-op; keeps RGBColor import path documented
    from pptx.dml.color import RGBColor
    connector.line.color.rgb = RGBColor(*rgb)
    connector.line.width = Pt(1)

    ln = connector.line._get_or_add_ln()
    prstDash = ln.find(qn('a:prstDash'))
    if prstDash is None:
        prstDash = ln.makeelement(qn('a:prstDash'), {})
        ln.append(prstDash)
    prstDash.set('val', 'dash')

    return connector


def set_picture_size_preserve_aspect(picture_shape, target_width_emu, left_emu, top_emu):
    """python-pptx equivalent of Set-ShapeSize: resize preserving aspect
    ratio, capturing original width/height ONCE before mutating either --
    same double-scale trap the PowerShell version's docstring warns about
    applies here (picture_shape.width/.height don't auto-link to each
    other in python-pptx the way a COM shape with LockAspectRatio does,
    but computing both from a stale re-read is still an easy mistake to
    reintroduce if this gets edited later)."""
    orig_width = picture_shape.width
    orig_height = picture_shape.height
    ratio = target_width_emu / orig_width
    picture_shape.width = Emu(int(target_width_emu))
    picture_shape.height = Emu(int(orig_height * ratio))
    picture_shape.left = Emu(int(left_emu))
    picture_shape.top = Emu(int(top_emu))


def try_export_slide_png(pptx_path, slide_1indexed, out_path):
    """Best-effort visual QA export. python-pptx CANNOT rasterize a slide
    to an image -- there is no pure-Python equivalent of COM's
    Slide.Export(). This shells out to LibreOffice headless conversion,
    which may or may not be present in a given claude.ai sandbox.

    Returns True if it worked, False if soffice isn't available or the
    conversion failed -- callers MUST handle the False case by falling
    back to structural/text-content verification (row counts, cell text
    dumps) instead of visual QA, and should say so explicitly rather than
    silently skipping verification. See "Verification before calling it
    done" in SKILL.md -- this is the biggest known gap vs. the desktop
    skill's Export-SlideImage, which always works because real PowerPoint
    is guaranteed present there.
    """
    import subprocess
    import shutil
    import os

    if shutil.which("soffice") is None:
        return False
    try:
        out_dir = os.path.dirname(out_path) or "."
        subprocess.run(
            ["soffice", "--headless", "--convert-to", "png", "--outdir", out_dir, pptx_path],
            check=True, timeout=60,
        )
        return os.path.exists(out_path)
    except Exception:
        return False
