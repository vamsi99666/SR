"""Scenes for 'the job pyramid is flipping'."""
import math

from engine import (INK, RED, TEAL, TEAL_L, GREY, CARD, WHITE, W, clamp, seg, ease_out, ease_back,
                    ease_in_out, lerp, fade, mix, person, robot, question_mark, check, ground)

ROWS = 5
DX, DY, PH = 86, 98, 78          # horizontal spacing, row spacing, person height
BASE_Y = 900                     # feet of the widest row (upright pyramid)
ROW_COL = [INK, INK, INK, TEAL_L, TEAL_L]  # top -> bottom: managers, seniors, freshers


def upright_people():
    out = []
    for r in range(ROWS):
        n = r + 1
        y = BASE_Y - (ROWS - 1 - r) * DY
        for k in range(n):
            out.append((360 + (k - (n - 1) / 2) * DX, y, r))
    return out


def inverted_people(top_y=520):
    out = []
    for r in range(ROWS):
        n = ROWS - r
        y = top_y + r * DY
        for k in range(n):
            out.append((360 + (k - (n - 1) / 2) * DX, y, r))
    return out


def tri(c, flip=0.0, color=GREY, y_apex=400, y_base=930, half=260):
    """Pyramid outline; flip 0 = upright, 1 = inverted (rotated through flat)."""
    cy = (y_apex + y_base) / 2
    k = math.cos(math.pi * flip)
    pts = [(360, cy + (y_apex - cy) * k), (360 - half, cy + (y_base - cy) * k), (360 + half, cy + (y_base - cy) * k)]
    c.line(pts + [pts[0]], color, 2)


def draw_pyramid(c, skip_rows=(), row_fade=None, bob_row=None, t=0.0):
    tri(c)
    for x, y, r in upright_people():
        if r in skip_rows:
            continue
        col = ROW_COL[r]
        if row_fade and r in row_fade:
            col = mix(col, GREY, row_fade[r])
        dy = -abs(math.sin(t * 9 + x)) * 12 if bob_row == r else 0
        person(c, x, y + dy, PH, col)


# ---- scenes: each is f(c, t, dur, p) ----

def pyramid_build(c, t, dur, p):
    tri(c, color=fade(GREY, seg(p, 0, 0.2)))
    people = sorted(upright_people(), key=lambda q: (-q[2], q[0]))
    for i, (x, y, r) in enumerate(people):
        s = ease_back(seg(p, 0.05 + i * 0.045, 0.05 + i * 0.045 + 0.12))
        person(c, x, y, PH, ROW_COL[r], scale=s)


def pyramid_labels(c, t, dur, p):
    active = 4 if p < 0.36 else (2 if p < 0.66 else 0)
    draw_pyramid(c, bob_row=active, t=t)
    tags = [(4, "freshers", 0.0), (2, "seniors", 0.36), (0, "managers", 0.66)]
    for r, name, at in tags:
        a = seg(p, at, at + 0.08)
        if a <= 0:
            continue
        y = BASE_Y - (ROWS - 1 - r) * DY - PH / 2
        xr = 360 - (r / 2) * DX - 40
        col = RED if r == active else INK
        c.text(20, y, name, 26, fade(col, a), "mono", anchor="lm")
        c.line([(20 + c.text_w(name, 26, "mono") + 8, y), (xr, y)], fade(col, a), 2)


def ladder_climb(c, t, dur, p):
    draw_pyramid(c)
    # red climber hops up the left edge, one row per hop
    q = ease_in_out(seg(p, 0.1, 0.92)) * (ROWS - 1)
    r0 = ROWS - 1 - int(min(q, ROWS - 1.001))
    f = q - int(min(q, ROWS - 1.001))
    def pos(r):
        return 360 - (r / 2) * DX - 70, BASE_Y - (ROWS - 1 - r) * DY
    (x0, y0), (x1, y1) = pos(r0), pos(max(0, r0 - 1))
    x, y = lerp(x0, x1, f), lerp(y0, y1, f) - math.sin(math.pi * f) * 45
    person(c, x, y, PH, RED, arm="up" if 0.05 < f < 0.95 else None)


def _robot_in(p, start=0.0):
    e = ease_back(seg(p, start, start + 0.35))
    return lerp(820, 640, e)


def ai_arrives(c, t, dur, p):
    draw_pyramid(c, row_fade={4: seg(p, 0.5, 0.9) * 0.5, 3: seg(p, 0.6, 1.0) * 0.3})
    rx = _robot_in(p, 0.05)
    robot(c, rx, 830 + math.sin(t * 4) * 6, 70, look=-1)


