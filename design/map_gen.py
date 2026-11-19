"""Turns Natural Earth 110m land into an SVG path for the map panel.

The page is drawn at 1:1 with no network, so the coastlines are baked into the
HTML rather than fetched: this script reads a local copy of ne_110m_land.geojson,
simplifies each ring with a tolerance in degrees, projects it onto the panel box
and prints one <path> element with every landmass as a subpath.
"""

import json
from pathlib import Path

from shapely.geometry import shape

GEOJSON = Path("/tmp/ne_land.geojson")
LON0, LON1 = -172, 188
LAT0, LAT1 = 80, -58
TOLERANCE = 1.1  # degrees; roughly one dot on a 300px thumbnail
MIN_AREA = 3.0  # square degrees; drops islands that read as specks


def project(lon, lat, w, h):
    x = (lon - LON0) / (LON1 - LON0) * w
    y = (LAT0 - lat) / (LAT0 - LAT1) * h
    return round(x, 1), round(y, 1)


def build(w, h):
    data = json.loads(GEOJSON.read_text())
    subs = []
    for feature in data["features"]:
        geom = shape(feature["geometry"]).simplify(TOLERANCE, preserve_topology=True)
        polys = [geom] if geom.geom_type == "Polygon" else list(geom.geoms)
        for poly in polys:
            if poly.area < MIN_AREA:
                continue
            rings = [poly.exterior] + [r for r in poly.interiors if poly.area > 40]
            for ring in rings:
                pts = [project(lon, lat, w, h) for lon, lat in ring.coords]
                if len(pts) < 3:
                    continue
                d = " ".join(f"{x},{y}" for x, y in pts)
                subs.append(f"M{d}Z")
    return "".join(subs)


if __name__ == "__main__":
    w, h = 290, 172
    path = build(w, h)
    out = Path(__file__).with_name("map_path.txt")
    out.write_text(path)
    print(f"{len(path)} chars, {path.count('M')} subpaths -> {out}")
