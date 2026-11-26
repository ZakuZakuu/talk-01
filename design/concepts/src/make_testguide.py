#!/usr/bin/env python3
"""Illustrated guide (Chinese) for the first prints: the calibration plate and tabs, the snap-fit lid and frame, the feel mock-up.
    python3 design/concepts/src/make_testguide.py docs/print-test-guide
Geometry is taken from cad/calibration.py (the plate: 110 x 70 mm; the lid: 30 x 24 mm). Standard library only.
"""
import os
import sys

FONT = "WenQuanYi Zen Hei, Noto Sans CJK SC, sans-serif"
PAPER, INK, DIM, ORANGE, GREEN, RED, BLUE = "#f4f0e6", "#2b2a28", "#6b675c", "#d9531e", "#2f7a46", "#b53a22", "#2f6f9f"
PLATE, PLATE_E = "#d8cfb4", "#6f6a5e"


def f(x):
    return f"{x:.2f}".rstrip("0").rstrip(".")


def text(x, y, s, size=16, fill=INK, weight="normal", anchor="start"):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return f'<text x="{f(x)}" y="{f(y)}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}" font-family="{FONT}">{s}</text>'


def rect(x, y, w, h, fill="none", stroke="none", sw=1, rx=0, extra=""):
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(rx)}" fill="{fill}" stroke="{stroke}" stroke-width="{f(sw)}" {extra}/>'


def line(x1, y1, x2, y2, stroke=INK, sw=1.5, extra=""):
    return f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{stroke}" stroke-width="{f(sw)}" {extra}/>'


def circ(cx, cy, r, fill="none", stroke="none", sw=1):
    return f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{fill}" stroke="{stroke}" stroke-width="{f(sw)}"/>'


def badge(x, y, n, col=ORANGE):
    return circ(x, y, 15, col, "#fff", 2) + text(x, y + 6, str(n), 17, "#fff", "bold", "middle")


def arrow(x1, y1, x2, y2, col=INK, sw=2.5):
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    h = 9
    p = [(x2, y2), (x2 - h * math.cos(a - 0.45), y2 - h * math.sin(a - 0.45)), (x2 - h * math.cos(a + 0.45), y2 - h * math.sin(a + 0.45))]
    return line(x1, y1, x2 - 4 * math.cos(a), y2 - 4 * math.sin(a), col, sw) + f'<polygon points="{" ".join(f(px) + "," + f(py) for px, py in p)}" fill="{col}"/>'


def svg(w, h, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"><rect width="{w}" height="{h}" fill="{PAPER}"/>{"".join(body)}</svg>'


def write(out, name, s):
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, name), "w", encoding="utf-8") as fh:
        fh.write(s)
    print("wrote", os.path.join(out, name))


# ------------------------------------------------------------------ page 1: the calibration plate and the tabs
CLEAR = (0.15, 0.20, 0.25, 0.30, 0.40)
GAPS = (0.8, 1.1, 1.4)
SLOTS = (0.6, 0.8, 1.0, 1.1, 1.3)
LINES = (0.4, 0.6, 0.8, 1.0, 1.2)


