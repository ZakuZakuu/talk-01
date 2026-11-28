# SPDX-License-Identifier: CERN-OHL-P-2.0
"""Export a CadQuery solid to a clean STL: tessellate, drop zero-area triangles (they appear at sharp fillet ends), check it is closed."""
import cadquery as cq
import trimesh


def export_stl(solid, path, tolerance=0.02, angular=0.1):
    cq.exporters.export(solid, path, tolerance=tolerance, angularTolerance=angular)
    m = trimesh.load(path)
    good = m.nondegenerate_faces()
    if not good.all():
        m.update_faces(good)
        m.remove_unreferenced_vertices()
        m.export(path)
    return m


# Lettering. Inter (the graphics, v4) and JetBrains Mono (SIL Open Font Licence 1.1) are used when installed; otherwise CadQuery's
# default font. Only the glyphs' outlines end up in the model, as geometry.
import os as _os
FONTS = {
    "mono": ("/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Bold.ttf",),
    "medium": ("/usr/share/fonts/opentype/inter/Inter-Medium.otf",),
    "semibold": ("/usr/share/fonts/opentype/inter/Inter-SemiBold.otf",),
}


def text_solid(txt, size, x, y, z0, depth, halign="left", valign="bottom", mirror=False, font="mono"):
    """A text solid from z0 to z0 + depth, placed at (x, y). mirror=True reads correctly from -z (a back face seen from behind)."""
    path = next((p for p in FONTS.get(font, ()) if _os.path.exists(p)), None)
    wp = cq.Workplane("XY").workplane(offset=z0)
    kw = dict(halign=halign, valign=valign, kind="bold" if font == "mono" else "regular")
    if path:
        kw["fontPath"] = path
    t = wp.text(txt, size, depth, combine=False, **kw)
    if mirror:
        t = t.mirror("YZ")
    return t.translate((x, y, 0))


def place_bbox(solid, x=None, y=None, anchor=("left", "top")):
    """Move a solid so that its bounding box's chosen edges sit at x and y (the glyphs' real extent, not the font's metrics)."""
    bb = solid.val().BoundingBox()
    dx = dy = 0.0
    if x is not None:
        dx = x - {"left": bb.xmin, "right": bb.xmax, "center": (bb.xmin + bb.xmax) / 2}[anchor[0]]
    if y is not None:
        dy = y - {"bottom": bb.ymin, "top": bb.ymax, "center": (bb.ymin + bb.ymax) / 2}[anchor[1]]
    return solid.translate((dx, dy, 0))
