"""Scenes for 'preparing kids for the next 10 years'."""
import math

from engine import (INK, RED, TEAL, TEAL_L, GREY, CARD, WHITE, ROBOT, W, clamp, seg, ease_out, ease_back,
                    ease_in_out, lerp, fade, mix, person, robot, question_mark, check, cross, ground)

KID = RED
GROUND = 960


def kid(c, x, y=GROUND, h=120, **kw):
    person(c, x, y, h, KID, kid=True, **kw)


def board(c, x, y, w, h, k=1.0):
    w, h = w * k, h * k
    c.rrect(x - w / 2 - 10, y - h / 2 - 10, x + w / 2 + 10, y + h / 2 + 10, 4, (120, 86, 52))
    c.rrect(x - w / 2, y - h / 2, x + w / 2, y + h / 2, 2, TEAL, False)


def kid_class5(c, t, dur, p):
    ground(c)
    k = ease_back(seg(p, 0.0, 0.25))
    board(c, 430, 560, 360, 260, k)
    if k > 0.9:
        c.text(430, 545, "5", 150, WHITE, "hand")
        c.text(430, 650, "class", 30, (200, 214, 210), "mono")
    walk = ease_out(seg(p, 0.15, 0.7))
    x = lerp(-60, 170, walk)
    kid(c, x, h=140, walk=t * 10 if 0 < walk < 1 else None)
    c.rrect(x - 44, GROUND - 105, x - 20, GROUND - 60, 4, INK)  # school bag


def future_door(c, t, dur, p):
    ground(c)
    yr = int(lerp(2026, 2036, ease_in_out(seg(p, 0.05, 0.6))))
    c.rrect(250, 260, 470, 380, 6, CARD)
    c.rrect(250, 260, 470, 292, 6, RED, False)
    c.text(360, 340, str(yr), 52, INK, "mono")
    g = ease_in_out(seg(p, 0.05, 0.6))
    person(c, 190, GROUND, lerp(140, 230, g), KID, kid=g < 0.5)
    # a door that hasn't been built yet: dashed outline, then a question mark
    x0, x1, top = 430, 600, 560
    c.dashed((x0, GROUND), (x0, top + 85), INK, 3)
    c.dashed((x1, GROUND), (x1, top + 85), INK, 3)
    c.arc((x0 + x1) / 2, top + 85, 85, 180, 360, INK, 3)
    q = ease_back(seg(p, 0.55, 0.75))
    if q > 0:
        question_mark(c, (x0 + x1) / 2, 790 + math.sin(t * 3) * 6, 110 * q)


def marks(c, t, dur, p):
    k = ease_back(seg(p, 0, 0.2))
    tilt = seg(p, 0.55, 0.8)
    cx, cy = 360, 600
    w, h = 300 * k, 380 * k
    c.rrect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, 6, CARD)
    if k > 0.9:
        c.text(cx, cy - 140, "REPORT CARD", 24, INK, "mono")
        for i in range(4):
            c.line([(cx - 110, cy - 80 + i * 40), (cx + 30, cy - 80 + i * 40)], GREY, 4)
            c.text(cx + 85, cy - 80 + i * 40, "100", 24, INK, "mono")
        a = ease_back(seg(p, 0.2, 0.35))
        c.circle(cx + 70, cy + 120, 52 * a, fade(RED, 0.15), shadow=False, outline=RED, width=4)
        if a > 0.8:
            c.text(cx + 70, cy + 120, "A+", 46, RED, "hand")
    if tilt > 0:
        cross(c, cx, cy, 330, RED, p=ease_out(tilt), width=14)


def questions(c, t, dur, p):
    ground(c)
    kid(c, 170, h=150, arm="up" if p > 0.1 else None)
    for i in range(3):
        k = ease_back(seg(p, 0.08 + i * 0.1, 0.2 + i * 0.1))
        if k > 0:
            question_mark(c, 140 + i * 55, 690 - i * 50 + math.sin(t * 3 + i) * 7, 70 * k)
    ry = 760 + math.sin(t * 3.5) * 8
    robot(c, 540, ry, 100 * ease_back(seg(p, 0.35, 0.5)), look=-1)
    for i in range(4):
        k = ease_out(seg(p, 0.45 + i * 0.07, 0.55 + i * 0.07))
        if k > 0:
            y = 560 - i * 54
            c.rrect(470, y - 22, lerp(470, 610, k), y + 22, 4, CARD)
            if k > 0.9:
                c.text(540, y, "answer", 20, GREY, "mono")
    hl = seg(p, 0.75, 0.9)
    if hl > 0:
        c.circle(195, 640, 80 + 6 * math.sin(t * 6), fade(RED, 0.1), shadow=False, outline=fade(RED, hl), width=4)