def page1(out):
    b = [text(50, 58, "校准板怎么试", 34, INK, "bold"), text(50, 90, "calibration_plate.stl + calibration_tabs.stl · 看个大概就行，不用量得很准", 16, DIM)]
    s, ox, oy = 8.0, 60, 140                               # 8 px per mm; the plate is 110 x 70 mm
    X = lambda x: ox + x * s
    Y = lambda y: oy + (70 - y) * s                        # cad y is up
    b.append(rect(ox, oy, 110 * s, 70 * s, PLATE, PLATE_E, 2.5, 6))
    # pockets (1)
    for i, c in enumerate(CLEAR):
        cx, cy, sz = 12 + i * 14, 52, 10 + 2 * c
        b.append(rect(X(cx - sz / 2), Y(cy + sz / 2), sz * s, sz * s, "#8d856f", INK, 1.5))
        for k in range(i + 1):
            b.append(circ(X(cx - 4 + k * 2.2), Y(cy - 8.5), 3.2, "#6f6a5e"))
    # ridge groups (2)
    for gi, g in enumerate(GAPS):
        x0 = 5 + gi * 27
        for k in range(4):
            xr = x0 + k * (1.9 + g)
            b.append(rect(X(xr), Y(28), 1.9 * s, 20 * s, "#efe9d6", INK, 1))
    # slots (3)
    for i, w in enumerate(SLOTS):
        b.append(rect(X(90 + i * 4), Y(24), w * s, 16 * s, PAPER, INK, 1))
    # lines (4)
    for i, w in enumerate(LINES):
        b.append(rect(X(90 + i * 4), Y(56), w * s, 20 * s, "#efe9d6", INK, 1))
    # zone frames and badges
    zones = [(1, X(4), Y(58.5), 70 * s + 8, 15 * s, X(2) - 6 - 10, Y(58.5) - 14),
             (2, X(3), Y(30), 80 * s - 6, 24 * s, X(-0.5) - 12, Y(30) - 14),
             (3, X(88.5), Y(26), 22 * s - 6, 20 * s, X(106) + 10, Y(26) - 18),
             (4, X(88.5), Y(58), 22 * s - 6, 26 * s, X(106) + 10, Y(58) - 18)]
    for (n, zx, zy, zw, zh, bx, by) in zones:
        b.append(rect(zx, zy, zw, zh, "none", ORANGE, 2.2, 8, 'stroke-dasharray="7 5"'))
        b.append(badge(bx if n in (1, 2) else bx + 4, by if n in (1, 2) else by, n))
    # labels under the plate map
    b.append(text(X(40), oy + 70 * s + 24, "（这是校准板的正面，朝上放在桌上看）", 14, DIM, "normal", "middle"))
    # explanations, right column
    ex = 980
    items = [(1, "间隙小块", ["把 calibration_tabs 里的小块", "逐个放进凹槽里（点数对应）。", "记：哪个放得进去又不晃？"]),
             (2, "脊线的缝", ["三组，缝 0.8 / 1.1 / 1.4 mm。", "斜着对光看，缝里干净、", "没有连丝 = 合格。"]),
             (3, "通缝", ["五条，宽 0.6~1.3 mm。", "对着灯看：能透光 = 通。", "记：最窄哪条是通的？"]),
             (4, "细线", ["五条凸起细线 0.4~1.2 mm。", "用指甲轻刮：", "没断、没掉 = 打出来了。"])]
    yy = 140
    for (n, ttl, lines_) in items:
        b.append(badge(ex, yy + 6, n))
        b.append(text(ex + 28, yy + 12, ttl, 20, INK, "bold"))
        for k, ln in enumerate(lines_):
            b.append(text(ex + 28, yy + 38 + k * 22, ln, 16, INK))
        yy += 142
    # tab test, bottom left
    ty = 770
    b.append(badge(60, ty, 1))
    b.append(text(88, ty + 7, "小块怎么试：把小块从上往下放进凹槽，只看三种情况", 20, INK, "bold"))
    cases = [("太紧", RED, 0.0, ["压不进去，要用力按、", "要敲才行，或者卡在半路。", "→ 这个间隙太小"]),
             ("刚好", GREEN, 0.5, ["轻轻一放就落到底，", "晃一晃不会咔咔响，", "倒过来也不会自己掉。"]),
             ("太松", BLUE, 1.2, ["放进去明显晃动，", "有缝能看到一圈，", "→ 这个间隙太大"])]
    for i, (name, col, gap, lns) in enumerate(cases):
        cx = 60 + i * 330
        by = ty + 8
        # cross-section: a plate with a pocket, the tab inside
        b.append(rect(cx, by + 80, 100, 36, PLATE, PLATE_E, 2))
        pk_w, tab_w = 80, 80 - gap * 20
        b.append(rect(cx + 10, by + 80, pk_w, 24, PAPER, INK, 1.5))                        # the pocket
        tx = cx + 10 + (pk_w - tab_w) / 2
        tab_y = by + 80 + (4 if name == "太紧" else 8)
        if name == "太紧":
            tab_y = by + 52
        b.append(rect(tx, tab_y, tab_w, 20, "#efe9d6", INK, 1.5))
        b.append(text(cx + 55, by + 140, name, 18, col, "bold", "middle"))
        for k, ln in enumerate(lns):
            b.append(text(cx + 130, by + 56 + k * 22, ln, 15, INK))
    # dots table
    b.append(text(60, ty + 235, "凹槽旁边的小点数：", 17, INK, "bold"))
    for i, c in enumerate(CLEAR):
        b.append(text(250 + i * 190, ty + 235, f"{'●' * (i + 1)}  {c:.2f} mm", 16, INK))
    b.append(text(60, ty + 262, "（每边的间隙。选「刚好」里最小的那个就行）", 14, DIM))
    # record
    ry = ty + 295
    b.append(rect(50, ry, 1300, 172, "#fffaf0", "#b9ad8a", 2, 8))
    b.append(text(70, ry + 32, "发给我这几个答案就够了（可以拍照）：", 18, INK, "bold"))
    recs = ["①  最小的「刚好」是几个点？   ____ 个点",
            "②  三组脊缝（0.8 / 1.1 / 1.4）哪几组是干净的？   ________",
            "③  最窄的通缝是哪一条（0.6 / 0.8 / 1.0 / 1.1 / 1.3）？   ________",
            "④  最细的、完整打出来的线是哪一条（0.4 / 0.6 / 0.8 / 1.0 / 1.2）？   ________"]
    for k, r in enumerate(recs):
        b.append(text(70, ry + 64 + k * 26, r, 16, INK))
    write(out, "1-calibration.svg", svg(1400, ry + 205, b))


