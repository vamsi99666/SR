"""Scenes for 'One control, four conclusions' (GRC control effectiveness, EN)."""
import math

from engine import (INK, RED, TEAL, TEAL_L, GREY, CARD, WHITE, W, clamp, seg, ease_out, ease_back,
                    ease_in_out, lerp, fade, mix, person, check, cross, question_mark)

NAVY = (28, 42, 68)
AMBER = (214, 150, 32)
GREEN = (46, 125, 90)
SOFT = (222, 214, 198)


def control_card(c, x, y, k=1.0, w=260, h=120, title="C001", sub="Encrypt data at rest"):
    if k <= 0:
        return
    w, h = w * k, h * k
    c.rrect(x - w / 2, y - h / 2, x + w / 2, y + h / 2, 12, NAVY)
    if k > 0.9:
        c.text(x, y - 18, title, 40, WHITE, "mono")
        c.text(x, y + 28, sub, 20, (200, 210, 225), "mono")


def pill(c, x, y, text, col, k=1.0, size=24, pad=26):
    if k <= 0:
        return
    w = (c.text_w(text, size, "mono") + pad * 2) * k
    h = (size + 26) * k
    c.rrect(x - w / 2, y - h / 2, x + w / 2, y + h / 2, h / 2, col)
    if k > 0.9:
        c.text(x, y, text, size, WHITE, "mono")


def one_to_many(c, t, dur, p):
    control_card(c, 360, 330, ease_back(seg(p, 0.0, 0.12)))
    cols, rows = 18, 12
    n = cols * rows
    for i in range(n):
        r, q = divmod(i, cols)
        a = 0.12 + (r * cols + q) / n * 0.3
        k = ease_out(seg(p, a, a + 0.08))
        if k <= 0:
            continue
        x, y = 70 + q * 34, 470 + r * 34
        sx, sy = lerp(360, x, k), lerp(380, y, k)
        c.circle(sx, sy, 8 * k, mix(TEAL_L, NAVY, (i * 7 % 10) / 20), shadow=False)
    if p > 0.25:
        c.line([(360, 390), (360, 455)], fade(NAVY, seg(p, 0.25, 0.35)), 3)
    a = seg(p, 0.2, 0.32)
    if a > 0:
        c.text(360, 900, "5,000 applications", 30, fade(INK, a), "mono")
    k = ease_back(seg(p, 0.55, 0.68))
    if k > 0:
        person(c, 610, 450, 150 * k, INK)
        c.text(610, 270, "CRO", 22, fade(INK, k), "mono")
        question_mark(c, 650, 300 + math.sin(t * 3) * 5, 70 * k)


TEAMS = [("Security Arch.", "PARTIALLY EFFECTIVE", AMBER), ("Cyber Risk", "INEFFECTIVE", RED),
         ("SOX", "NOT APPLICABLE", GREY), ("Internal Audit", "EFFECTIVE", GREEN)]
STAMP_AT = [0.36, 0.53, 0.66, 0.80]   # measured from VO word times


def four_stamps(c, t, dur, p):
    control_card(c, 360, 320, ease_back(seg(p, 0.0, 0.1)))
    for i, ((team, verdict, col), at) in enumerate(zip(TEAMS, STAMP_AT)):
        y = 470 + i * 110
        k = ease_out(seg(p, at - 0.08, at))
        if k <= 0:
            continue
        c.text(lerp(-200, 60, k), y, team, 26, INK, "mono", anchor="lm")
        s = seg(p, at, at + 0.06)
        if s > 0:
            sc = lerp(1.6, 1.0, ease_out(s))
            pill(c, 520, y, verdict, col, sc if s < 1 else 1.0, size=20, pad=18)
    if p > 0.9:
        a = ease_out(seg(p, 0.9, 0.97))
        c.line([(680, 450), (695, 450), (695, 810), (680, 810)], fade(RED, a), 4)
        c.text(360, 880, "1 control · 4 conclusions", 30, fade(RED, a), "mono")


