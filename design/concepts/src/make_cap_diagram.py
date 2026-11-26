#!/usr/bin/env python3
"""Diagram (Chinese): how the keyhole-slide cap goes on and comes off. Geometry from cad/s2_cap.py (lower part of the S2 shell, mm).
    python3 design/concepts/src/make_cap_diagram.py docs/print-test-guide
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_testguide import text, rect, line, circ, arrow, svg, write, INK, DIM, ORANGE, GREEN, RED, BLUE, PLATE, PLATE_E  # noqa: E402

W, YT = 48.0, 58.0
PEGS = ((8, 11), (40, 11), (8, 45), (40, 45))
SLIDE = 6.0


def panel(ox, oy, s, off, cap_col, label):
    X = lambda x: ox + x * s
    Y = lambda y: oy + (YT - y) * s
    b = [f'<path d="M{X(0)},{Y(YT)} V{Y(5)} Q{X(0)},{Y(0)} {X(5)},{Y(0)} H{X(W - 5)} Q{X(W)},{Y(0)} {X(W)},{Y(5)} V{Y(YT)} Z" fill="#e8e1cf" stroke="{PLATE_E}" stroke-width="2.5"/>']
    b.append(rect(X(0), Y(YT), W * s, 6 * s, "#bdb6a2", "none"))
    b.append(text(X(W / 2), Y(YT) + 4 * s, "控制区", 15, INK, "bold", "middle"))
    b.append(circ(X(24), Y(25), 17 * s, "#faf6ea", "#8a857a", 2))
    for (px, py) in PEGS:                                          # the keyholes
        b.append(rect(X(px - 1.4), Y(py), 2.8 * s, SLIDE * s, "#faf6ea", "#8a857a", 1.5))
        b.append(circ(X(px), Y(py), 1.4 * s, "#faf6ea", "#8a857a", 1.5))
        b.append(circ(X(px), Y(py - SLIDE), 3.1 * s, "#faf6ea", "#8a857a", 1.5))
    capy0, capy1 = 0.1 + off, 51.85 + off
    b.append(rect(X(0.1), Y(capy1), 47.8 * s, (capy1 - capy0) * s, cap_col, ORANGE, 3, 8, 'fill-opacity="0.55"'))
    for (px, py) in PEGS:
        b.append(circ(X(px), Y(py + off), 1.2 * s, INK))
        b.append(circ(X(px), Y(py + off), 2.5 * s, "none", INK, 1.5))
    b.append(text(ox, oy - 14, label, 17, INK, "bold"))
    return "".join(b), X, Y


def main(out):
    b = [text(50, 58, "卡扣盖板：锁孔滑动式", 34, INK, "bold"), text(50, 90, "盖板正面是完整的一块平面，卡扣全部藏在背面 · 示意图（比例大致准确）", 16, DIM)]
    s = 4.2
    ys = 160
    steps = [(-SLIDE, "① 放上去", ["盖板比正位低 6 mm", "（下边悬在机身外）", "四个蘑菇钉对准圆孔，垂直放下"]),
             (-SLIDE / 2, "② 向上推", ["蘑菇钉滑进窄槽", "顶边顶住控制区", "「咔哒」一声卡到位"]),
             (0.0, "③ 卡好", ["外轮廓和机身一样大", "正面只有一块平面", "蘑菇头比窄槽宽，提不起来"])]
    for i, (off, lab, lines_) in enumerate(steps):
        ox = 60 + i * 450
        g, X, Y = panel(ox, ys, s, off, ["#c7b999", "#c7b999", "#c7b999"][i], lab)
        b.append(g)
        for k, ln in enumerate(lines_):
            b.append(text(ox, ys + YT * s + 36 + (6 * s if i == 0 else 0) + k * 22, ln, 15, INK if k == 0 else DIM))
        if i < 2:
            b.append(arrow(ox + W * s + 18, ys + 190, ox + W * s + 18 + 56, ys + 190, ORANGE, 4) if False else "")
    b.append(arrow(60 + W * s + 30, ys + 250, 60 + 450 - 30, ys + 250, ORANGE, 4))
    b.append(arrow(60 + 450 + W * s + 30, ys + 250, 60 + 900 - 30, ys + 250, ORANGE, 4))
    b.append(text(60 + W * s + 32, ys + 235, "向上推", 14, ORANGE, "bold"))
    b.append(text(60 + 450 + W * s + 32, ys + 235, "向上推", 14, ORANGE, "bold"))
    # how to take it off
    ty = ys + YT * s + 150
    b.append(rect(50, ty - 28, 1300, 74, "#fffaf0", "#b9ad8a", 2, 8))
    b.append(text(70, ty, "取下来：", 18, INK, "bold"))
    b.append(text(160, ty, "拇指压着横脊，把盖板往下推 6 mm（要用点力，越过「咔哒」），然后垂直提起。横脊本来就是防滑的把手。", 16, INK))
    b.append(text(160, ty + 28, "要不要更好抓？下边缘可以做一个很小的缺口露出盖板边缘（在机身上，不在盖板上），以后再说。", 15, DIM))
    # side section
    sy = ty + 110
    b.append(text(50, sy, "侧面剖开看一个蘑菇钉（放大）", 20, INK, "bold"))
    s2, ox, oy = 26, 120, sy + 60
    b.append(rect(ox, oy, 10.5 * s2, 2.4 * s2, "#c7b999", INK, 2))                    # the cap plate, 2.4
    b.append(rect(ox, oy + 2.4 * s2, 4.2 * s2, 1.6 * s2, PLATE, INK, 2))                # the floor, left of the slot
    b.append(rect(ox + 6.7 * s2, oy + 2.4 * s2, 3.8 * s2, 1.6 * s2, PLATE, INK, 2))     # right of the slot
    cx = ox + 5.45 * s2
    b.append(rect(cx - 1.2 * s2, oy + 2.4 * s2, 2.4 * s2, 1.9 * s2, "#b6a98c", INK, 2))  # the neck
    pts = f"{cx - 1.2 * s2},{oy + 4.3 * s2} {cx + 1.2 * s2},{oy + 4.3 * s2} {cx + 2.5 * s2},{oy + 5.9 * s2} {cx - 2.5 * s2},{oy + 5.9 * s2}"
    b.append(f'<polygon points="{pts}" fill="#b6a98c" stroke="{INK}" stroke-width="2"/>')
    b.append(rect(cx - 2.5 * s2, oy + 5.9 * s2, 5 * s2, 0.5 * s2, "#b6a98c", INK, 2))
    lx = ox + 10.5 * s2 + 40
    for k, (ty2, t) in enumerate(((oy + 1.0 * s2, "盖板 2.4 mm（正面朝上，横脊在最上面）"), (oy + 3.2 * s2, "地板 1.6 mm，中间是窄槽（宽 2.8）"),
                                  (oy + 3.9 * s2, "颈 Ø2.4：在槽里滑动"), (oy + 6.0 * s2, "蘑菇头 Ø5.0：比槽宽，盖板就提不起来"))):
        b.append(line(lx - 30, ty2, lx - 6, ty2, "#8a857a", 1.5))
        b.append(text(lx, ty2 + 5, t, 15, INK))
    # the detent
    dy = oy + 8.6 * s2 + 20
    b.append(text(50, dy, "「咔哒」是怎么来的（地板里的小弹舌，俯视）", 20, INK, "bold"))
    b.append(rect(120, dy + 40, 360, 4.2 * s2 * 0.5, PLATE, INK, 2))
    b.append(rect(180, dy + 40, 250, 5 * 0.5 * s2, "#faf6ea", INK, 1.5))
    b.append(rect(200, dy + 40, 210, 3 * 0.5 * s2 * 1.0, PLATE, INK, 2))
    b.append(circ(214, dy + 40, 6, "#8a857a"))
    for k, t in enumerate(["地板上切出一条细细的平舌（14 × 3 mm），舌尖有一个小凸点（0.6 mm）。", "盖板背面对应位置有一条浅槽。盖板滑到位时，凸点弹进槽里，就是「咔哒」。",
                           "舌是平躺着弯的，顺着打印层的方向受力，比竖着的卡臂结实（这是 FDM 的经验，没有测试过）。", "想取下时，推力要越过凸点，估计要 2~3 N（手算，PLA，没有测过）。"]):
        b.append(text(520, dy + 30 + k * 26, t, 15, INK if k < 2 else DIM))
    write(out, "cap-keyhole.svg", svg(1400, dy + 190, b))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