def basics(c, t, dur, p):
    ground(c)
    blocks = [("అ", TEAL_L), ("ABC", INK), ("123", RED)]
    for i, (s, col) in enumerate(blocks):
        k = seg(p, 0.08 + i * 0.12, 0.2 + i * 0.12)
        if k <= 0:
            continue
        yt = GROUND - 90 - i * 92
        y = lerp(200, yt, k * k)
        c.rrect(140, y, 330, y + 88, 4, col)
        c.text(235, y + 44, s, 44, WHITE, "te")
    kid(c, 400, h=130)
    rk = ease_back(seg(p, 0.5, 0.62))
    robot(c, 600, 760 + math.sin(t * 3) * 6, 80 * rk, look=-1)
    bk = ease_out(seg(p, 0.58, 0.68))
    if bk > 0:
        c.rrect(420, 560, 420 + 230 * bk, 640, 10, CARD)
        if bk > 0.9:
            c.text(535, 600, "2 + 2 = 5", 36, INK, "mono")
    xk = seg(p, 0.72, 0.85)
    if xk > 0:
        cross(c, 690, 600, 44, RED, p=xk, width=8)


def hands(c, t, dur, p):
    ground(c)
    kid(c, 160, h=130, arm="point" if p > 0.1 else None)
    parts = [
        (380, 870, 560, 960, TEAL_L),
        (390, 780, 470, 870, CARD),
        (470, 780, 550, 870, CARD),
    ]
    for i, (x0, y0, x1, y1, col) in enumerate(parts):
        k = seg(p, 0.08 + i * 0.12, 0.18 + i * 0.12)
        if k > 0:
            dy = (1 - k * k) * -500
            c.rrect(x0, y0 + dy, x1, y1 + dy, 3, col)
    k = seg(p, 0.45, 0.58)
    if k > 0:
        dy = (1 - k * k) * -500
        c.poly([(360, 780 + dy), (580, 780 + dy), (530, 700 + dy), (410, 700 + dy)], RED)
    s = ease_back(seg(p, 0.62, 0.75))
    if s > 0:
        c.rrect(420, 640 - 30 * s, 540, 640 + 30 * s, 4, CARD)
        if s > 0.9:
            c.text(480, 640, "SHOP", 26, INK, "mono")
    for i in range(3):
        k = ease_back(seg(p, 0.75 + i * 0.06, 0.85 + i * 0.06))
        if k > 0:
            c.circle(410 + i * 45, 830, 14 * k, [RED, (230, 170, 40), TEAL_L][i])


def speak(c, t, dur, p):
    ground(c)
    c.rrect(290, 900, 430, GROUND, 3, TEAL)
    kid(c, 360, 900, 140, arm=f"wave:{t * 5}" if p > 0.2 else None)
    k = ease_back(seg(p, 0.1, 0.3))
    if k > 0:
        bw, bh = 340 * k, 200 * k
        cx, cy = 400, 560
        c.rrect(cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2, 22, CARD)
        c.poly([(cx - 60 * k, cy + bh / 2 - 2), (cx - 20 * k, cy + bh / 2 - 2), (cx - 70 * k, cy + bh / 2 + 50 * k)],
               CARD, shadow=False)
        for i, ln in enumerate([0.8, 0.6, 0.7]):
            lk = ease_out(seg(p, 0.3 + i * 0.12, 0.42 + i * 0.12))
            if lk > 0:
                y = cy - 50 + i * 50
                c.line([(cx - 130, y), (cx - 130 + 260 * ln * lk, y)], [INK, RED, INK][i], 10)
    for i in range(6):
        x = 60 + i * 120
        bob = math.sin(t * 4 + i) * 3 if p > 0.6 else 0
        c.circle(x, 985 + bob, 34, mix(INK, (90, 90, 90), (i % 2) * 0.4), shadow=False)


