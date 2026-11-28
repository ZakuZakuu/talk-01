# SPDX-License-Identifier: CERN-OHL-P-2.0
"""The S2 GRAPHICS LAYER (v4, 2026-11-28): every mark on the body, drawn on one grid.

The owner and Claude compared the v3 renders with Teenage Engineering's product photos: what was missing is the layer of printed marks
(type, scales, ticks, small symbols) and, under it, a grid that everything sits on. This file holds both.

THE GRID: a 4 mm margin from every outer edge (x 4 and 44; the top at y 84), and the wheel's centre line (y 75) as the upper zone's
horizontal axis: the lamp, the DICT tick and the wheel sit on it. Small type is Inter SemiBold, the wordmark Inter Medium (both SIL OFL).

HOW IT IS MADE: each mark is a solid 0.4 mm deep (two 0.2 mm layers) in the face that prints on the bed. Without a multi-colour unit the
marks are ENGRAVED (cut 0.4 mm; a wipe of acrylic paint or a paint marker fills them, as model makers do). With an AMS the same solids
are exported as INLAYS (`*_ink.stl`): the slicer prints them in a second colour, flush with the face, like a pad print.
Assembled coordinates: x right, y up, z toward the front (the face is z = 17).
"""
import math
import cadquery as cq
from export_util import text_solid, place_bbox
from s2_lower import box, cyl
from s2_params import W, H, D, WHEEL_R, WHEEL_CX

INK_D = 0.4
MARGIN = 4.0
TOP = H - MARGIN                      # 84
WHEEL_C = (WHEEL_CX, H - 13.0)        # (32.9, 75)
AXIS_Y = WHEEL_C[1]
LAMP = (MARGIN + 0.95, AXIS_Y)        # the lamp: a 1.75 mm clear filament as a light pipe, its left edge on the margin
LAMP_HOLE = 1.9
# the dial's scale: four positions 45 deg apart, from DICT on the left (180) round the bottom to LOCK (315); the wheel carries the pointer
MODES = (("DICT", 180.0), ("TALK", 225.0), ("OPEN", 270.0), ("LOCK", 315.0))
TICK_R0, TICK_R1, TICK_W = 12.9, 14.3, 0.5
ARC_R0, ARC_R1 = 12.9, 13.35
LABEL_SIZE = 2.3                      # cap height about 1.7 mm, strokes about 0.35 mm: about the finest a 0.4 mm nozzle prints
COLLAR_R, COLLAR_D = 12.4, 0.5        # a recessed ring round the wheel's bore (a shadow line that frames the wheel)
POINTER = (3.4, 8.7, 0.9)             # the wheel's pointer: r0, r1, width


def _polar(r, a):
    return WHEEL_C[0] + r * math.cos(math.radians(a)), WHEEL_C[1] + r * math.sin(math.radians(a))


def _bar(x0, y0, x1, y1, w, z0, z1):
    """A bar with round ends from (x0, y0) to (x1, y1)."""
    L = math.hypot(x1 - x0, y1 - y0)
    ang = math.degrees(math.atan2(y1 - y0, x1 - x0))
    s = cq.Workplane("XY").workplane(offset=z0).slot2D(L + w, w, 0).extrude(z1 - z0)
    return s.rotate((0, 0, 0), (0, 0, 1), ang).translate(((x0 + x1) / 2, (y0 + y1) / 2, 0))


def _arc(r0, r1, a0, a1, z0, z1, n=48):
    outer = [(_polar(r1, a0 + (a1 - a0) * i / n)) for i in range(n + 1)]
    inner = [(_polar(r0, a1 - (a1 - a0) * i / n)) for i in range(n + 1)]
    return cq.Workplane("XY").workplane(offset=z0).polyline(outer + inner).close().extrude(z1 - z0)


def _label(txt, size, z0, z1, font="semibold"):
    return text_solid(txt, size, 0, 0, z0, z1 - z0, font=font)


# Three directions on the same grid and the same parts (owner, 2026-11-28: "make two or three versions"):
#   A "instrument": a scale like a measuring instrument (arc, ticks, words), a ridged cap with a block of equal slots, warm light colours;
#   B "radio":      quiet, like a 1960s radio: four dots and numbers round the wheel, a flat cap with a field of round holes, one light grey;
#   C "signal":     graphic and dark: the wordmark runs up the left margin in a column with the lamp and the key's mark, mono labels,
#                   a ridged cap; a dark body with light marks and a light wheel.
STYLES = {
    "A": dict(name="instrument", grille="slots"),
    "B": dict(name="radio", grille="holes"),
    "C": dict(name="signal", grille="slots"),
}
STYLE = "A"


def _union(parts):
    out = parts[0]
    for p in parts[1:]:
        out = out.union(p)
    return out