# ------------------------------------------------------------------ page 2: the snap-fit lid and the feel mock-up
def lid_top(ox, oy, s, show_labels=True):
    """The lid from the front (30 x 24 mm), drawn to scale; y is down in the image (top edge = hooks)."""
    b = []
    X = lambda x: ox + (x + 15) * s
    Y = lambda y: oy + (24 - y) * s
    b.append(rect(X(-15), Y(24), 30 * s, 24 * s, PLATE, PLATE_E, 2.5))
    for (x0, x1) in ((4.2, 10.8), (-10.8, -4.2)):
        b.append(rect(X(x0), Y(25.6), (x1 - x0) * s, 1.6 * s, "#b6a98c", INK, 2))
    for sgn in (1, -1):
        xo = sgn * 15
        lo, hi = sorted((sgn * 13.8, sgn * 12.8))
        b.append(rect(X(lo), Y(14), (hi - lo) * s, 14.5 * s, "#2b2a28"))                          # the slot
        a_lo, a_hi = sorted((xo, sgn * 13.8))
        b.append(rect(X(a_lo), Y(14), (a_hi - a_lo) * s, 14 * s, "#c7b999", INK, 1.5))             # the arm
        bx0, bx1 = sorted((xo, xo + sgn * 0.8))
        b.append(rect(X(bx0), Y(4), (bx1 - bx0) * s, 3.2 * s, ORANGE, INK, 1.5))                   # the bump
    b.append(f'<path d="M{f(X(-3))},{f(Y(0))} a{f(3 * s)},{f(3 * s)} 0 0 1 {f(6 * s)},0 Z" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>')
    return "".join(b), X, Y