def fall_rise(c, t, dur, p):
    ground(c)
    run = seg(p, 0, 0.3)
    x = lerp(60, 330, run)
    fall = ease_in_out(seg(p, 0.3, 0.42))
    rise = ease_in_out(seg(p, 0.55, 0.75))
    ang = (fall - rise) * (math.pi / 2)
    go = ease_out(seg(p, 0.78, 1.0))
    x = x + go * 220
    c.rrect(345, GROUND - 22, 385, GROUND, 4, INK)  # the stone
    moving = run < 1 or 0 < go < 1
    kid(c, x if go == 0 else x, h=130, angle=ang, walk=t * 11 if moving else None,
        arm="up" if go > 0 else None)
    if 0.35 < p < 0.55:
        for i in range(4):
            a = i * math.pi / 2 + t * 2
            c.line([(x + 80 + math.cos(a) * 20, GROUND - 40 + math.sin(a) * 20),
                    (x + 80 + math.cos(a) * 34, GROUND - 40 + math.sin(a) * 34)], GREY, 3)


def ai_tool(c, t, dur, p):
    ground(c)
    walk = seg(p, 0.1, 0.9)
    x = lerp(140, 260, walk)
    kid(c, x, h=140, walk=t * 9 if 0 < walk < 1 else None, arm="up")
    rx = x + 220 + math.sin(t * 1.7) * 18
    ry = 560 + math.sin(t * 2.3) * 22
    hand = (x + 40, GROUND - 160)
    c.line([hand, (lerp(hand[0], rx, 0.5), lerp(hand[1], ry, 0.5) + 30), (rx, ry + 60)], GREY, 2)
    robot(c, rx, ry, 90, look=-1, blink=int(t * 2.5) % 6 == 0)
    k = ease_back(seg(p, 0.45, 0.6))
    if k > 0:
        c.rrect(rx - 70, ry + 110, rx + 70, ry + 160, 6, CARD)
        if k > 0.9:
            c.text(rx, ry + 135, "tool", 26, INK, "mono")


SKILL_CHIPS = ["ప్రశ్నలు", "basics", "projects", "మాట", "ధైర్యం"]


def ranks_skills(c, t, dur, p):
    for i, r in enumerate(["#1", "#2", "#3"]):
        k = seg(p, 0.1 + i * 0.08, 0.5 + i * 0.08)
        x = 200 + i * 160
        y = 420 + k * k * 600
        col = fade(mix(INK, GREY, k), 1 - k)
        if k < 1:
            c.circle(x, y, 60, col, shadow=k < 0.2)
            c.text(x, y, r, 40, fade(WHITE, 1 - k), "mono")
    for i, s in enumerate(SKILL_CHIPS):
        k = ease_back(seg(p, 0.45 + i * 0.08, 0.58 + i * 0.08))
        if k <= 0:
            continue
        y = 960 - i * 82
        w = 300 * k
        c.rrect(360 - w / 2, y - 34, 360 + w / 2, y + 34, 6, [TEAL_L, INK, RED, TEAL_L, INK][i])
        if k > 0.9:
            c.text(360, y, s, 36, WHITE, "te")


def end(c, t, dur, p):
    rise = ease_out(seg(p, 0, 0.6))
    c.circle(360, 900 - 140 * rise, 170, mix(RED, (240, 150, 60), 0.3), shadow=False)
    c.rrect(-10, 900, W + 10, 1000, 0, TEAL, False)
    walk = seg(p, 0.1, 1.0)
    x = lerp(120, 330, walk)
    person(c, x, 900, 230, INK, walk=t * 7, arm=None)
    kid(c, x + 70, 900, 130, walk=t * 7 + 1)
    c.line([(x + 25, 900 - 130), (x + 55, 900 - 85)], INK, 6)


SCENES = {f.__name__: f for f in [kid_class5, future_door, marks, questions, basics, hands, speak, fall_rise,
                                   ai_tool, ranks_skills, end]}