TASKS = ["notes", "reports", "code"]


def ai_tasks(c, t, dur, p):
    draw_pyramid(c, row_fade={4: 0.5 + 0.4 * p, 3: 0.3 + 0.4 * p})
    rx, ry = 640, 830 + math.sin(t * 4) * 6
    robot(c, rx, ry, 70, look=-1, blink=(int(t * 3) % 7 == 0))
    for i, name in enumerate(TASKS):
        a, b = 0.05 + i * 0.28, 0.05 + i * 0.28 + 0.3
        k = seg(p, a, b)
        if k <= 0:
            continue
        sx, sy = 190 + i * 110, BASE_Y - 110
        e = ease_in_out(k)
        x = lerp(sx, rx - 10, e)
        y = lerp(sy, ry - 20, e) - math.sin(math.pi * e) * 120
        sc = lerp(1, 0.4, e)
        if k >= 1:
            continue
        w = c.text_w(name, 22, "mono") + 24
        c.rrect(x - w / 2 * sc, y - 20 * sc, x + w / 2 * sc, y + 20 * sc, 4, CARD)
        if sc > 0.5:
            c.text(x, y, name, int(22 * sc), INK, "mono")
    done = sum(1 for i in range(3) if p > 0.05 + i * 0.28 + 0.3)
    for i in range(done):
        check(c, 580 + i * 34, 740, 22)


def base_melt(c, t, dur, p):
    tri(c, color=fade(GREY, 1 - seg(p, 0.3, 0.8) * 0.6))
    for x, y, r in upright_people():
        col = ROW_COL[r]
        if r >= 3:
            st = (0.05 if r == 4 else 0.25) + (x % 7) * 0.015
            k = seg(p, st, st + 0.45)
            fall = k * k * 420
            col = fade(mix(col, GREY, 0.7), 1 - k)
            if k >= 1:
                continue
            person(c, x, y + fall, PH, col, angle=(k * 0.6 if x > 360 else -k * 0.6))
        else:
            person(c, x, y, PH, col)
    robot(c, 640, 830 + math.sin(t * 4) * 6, 70, look=-1)


def invert(c, t, dur, p):
    flip = ease_in_out(seg(p, 0.05, 0.5))
    tri(c, flip=flip, color=TEAL, y_apex=400, y_base=930)
    for i, (x, y, r) in enumerate(inverted_people()):
        s = ease_back(seg(p, 0.5 + i * 0.025, 0.62 + i * 0.025))
        person(c, x, y, PH, INK if r < 3 else TEAL_L, scale=s)


def inverted_detail(c, t, dur, p):
    tri(c, flip=1, color=TEAL)
    pts = inverted_people()
    for x, y, r in pts:
        person(c, x, y, PH, INK if r < 3 else TEAL_L,
               arm="up" if r == 0 and p > 0.4 else None)
    # small robots float over the experts like kites
    for i, (x, y, r) in enumerate(p_ for p_ in pts if p_[2] == 0):
        k = ease_back(seg(p, 0.4 + i * 0.08, 0.55 + i * 0.08))
        if k <= 0:
            continue
        ry = y - PH - 70 + math.sin(t * 3 + i) * 8
        c.line([(x + 18, y - PH * 0.75), (x + 4, ry + 18)], GREY, 1.5)
        robot(c, x, ry, 30 * k)
    # "few" vs "many" marks
    a = seg(p, 0.1, 0.25)
    c.text(360, 1010, "entry level", 24, fade(TEAL, a), "mono")
    c.text(360, 290, "experts + AI", 24, fade(RED, seg(p, 0.45, 0.6)), "mono")


def ladder(c, missing=2, color=INK, x0=300, x1=420, top=380, bottom=960, gap=64):
    c.line([(x0, top), (x0, bottom)], color, 6)
    c.line([(x1, top), (x1, bottom)], color, 6)
    n = int((bottom - top) / gap)
    for i in range(1, n):
        y = bottom - i * gap
        if i <= missing:
            c.dashed((x0, y), (x1, y), GREY, 2, 8)
            continue
        c.line([(x0, y), (x1, y)], color, 6)


def missing_rung(c, t, dur, p):
    ground(c)
    ladder(c)
    person(c, 220, 960, 110, RED)
    for i in range(3):
        k = ease_back(seg(p, 0.2 + i * 0.15, 0.35 + i * 0.15))
        if k > 0:
            question_mark(c, 200 + i * 40, 780 - i * 30 + math.sin(t * 3 + i) * 6, 50 * k)