def copies(c, t, dur, p):
    n = 14
    cols = [GREEN, RED, AMBER, GREEN, GREY, RED, AMBER, GREEN, RED, AMBER, GREEN, RED, GREY, AMBER]
    for i in range(n):
        k = ease_out(seg(p, 0.08 + i * 0.035, 0.2 + i * 0.035))
        ang = (i / n) * math.tau + 0.3
        rad = 230 * k
        x = 360 + math.cos(ang) * rad
        y = 590 + math.sin(ang) * rad * 0.95
        if k <= 0:
            continue
        rot_w = 150
        c.rrect(x - rot_w / 2, y - 38, x + rot_w / 2, y + 38, 8, CARD)
        c.text(x - 18, y - 10, f"C001 v{i + 1}", 18, NAVY, "mono")
        c.circle(x + 52, y - 10, 9, cols[i], shadow=False)
        c.line([(x - 55, y + 16), (x + 40 - (i % 3) * 18, y + 16)], SOFT, 4)
    control_card(c, 360, 590, 1.0, w=200, h=100, sub="master?")
    z = seg(p, 0.6, 0.9)
    if z > 0:
        for j in range(5):
            a1 = (j * 3 / n) * math.tau + 0.3
            a2 = ((j * 3 + 7) / n) * math.tau + 0.3
            p1 = (360 + math.cos(a1) * 230, 590 + math.sin(a1) * 218)
            p2 = (360 + math.cos(a2) * 230, 590 + math.sin(a2) * 218)
            m = (lerp(p1[0], p2[0], 0.5) + 25, lerp(p1[1], p2[1], 0.5) - 25)
            if j / 5 < z:
                c.line([p1, m, p2], RED, 3)
        c.text(360, 920, "conflicting ratings · fragmented evidence", 22, fade(RED, z), "mono")


LAYERS = [("DEFINITION", "what must be true", NAVY, 0.31),
          ("IMPLEMENTATION", "where & how it applies", TEAL, 0.50),
          ("ASSESSMENT", "tested · evidence · result", RED, 0.76)]


def three_layers(c, t, dur, p):
    for i, (name, sub, col, at) in enumerate(LAYERS):
        split = ease_in_out(seg(p, at - 0.1, at))
        y = lerp(560, 380 + i * 190, split)
        w = 520
        c.rrect(360 - w / 2, y - 70, 360 + w / 2, y + 70, 14, col if split > 0 else NAVY)
        if split > 0.8:
            c.text(360, y - 18, name, 34, WHITE, "mono")
            c.text(360, y + 28, sub, 22, (225, 230, 236), "mono")
        elif i == 0 and split == 0:
            c.text(360, y, "C001", 40, WHITE, "mono")
    if p > 0.85:
        a = seg(p, 0.85, 0.95)
        for i in range(2):
            y0 = 380 + i * 190 + 70
            c.line([(360, y0), (360, y0 + 50)], fade(INK, a), 3)


def average_trap(c, t, dur, p):
    merge = ease_in_out(seg(p, 0.3, 0.6))
    cols, rows = 10, 4
    for i in range(cols * rows):
        r, q = divmod(i, cols)
        x0, y0 = 120 + q * 50, 420 + r * 50
        x = lerp(x0, 360, merge)
        y = lerp(y0, 600, merge)
        s = lerp(18, 4, merge)
        if merge < 1:
            c.rrect(x - s, y - s, x + s, y + s, 4, GREEN, shadow=False)
    # critical red app
    out = ease_back(seg(p, 0.8, 0.92))
    cx = lerp(lerp(600, 360, merge), 360, out)
    cy = lerp(lerp(530, 600, merge), 380, out)
    cs = lerp(lerp(30, 6, merge), 46, out)
    if merge < 1 or out > 0:
        c.rrect(cx - cs, cy - cs, cx + cs, cy + cs, 6, RED)
    if merge < 0.2:
        c.text(600, 478, "critical", 20, RED, "mono")
    if merge > 0.6:
        a = seg(p, 0.5, 0.65)
        c.rrect(110, 560, 610, 640, 10, fade(GREEN, a))
        c.text(360, 600, "average: 97% effective", 28, fade(WHITE, a), "mono")
    if out > 0.8:
        c.text(360, 380, "!", 54, WHITE, "te")
        c.text(360, 470, "critical app: INEFFECTIVE", 26, RED, "mono")
        cross(c, 360, 600, 120, RED, p=seg(p, 0.9, 0.98), width=8)


