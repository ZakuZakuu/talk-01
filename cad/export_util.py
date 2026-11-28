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


# Engraved lettering. JetBrains Mono (SIL Open Font Licence 1.1) is used when it is installed; otherwise CadQuery's default font.
# Only the glyphs' outlines end up in the model, as geometry.
import os as _os
FONT_PATHS = ("/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Bold.ttf",
              "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-ExtraBold.ttf")


def text_solid(txt, size, x, y, z0, depth, halign="left", valign="bottom", mirror=False):
    """A text solid from z0 to z0 + depth, placed at (x, y). mirror=True reads correctly from -z (a back face seen from behind)."""
    font = next((p for p in FONT_PATHS if _os.path.exists(p)), None)
    wp = cq.Workplane("XY").workplane(offset=z0)
    kw = dict(halign=halign, valign=valign, kind="bold")
    if font:
        kw["fontPath"] = font
    t = wp.text(txt, size, depth, combine=False, **kw)
    if mirror:
        t = t.mirror("YZ")
    return t.translate((x, y, 0))
