#!/usr/bin/env python3
"""Round 2: the size ladder compared (front outlines and side profiles overlaid) with a paper-fit note for each.
    python3 design/concepts/src/make_ladder.py docs/print-test-guide
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_testguide import text, rect, line, circ, svg, write, INK, DIM, ORANGE, GREEN, RED, BLUE  # noqa: E402

SIZES = [("S0", 58, 92, 24, "#8a857a", "第一轮（已打印）", 121), ("S1", 52, 90, 20, BLUE, "小一步", 87), ("S2", 48, 88, 17, ORANGE, "明显变薄变窄", 66), ("S3", 46, 86, 15, GREEN, "很薄（只用来体验）", 54)]
CH = 15


def outline(ox, oy, s, w, h, col, dash=False):
    pts = [(0, 0), (w - CH, 0), (w, CH), (w, h), (0, h)]
    d = " ".join(f"{ox + x * s:.1f},{oy + y * s:.1f}" for x, y in pts)
    return (f'<polygon points="{d}" fill="none" stroke="{col}" stroke-width="3" stroke-linejoin="round" '
            f'{"stroke-dasharray=\"8 6\"" if dash else ""}/>')


def main(out):
    b = [text(50, 58, "第二轮：尺寸梯度", 34, INK, "bold"), text(50, 90, "你觉得「太厚、太宽」，所以做三个更小的机身一起比一比（宽 × 高 × 厚，单位 mm）", 16, DIM)]
    s, ox, oy = 5.6, 70, 150
    b.append(text(ox, oy - 14, "正面（左上角对齐）", 18, INK, "bold"))
    for (n, w, h, d, col, note, vol) in SIZES:
        b.append(outline(ox, oy, s, w, h, col, dash=(n == "S0")))
        i = [x[0] for x in SIZES].index(n)
        b.append(rect(ox + 58 * s + 30, oy + 20 + i * 30, 16, 16, col))
        b.append(text(ox + 58 * s + 54, oy + 33 + i * 30, f"{n}   {w} × {h} × {d}   （{note}）", 15, col, "bold"))
    sx = 780
    b.append(text(sx, oy - 14, "侧面（后面对齐；厚度 = 右边）", 18, INK, "bold"))
    for (n, w, h, d, col, note, vol) in SIZES:
        b.append(outline_side(sx, oy, s, d, h, col, n == "S0"))
    b.append(text(sx, oy + 92 * s + 28, "越往右越厚：S0 24 → S1 20 → S2 17 → S3 15 mm", 14, DIM))
    # table
    ty = oy + 92 * s + 90
    b.append(text(50, ty, "纸面上能不能装得下电子件？（按现有零件的典型尺寸算，没有量过真实零件）", 20, INK, "bold"))
    rows = [("S0 58×92×24", "能装，板子可以放在滚轮零件后面，余量约 3.6 mm。", "你说太厚、太宽、够不着滚轮。"),
            ("S1 52×90×20", "勉强：板子放在滚轮零件后面会超出约 0.4 mm，要么用更矮的开关，要么把板子挪到旁边。", "小一步。"),
            ("S2 48×88×17", "可以，但要把主控板放在滚轮的左边（不是后面），USB 接口靠左；开关要选矮一点的（约 3 mm）。余量约 2~3 mm。", "我倾向这个。"),
            ("S3 46×86×15", "装不下：宽度放不下主控板，厚度只剩约 0.2 mm 余量。", "只用来体验「很薄」是什么手感。")]
    for i, (a, bb, c) in enumerate(rows):
        y = ty + 36 + i * 64
        col = SIZES[i][4]
        b.append(rect(50, y - 20, 14, 14, col))
        b.append(text(76, y - 8, a, 17, col, "bold"))
        b.append(text(300, y - 8, bb, 15, INK))
        b.append(text(300, y + 14, c, 14, DIM))
    b.append(text(50, ty + 36 + 4 * 64 + 20, "按键块：每个机身配一个 5 mm 的（深度随机身变），你上一轮没告诉我 3/5/7 哪个最舒服——这次请一起告诉我。", 15, INK))
    write(out, "round2-size-ladder.svg", svg(1400, ty + 36 + 4 * 64 + 60, b))


def outline_side(ox, oy, s, d, h, col, dash):
    return rect(ox, oy, d * s, h * s, "none", col, 3, 4, 'stroke-dasharray="8 6"' if dash else "")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