def cro_dashboard(c, t, dur, p):
    k = ease_out(seg(p, 0.0, 0.12))
    if k <= 0:
        return
    c.rrect(60, lerp(400, 260, k), 660, lerp(800, 920, k), 18, CARD)
    if k < 1:
        return
    c.text(90, 300, "C001 · Enterprise view", 24, NAVY, "mono", anchor="lm")
    pill(c, 360, 380, "PARTIALLY EFFECTIVE", AMBER, ease_back(seg(p, 0.15, 0.27)), size=26)
    a = seg(p, 0.35, 0.5)
    if a > 0:
        c.text(90, 480, "Critical apps covered", 22, INK, "mono", anchor="lm")
        c.rrect(90, 505, 630, 535, 8, SOFT, shadow=False)
        c.rrect(90, 505, 90 + 540 * 0.92 * ease_out(a), 535, 8, TEAL, shadow=False)
        c.text(630, 480, f"{int(92 * ease_out(a))}%", 26, TEAL, "mono", anchor="rm")
    b = seg(p, 0.66, 0.76)
    if b > 0:
        c.text(90, 610, "Ineffective / failing", 22, INK, "mono", anchor="lm")
        c.rrect(90, 635, 630, 665, 8, SOFT, shadow=False)
        c.rrect(90, 635, 90 + 540 * 0.08 * ease_out(b) / 0.08 * 0.08, 665, 8, RED, shadow=False)
        c.text(630, 610, f"{int(8 * ease_out(b))}%", 26, RED, "mono", anchor="rm")
    e = seg(p, 0.82, 0.92)
    if e > 0:
        c.text(90, 750, "Exceptions", 22, INK, "mono", anchor="lm")
        c.text(630, 750, "tracked", 22, fade(GREEN, e), "mono", anchor="rm")
        check(c, 500, 750, 30, GREEN, p=e)
        c.text(360, 850, "evidence: current 2nd-line testing", 20, fade(GREY, e), "mono")


PLATFORMS = ["Platform A", "Platform B", "Platform C", "Platform D"]


def governance(c, t, dur, p):
    k = ease_back(seg(p, 0.0, 0.15))
    if k > 0:
        pill(c, 360, 330, "DEFENSIBLE RISK STATEMENT", GREEN, k, size=24)
    for i, name in enumerate(PLATFORMS):
        a = ease_out(seg(p, 0.3 + i * 0.04, 0.4 + i * 0.04))
        if a <= 0:
            continue
        x, y = 200 + (i % 2) * 320, 480 + (i // 2) * 110
        dim = seg(p, 0.55, 0.7)
        c.rrect(x - 130, y - 38, x + 130, y + 38, 10, mix(NAVY, SOFT, dim * 0.7))
        c.text(x, y, name, 22, WHITE, "mono")
        if dim > 0.5:
            question_mark(c, x + 110, y - 40, 34)
    g = ease_back(seg(p, 0.76, 0.88))
    if g > 0:
        w, h = 520 * g, 120 * g
        c.rrect(360 - w / 2, 800 - h / 2, 360 + w / 2, 800 + h / 2, 16, RED)
        if g > 0.9:
            c.text(360, 785, "GOVERNANCE", 36, WHITE, "mono")
            c.text(360, 830, "decision", 24, WHITE, "mono")


SCENES = {f.__name__: f for f in [one_to_many, four_stamps, copies, three_layers, average_trap,
                                   cro_dashboard, governance]}