def leap(c, t, dur, p):
    ground(c)
    ladder(c)
    target_y = 960 - 3 * 64
    crouch = seg(p, 0.05, 0.3)
    jump = ease_out(seg(p, 0.3, 0.65))
    x = lerp(220, 360, jump)
    y = lerp(960, target_y, jump) - math.sin(math.pi * jump) * 110
    h = 110 * (1 - 0.18 * math.sin(math.pi * crouch) if jump == 0 else 1)
    person(c, x, y, h, RED, arm="up" if jump > 0 else None)
    if 0.3 < p < 0.7:
        for i in range(3):
            yy = y - 30 - i * 25
            c.line([(x - 60 - i * 6, yy + 40), (x - 90 - i * 6, yy + 70)], GREY, 2)
    # keeps climbing after landing
    if p > 0.65:
        k = seg(p, 0.7, 1)
        y0 = target_y - 90 - k * 40
        c.arrow((470, y0), (470, y0 - 90), fade(RED, k), 5, 22)


SKILLS = [("AI తో పని", "robot"), ("judgment", "scale"), ("real projects", "blocks")]


def _icon(c, kind, x, y):
    if kind == "robot":
        robot(c, x, y - 6, 38, shadow=False)
    elif kind == "scale":
        c.line([(x, y - 30), (x, y + 26)], INK, 4)
        c.line([(x - 32, y - 20), (x + 32, y - 20)], INK, 4)
        for sx in (-1, 1):
            c.line([(x + sx * 32, y - 20), (x + sx * 32, y)], INK, 2)
            c.arc(x + sx * 32, y - 4, 14, 0, 180, RED, 4)
        c.line([(x - 18, y + 26), (x + 18, y + 26)], INK, 4)
    else:
        c.rrect(x - 30, y + 2, x - 2, y + 28, 2, TEAL_L, False)
        c.rrect(x + 2, y + 2, x + 30, y + 28, 2, RED, False)
        c.rrect(x - 14, y - 26, x + 14, y - 2, 2, INK, False)


def three_skills(c, t, dur, p):
    for i, (name, icon) in enumerate(SKILLS):
        k = ease_out(seg(p, 0.02 + i * 0.3, 0.2 + i * 0.3))
        if k <= 0:
            continue
        y = 430 + i * 180
        x0 = lerp(-560, 80, k)
        c.rrect(x0, y - 60, x0 + 560, y + 60, 6, CARD)
        _icon(c, icon, x0 + 70, y)
        c.text(x0 + 130, y, name, 38, INK, "te", anchor="lm")
        check(c, x0 + 510, y, 34, p=seg(p, 0.15 + i * 0.3, 0.28 + i * 0.3))


def fresher_senior(c, t, dur, p):
    ground(c)
    walk = seg(p, 0, 0.45)
    x = lerp(120, 360, ease_out(walk))
    grow = ease_in_out(seg(p, 0.35, 0.8))
    sh = lerp(100, 300, grow)
    person(c, x + 40 * grow, 960, sh, fade((170, 160, 145), 0.35 + 0.65 * grow), shadow=False)
    person(c, x, 960, 100, RED, walk=t * 9 if walk < 1 else None)
    c.text(x, 1000, "fresher", 24, RED, "mono")
    c.text(x + 40, 960 - sh - 30, "senior", 24, fade(INK, grow), "mono")


def end(c, t, dur, p):
    k = ease_out(seg(p, 0, 0.3))
    pts = [(360 - 280 * k, 520), (360 + 280 * k, 520), (360, 520 + 420 * k)]
    c.poly(pts, TEAL)
    person(c, 360, 520, 120, RED, arm=f"wave:{t * 6}" if p > 0.3 else None, scale=ease_back(seg(p, 0.2, 0.4)))
    for i, (x, y) in enumerate([(200, 430), (520, 420), (440, 340)]):
        robot(c, x, y + math.sin(t * 3 + i) * 8, 34 * ease_back(seg(p, 0.35 + i * 0.1, 0.5 + i * 0.1)))


SCENES = {f.__name__: f for f in [pyramid_build, pyramid_labels, ladder_climb, ai_arrives, ai_tasks, base_melt,
                                   invert, inverted_detail, missing_rung, leap, three_skills, fresher_senior, end]}
