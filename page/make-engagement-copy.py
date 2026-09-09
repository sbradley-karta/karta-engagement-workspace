#!/usr/bin/env python3
"""Produce a titled copy of the blank workspace page for one engagement's artifact.

Usage: python3 page/make-engagement-copy.py "Legend · Continuous Support" page/dist/legend-continuous-support.html
Then publish the output with the Artifact tool, passing that engagement's url from page/artifacts.json.
Only the <title> differs from page/engagement-workspace.html; the page retitles its own document on setup,
but the artifact's name in claude.ai is set by the publish, so the copy carries the name too.
"""
import pathlib, sys
if len(sys.argv) != 3:
    sys.exit(__doc__)
title, out = sys.argv[1], pathlib.Path(sys.argv[2])
src = pathlib.Path(__file__).with_name("engagement-workspace.html").read_text()
marker = "<title>Karta Engagement Workspace</title>"
if marker not in src:
    sys.exit("blank template title not found")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(src.replace(marker, "<title>" + title.replace("&", "&amp;").replace("<", "&lt;") + "</title>", 1))
print(out)