def page2(out):
    b = [text(50, 58, "卡扣盖板和手感试件怎么试", 34, INK, "bold"), text(50, 90, "snap_lid.stl + snap_frame.stl，以及机身、按键块、滚轮 · 大意到了就行", 16, DIM)]
    # --- the snap lid, from the front
    s = 11.5
    g, X, Y = lid_top(70, 190, s)
    b.append(text(50, 140, "A  卡扣盖板：先认识它", 22, INK, "bold"))
    b.append(g)
    lab = [(X(7.5), Y(25.6), "钩子 ×2：硬的，不会弯，", "用来钩进框架上边的唇下面", 620, 150),
           (X(14.4), Y(8), "卡臂 ×2：细长的，会向里弯，", "尾巴上的橙色凸点会「咔哒」卡进框架侧槽", 620, 240),
           (X(0), Y(0) - 12, "拇指缺口：用指甲抠这里把盖板撬起来", "", 620, 330)]
    for (px, py, l1, l2, tx, ty) in lab:
        b.append(line(px, py, tx - 8, ty - 5, "#8a857a", 1.5))
        b.append(circ(px, py, 4, "#8a857a"))
        b.append(text(tx, ty, l1, 16, INK, "bold"))
        if l2:
            b.append(text(tx, ty + 22, l2, 15, INK))
    # --- how it goes on, three side views (to scale-ish)
    sy = 560
    b.append(text(50, sy - 16, "怎么装上去（侧面看，上边是盖板的「钩子」那一头）", 22, INK, "bold"))
    for i, (ang, cap1, cap2) in enumerate(((28, "① 斜着，钩子", "先插进框架的唇下面"), (12, "② 慢慢放平", "钩子留在唇下面"), (0, "③ 压盖板的下边", "听到「咔哒」= 卡上了"))):
        ox = 70 + i * 420
        # frame side: a wall on the left with a lip at the top
        b.append(rect(ox, sy + 20, 24, 190, PLATE, PLATE_E, 2))
        b.append(rect(ox, sy + 20, 90, 22, PLATE, PLATE_E, 2))                  # the lip at the top
        b.append(rect(ox, sy + 188, 70, 22, PLATE, PLATE_E, 2))                 # the bottom wall
        # the lid: a bar, hinged at the top hook
        import math
        a = math.radians(ang)
        px, py = ox + 48, sy + 56
        L = 150
        ex, ey = px + L * math.sin(a), py + L * math.cos(a)
        b.append(f'<polygon points="{f(px)},{f(py)} {f(px + 16 * math.cos(a))},{f(py - 16 * math.sin(a))} {f(ex + 16 * math.cos(a))},{f(ey - 16 * math.sin(a))} {f(ex)},{f(ey)}" fill="#c7b999" stroke="{INK}" stroke-width="2"/>')
        b.append(rect(px - 22, py - 4, 26, 12, "#b6a98c", INK, 2))                  # the hook
        if i < 2:
            b.append(arrow(ox + 140, sy + 150 if i == 0 else sy + 160, ox + 100, sy + 110 if i == 0 else sy + 150, ORANGE, 3))
        else:
            b.append(arrow(ox + 150, sy + 150, ox + 90, sy + 150, ORANGE, 3))
            b.append(text(ox + 150, sy + 120, "咔哒", 18, ORANGE, "bold"))
        b.append(text(ox + 20, sy + 250, cap1, 18, INK, "bold"))
        b.append(text(ox + 20, sy + 274, cap2, 15, DIM))
    b.append(text(70, sy + 310, "怎么取下来：指甲伸进拇指缺口 → 先把下边撬起来 → 再把钩子从唇下斜着抽出来。", 17, INK))
    # --- how to judge
    jy = sy + 350
    b.append(text(50, jy, "怎么判断（三种情况）", 22, INK, "bold"))
    judge = [("太紧", RED, ["要用很大的力才压得下，", "卡臂弯得很厉害，", "或者听到「啪」一声断了。"]),
             ("刚好", GREEN, ["轻按就有清楚的「咔哒」，", "装好后不晃，", "倒过来轻抖也不会掉。"]),
             ("太松", BLUE, ["没有咔哒声，", "装好后会晃，", "倒过来一抖就掉下来。"])]
    for i, (n, col, lns) in enumerate(judge):
        x = 70 + i * 420
        b.append(rect(x - 14, jy + 20, 390, 110, "#fffaf0", col, 2.5, 8))
        b.append(text(x, jy + 52, n, 20, col, "bold"))
        for k, ln in enumerate(lns):
            b.append(text(x, jy + 78 + k * 20, ln, 15, INK))
    b.append(text(70, jy + 160, "再做两件事：①装上、取下，重复 5 次 → 臂有没有裂？  ②装好后在桌上轻轻敲一敲 → 松不松？", 16, INK))
    b.append(text(70, jy + 186, "PLA 比较脆，臂断了也是有用的信息，不算打坏。把断口拍给我看就行。", 15, DIM))
    # --- the feel mock-up
    my = jy + 240
    b.append(text(50, my, "B  手感试件：四件小事", 22, INK, "bold"))
    rows = [("握", "左手握住机身，拿 1 分钟。", "太厚？太宽？还是刚好？"),
            ("键", "把 3 / 5 / 7 mm 的按键块用双面胶贴在左边缘的浅凹槽里，", "分别用拇指按一按。哪个不硌手、够得着？"),
            ("轮", "滚轮放进右上角圆凹槽，插一根 1.75 mm 耗材当轴，", "用食指或拇指拨轮缘。凸出的 1.2 mm 够不够拨？"),
            ("纹", "手指在下半部横脊上划过去。", "舒服？扎手？会不会太滑？")]
    for i, (k, l1, l2) in enumerate(rows):
        y = my + 40 + i * 62
        b.append(circ(72, y - 5, 20, ORANGE, "#fff", 2))
        b.append(text(72, y + 3, k, 20, "#fff", "bold", "middle"))
        b.append(text(110, y - 4, l1, 16, INK))
        b.append(text(110, y + 20, l2, 16, INK, "bold"))
    b.append(text(70, my + 300, "拍几张照片发给我就好：校准板正面、卡扣盖板装好的样子、三个按键块贴在机身上的样子（带尺子更好）。", 16, INK))
    write(out, "2-snap-and-feel.svg", svg(1400, my + 340, b))


if __name__ == "__main__":
    o = sys.argv[1] if len(sys.argv) > 1 else "."
    page1(o)
    page2(o)