def _scale_words(z0, z1, font="semibold"):
    parts = [_arc(ARC_R0, ARC_R1, 180.0, 315.0, z0, z1)]
    for (name, a) in MODES:
        (x0, y0), (x1, y1) = _polar(TICK_R0, a), _polar(TICK_R1, a)
        parts.append(_bar(x0, y0, x1, y1, TICK_W, z0, z1))
        lab = _label(name, LABEL_SIZE, z0, z1, font=font)
        xo, yo = _polar(TICK_R1 + 1.0, a)
        if a == 180.0:
            lab = place_bbox(lab, xo, AXIS_Y, ("right", "center"))
        elif a == 225.0:
            lab = place_bbox(lab, xo + 0.3, yo + 0.3, ("right", "top"))
        elif a == 270.0:
            lab = place_bbox(lab, WHEEL_C[0], yo, ("center", "top"))
        else:
            lab = place_bbox(lab, W - MARGIN, y1 - 1.5, ("right", "top"))      # under its tick, right edge on the margin
        parts.append(lab)
    return parts


def _scale_dots(z0, z1):
    parts = []
    for i, (name, a) in enumerate(MODES):
        x, y = _polar(13.6, a)
        parts.append(cyl(x, y, 0.6, z0, z1))
        xn, yn = _polar(16.0, a)
        xn = min(xn, W - MARGIN - 0.8)
        parts.append(place_bbox(_label(str(i + 1), LABEL_SIZE, z0, z1), xn, yn, ("center", "center")))
    return parts


def _ptt(z0, z1, text=True, font="semibold"):
    ky = 55.65
    parts = [cq.Workplane("XY").workplane(offset=z0).polyline([(MARGIN, ky), (MARGIN + 1.5, ky + 0.95), (MARGIN + 1.5, ky - 0.95)]).close().extrude(z1 - z0)]
    if text:
        parts.append(place_bbox(_label("PTT", LABEL_SIZE, z0, z1, font=font), MARGIN + 2.4, ky, ("left", "center")))
    return parts


def face_ink(extra=0.0, style=None):
    """The marks on the upper shell's face. extra > 0 lets the solid stand out of the face (for cutting)."""
    style = style or STYLE
    z0, z1 = D - INK_D, D + extra
    if style == "A":
        parts = [place_bbox(_label("talk.01", 4.2, z0, z1, font="medium"), MARGIN, TOP, ("left", "top"))]
        parts += _scale_words(z0, z1) + _ptt(z0, z1)
    elif style == "B":
        parts = [place_bbox(_label("talk.01", 3.4, z0, z1, font="medium"), MARGIN, TOP, ("left", "top"))]
        parts += _scale_dots(z0, z1) + _ptt(z0, z1, text=False)
    else:
        word = _label("talk.01", 4.6, z0, z1, font="medium").rotate((0, 0, 0), (0, 0, 1), 90)   # reads upward, along the left margin
        parts = [place_bbox(word, MARGIN, 59.0, ("left", "bottom"))]
        parts += _scale_words(z0, z1, font="mono") + _ptt(z0, z1, text=False)
    return _union(parts)


def collar_cut():
    from s2_upper import BORE_R
    return cyl(WHEEL_C[0], WHEEL_C[1], COLLAR_R, D - COLLAR_D, D + 0.1).cut(cyl(WHEEL_C[0], WHEEL_C[1], BORE_R - 0.01, D - 1, D + 1))


def wheel_ink(z_face, extra=0.0, angle=180.0):
    """The wheel's pointer (at rest it points at DICT, 180 deg)."""
    r0, r1, w = POINTER
    (x0, y0), (x1, y1) = _polar(r0, angle), _polar(r1, angle)
    return _bar(x0, y0, x1, y1, w, z_face - INK_D, z_face + extra)


def back_ink(extra=0.0, style=None):
    """The back's lettering, mirrored to read from behind; its left edge (seen from behind) on the margin (model x = 44),
    its top under the chamfer's margin line. Style B adds the legend of its numbered scale."""
    style = style or STYLE
    z0, z1 = -extra, INK_D
    lines = [("talk.01", 4.2, "medium"), ("USB-C MICROPHONE", 2.0, "semibold"), ("S2 · 48 × 88 × 17", 2.0, "semibold")]
    if style == "B":
        lines[2] = ("1 DICT  2 TALK  3 OPEN  4 LOCK", 2.0, "semibold")       # the legend of the numbered scale (one line: the screws at y 59 are below)
    if style == "C":
        lines = [(t, sz, "mono" if f == "semibold" else f) for (t, sz, f) in lines]
    y = 70.5
    out = None
    for (txt, size, font) in lines:
        t = text_solid(txt, size, 0, 0, z0, z1 - z0, mirror=True, font=font)
        t = place_bbox(t, W - MARGIN, y, ("right", "top"))
        out = t if out is None else out.union(t)
        y = t.val().BoundingBox().ymin - (1.6 if size > 3 else 1.1)
    return out


def cap_ink(extra=0.0, style=None):
    """Marks on the cap (it prints face down too). Style B: a fine ring that frames the field of holes. Others: none."""
    style = style or STYLE
    if style != "B":
        return None
    from s2_cap import HOLE_C, HOLE_FIELD_R
    z0, z1 = D - INK_D, D + extra
    return cyl(HOLE_C[0], HOLE_C[1], HOLE_FIELD_R + 1.6, z0, z1).cut(cyl(HOLE_C[0], HOLE_C[1], HOLE_FIELD_R + 1.15, z0 - 1, z1 + 1))
