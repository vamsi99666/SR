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
    yr = int(lerp(2026, 2035, ease_in_out(seg(p, 0.05, 0.6))))
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


def twelve_grid(c, t, dur, p):
    for i in range(12):
        r, col = divmod(i, 3)
        x, y = 170 + col * 190, 330 + r * 160
        k = ease_back(seg(p, 0.1 + i * 0.05, 0.22 + i * 0.05))
        if k <= 0:
            continue
        w, h = 150 * k, 120 * k
        fill = [TEAL_L, INK, RED][i % 3]
        c.rrect(x - w / 2, y - h / 2, x + w / 2, y + h / 2, 8, fill)
        if k > 0.9:
            c.text(x, y, str(i + 1), 56, WHITE, "mono")


def memorize(c, t, dur, p):
    ground(c)
    kid(c, 160, h=140)
    rx, ry = 560, 700 + math.sin(t * 3) * 6
    robot(c, rx, ry, 100 * ease_back(seg(p, 0.05, 0.2)), look=-1)
    for i in range(5):
        a, b = 0.2 + i * 0.1, 0.45 + i * 0.1
        k = seg(p, a, b)
        if k >= 1:
            continue
        e = ease_in_out(k)
        x = lerp(200, rx, e)
        y = lerp(GROUND - 200 - i * 10, ry, e) - math.sin(math.pi * e) * 160
        s = lerp(1, 0.3, e)
        c.rrect(x - 40 * s, y - 28 * s, x + 40 * s, y + 28 * s, 3, [RED, TEAL_L, INK][i % 3])
        if s > 0.6:
            c.line([(x - 24 * s, y - 6 * s), (x + 24 * s, y - 6 * s)], WHITE, 3)
            c.line([(x - 24 * s, y + 8 * s), (x + 14 * s, y + 8 * s)], WHITE, 3)
    stack = sum(1 for i in range(5) if p > 0.45 + i * 0.1)
    for i in range(stack):
        c.rrect(rx - 50, ry - 110 - i * 22, rx + 50, ry - 90 - i * 22, 3, [RED, TEAL_L, INK][i % 3])
    if p > 0.8:
        check(c, 620, 470, 40, p=seg(p, 0.8, 0.95))


def focus(c, t, dur, p):
    ground(c)
    c.rrect(260, 860, 460, 880, 3, INK)              # desk
    c.line([(290, 880), (290, GROUND)], INK, 6)
    c.line([(430, 880), (430, GROUND)], INK, 6)
    c.rrect(320, 830, 400, 860, 3, CARD)             # book
    kid(c, 360, 860, 120)
    ring = ease_out(seg(p, 0.45, 0.7))
    for i in range(7):
        a = i / 7 * math.tau + t * 0.6
        k = ease_back(seg(p, 0.05 + i * 0.05, 0.15 + i * 0.05))
        if k <= 0:
            continue
        rad = lerp(190, 300, ring)
        x, y = 360 + math.cos(a) * rad, 720 + math.sin(a) * rad * 0.8
        fade_k = 1 - seg(p, 0.6, 0.85)
        if fade_k <= 0:
            continue
        c.rrect(x - 44 * k, y - 22 * k, x + 44 * k, y + 22 * k, 10, fade(RED if i % 2 else INK, fade_k))
        if k > 0.9:
            c.circle(x - 26, y, 6, fade(WHITE, fade_k), shadow=False)
    if p > 0.6:
        g = seg(p, 0.6, 0.8)
        c.circle(360, 790, 110 + 6 * math.sin(t * 4), None, shadow=False, outline=fade(TEAL, g), width=4)


def adapt(c, t, dur, p):
    ground(c)
    # one narrow path vs a kid that can switch between shapes
    m = ease_in_out(seg(p, 0.25, 0.75))
    for i, (x, col) in enumerate([(160, TEAL_L), (360, INK), (560, RED)]):
        c.rrect(x - 70, 420, x + 70, 520, 8, fade(col, 0.35 + 0.65 * (abs(m * 2 - i) < 0.5)))
    labels = ["coding", "design", "business"]
    for i, (x, s) in enumerate(zip([160, 360, 560], labels)):
        c.text(x, 470, s, 24, WHITE, "mono")
    x = lerp(160, 560, m)
    kid(c, x, h=140, walk=t * 9 if 0 < m < 1 else None, arm="up")
    c.arrow((x, 760), (x, 560), RED, 4, 16)


def split_schools(c, t, dur, p):
    ground(c)
    k = ease_back(seg(p, 0.05, 0.25))
    for x, col, name, icon in [(200, GREY, "speed", "fast"), (520, TEAL, "thinking", "think")]:
        w, h = 220 * k, 300 * k
        c.rrect(x - w / 2, GROUND - h, x + w / 2, GROUND, 6, col)
        c.poly([(x - w / 2 - 20, GROUND - h), (x + w / 2 + 20, GROUND - h), (x, GROUND - h - 90 * k)], INK)
        if k > 0.9:
            c.text(x, GROUND - 230, name, 30, WHITE, "mono")
            if icon == "fast":
                for j in range(3):
                    c.line([(x - 60, GROUND - 150 + j * 30), (x + 60 - j * 20, GROUND - 150 + j * 30)], WHITE, 6)
            else:
                c.circle(x, GROUND - 130, 34, (240, 200, 70), shadow=False)
                c.rrect(x - 14, GROUND - 98, x + 14, GROUND - 80, 3, WHITE, False)
    walk = seg(p, 0.35, 0.9)
    kid(c, lerp(360, 520, ease_in_out(walk)), h=110, walk=t * 9 if 0 < walk < 1 else None)


def home(c, t, dur, p):
    ground(c)
    c.poly([(140, 520), (580, 520), (360, 360)], RED)
    c.rrect(170, 520, 550, GROUND, 4, CARD)
    c.rrect(250, 840, 470, 860, 3, INK)
    person(c, 260, GROUND, 230, INK, arm="point" if p > 0.2 else None)
    kid(c, 420, GROUND, 130, arm="up" if p > 0.55 else None)
    k = ease_back(seg(p, 0.55, 0.7))
    if k > 0:
        y = 700 + math.sin(t * 3) * 6
        c.circle(430, y, 40 * k, (240, 200, 70), shadow=False)
        c.rrect(430 - 16 * k, y + 34 * k, 430 + 16 * k, y + 54 * k, 3, INK, False)
        for j in range(6):
            a = j / 6 * math.tau
            c.line([(430 + math.cos(a) * 52 * k, y + math.sin(a) * 52 * k),
                    (430 + math.cos(a) * 68 * k, y + math.sin(a) * 68 * k)], (240, 200, 70), 4)


def thinker(c, t, dur, p):
    ground(c)
    kid(c, 360, h=170)
    for i in range(10):
        a = i / 10 * math.tau + t * 0.8
        k = ease_back(seg(p, 0.05 + i * 0.03, 0.15 + i * 0.03))
        x, y = 360 + math.cos(a) * 250, 600 + math.sin(a) * 200
        c.rrect(x - 50 * k, y - 18 * k, x + 50 * k, y + 18 * k, 4, fade(GREY, 1 - 0.6 * seg(p, 0.5, 0.8)))
        if k > 0.9:
            c.text(x, y, "answer", 18, fade(WHITE, 1 - seg(p, 0.5, 0.8)), "mono")
    g = ease_back(seg(p, 0.5, 0.65))
    if g > 0:
        y = 700 + math.sin(t * 3) * 6
        c.circle(360, y, 46 * g, (240, 200, 70), shadow=False)
        c.rrect(360 - 18 * g, y + 40 * g, 360 + 18 * g, y + 62 * g, 3, INK, False)


def money(c, t, dur, p):
    ground(c)
    kid(c, 170, h=140, arm="point" if p > 0.1 else None)
    # piggy bank
    c.circle(470, 860, 90, (232, 150, 160))
    c.circle(550, 840, 30, (232, 150, 160))
    c.rrect(410, 930, 440, GROUND, 4, (210, 130, 140))
    c.rrect(500, 930, 530, GROUND, 4, (210, 130, 140))
    c.rrect(445, 768, 495, 778, 3, INK, False)
    c.circle(545, 832, 6, INK, shadow=False)
    for i in range(5):
        k = seg(p, 0.1 + i * 0.13, 0.28 + i * 0.13)
        if 0 < k < 1:
            c.circle(470, lerp(420, 770, k * k), 24, (236, 186, 60))
            c.text(470, lerp(420, 770, k * k), "₹", 26, INK, "te")
    saved = sum(1 for i in range(5) if p > 0.28 + i * 0.13)
    for i in range(saved):
        c.rrect(590, 900 - i * 24, 660, 920 - i * 24, 4, (236, 186, 60))


def _phone(c, x, y, w=220, h=380):
    c.rrect(x - w / 2, y - h / 2, x + w / 2, y + h / 2, 26, INK)
    c.rrect(x - w / 2 + 14, y - h / 2 + 30, x + w / 2 - 14, y + h / 2 - 30, 10, CARD, False)


def fact_check(c, t, dur, p):
    ground(c)
    kid(c, 150, h=130)
    person(c, 250, GROUND, 220, INK)
    k = ease_back(seg(p, 0.05, 0.2))
    if k <= 0:
        return
    _phone(c, 520, 620, 220 * k, 380 * k)
    if k < 0.9:
        return
    c.rrect(430, 480, 610, 560, 12, (200, 235, 200), False)
    for j in range(3):
        c.line([(445, 500 + j * 22), (595 - j * 30, 500 + j * 22)], INK, 4)
    c.text(520, 590, "Forwarded", 18, GREY, "mono")
    m = ease_in_out(seg(p, 0.3, 0.6))
    mx, my = lerp(380, 520, m), lerp(800, 520, m)
    c.circle(mx, my, 46, None, shadow=False, outline=RED, width=7)
    c.line([(mx + 32, my + 32), (mx + 70, my + 70)], RED, 10)
    st = ease_back(seg(p, 0.65, 0.78))
    if st > 0:
        c.rrect(440, 660 - 34 * st, 600, 660 + 34 * st, 6, None, shadow=False, outline=RED, width=5)
        if st > 0.9:
            c.text(520, 660, "FAKE?", 40, RED, "mono")


def bias_scale(c, t, dur, p):
    ground(c)
    tilt = math.sin(seg(p, 0.15, 1) * math.pi * 2.5) * 0.18 * (1 - seg(p, 0.85, 1)) + 0.12 * seg(p, 0.85, 1)
    cx, cy = 360, 560
    c.poly([(cx - 70, GROUND), (cx + 70, GROUND), (cx, GROUND - 60)], INK)
    c.line([(cx, GROUND - 40), (cx, cy)], INK, 8)
    dx, dy = math.cos(tilt) * 230, math.sin(tilt) * 230
    left, right = (cx - dx, cy - dy), (cx + dx, cy + dy)
    c.line([left, right], INK, 8)
    c.circle(cx, cy, 14, RED)
    for (x, y), lab, col in [(left, "AI", TEAL_L), (right, "news", RED)]:
        c.line([(x, y), (x - 50, y + 120)], INK, 2)
        c.line([(x, y), (x + 50, y + 120)], INK, 2)
        c.poly([(x - 75, y + 120), (x + 75, y + 120), (x + 55, y + 150), (x - 55, y + 150)], col)
        c.text(x, y + 135, lab, 24, WHITE, "mono")
    k = ease_back(seg(p, 0.55, 0.7))
    if k > 0:
        question_mark(c, cx, 400, 80 * k)


def two_channels(c, t, dur, p):
    ground(c)
    for j, (x, col, mood) in enumerate([(200, TEAL_L, 1), (520, RED, -1)]):
        k = ease_back(seg(p, 0.05 + j * 0.15, 0.2 + j * 0.15))
        if k <= 0:
            continue
        w, h = 260 * k, 200 * k
        y = 520
        c.rrect(x - w / 2, y - h / 2, x + w / 2, y + h / 2, 10, INK)
        c.rrect(x - w / 2 + 12, y - h / 2 + 12, x + w / 2 - 12, y + h / 2 - 12, 4, col, False)
        c.line([(x - 40, y + h / 2), (x - 60, y + h / 2 + 40)], INK, 5)
        c.line([(x + 40, y + h / 2), (x + 60, y + h / 2 + 40)], INK, 5)
        if k > 0.9:
            person(c, x, y + 70, 110, WHITE, shadow=False, arm="up" if mood > 0 else None)
            c.text(x, y - 70, "CH " + str(j + 1), 22, WHITE, "mono")
            # same story, different spin
            c.arc(x, y + 60 - mood * 10, 40, 200 if mood > 0 else 20, 340 if mood > 0 else 160, WHITE, 0)
    kid(c, 360, h=130, arm="point" if p > 0.5 else None)
    k = ease_back(seg(p, 0.55, 0.7))
    if k > 0:
        question_mark(c, 360, 760 + math.sin(t * 3) * 6, 70 * k)


def choose(c, t, dur, p):
    ground(c)
    robot(c, 580, 820 + math.sin(t * 3) * 6, 90, look=-1)
    kid(c, 140, h=140, arm="up" if p > 0.6 else None)
    picked = 4
    for i in range(10):
        k = ease_out(seg(p, 0.05 + i * 0.04, 0.2 + i * 0.04))
        if k <= 0:
            continue
        col, row = i % 2, i // 2
        tx, ty = 270 + col * 140, 380 + row * 80
        x, y = lerp(580, tx, k), lerp(780, ty, k)
        chosen = i == picked and p > 0.6
        dim = seg(p, 0.6, 0.75) if i != picked else 0
        fill = RED if chosen else fade(CARD, 1 - 0.7 * dim)
        c.rrect(x - 60, y - 28, x + 60, y + 28, 6, fill)
        c.text(x, y, f"option {i + 1}", 18, WHITE if chosen else fade(INK, 1 - 0.7 * dim), "mono")
    if p > 0.7:
        check(c, 270 + 140 * (picked % 2) + 90, 380 + 80 * (picked // 2), 34, p=seg(p, 0.7, 0.85))


def _face(c, x, y, r, col, mood):
    c.circle(x, y, r, col)
    c.circle(x - r * 0.35, y - r * 0.2, r * 0.1, INK, shadow=False)
    c.circle(x + r * 0.35, y - r * 0.2, r * 0.1, INK, shadow=False)
    if mood == "happy":
        c.arc(x, y + r * 0.05, r * 0.45, 20, 160, INK, 4)
    elif mood == "sad":
        c.arc(x, y + r * 0.55, r * 0.4, 200, 340, INK, 4)
    elif mood == "angry":
        c.line([(x - r * 0.55, y - r * 0.5), (x - r * 0.15, y - r * 0.35)], INK, 4)
        c.line([(x + r * 0.55, y - r * 0.5), (x + r * 0.15, y - r * 0.35)], INK, 4)
        c.line([(x - r * 0.3, y + r * 0.4), (x + r * 0.3, y + r * 0.4)], INK, 4)
    else:  # scared
        c.circle(x, y + r * 0.4, r * 0.15, INK, shadow=False)


def feelings(c, t, dur, p):
    ground(c)
    kid(c, 360, h=150, arm="point" if p > 0.5 else None)
    moods = [("angry", (230, 120, 100), "కోపం"), ("scared", (180, 200, 230), "భయం"),
             ("sad", (170, 190, 200), "బాధ"), ("happy", (240, 205, 90), "సంతోషం")]
    for i, (m, col, name) in enumerate(moods):
        k = ease_back(seg(p, 0.08 + i * 0.1, 0.2 + i * 0.1))
        if k <= 0:
            continue
        x, y = 135 + i * 150, 520 + math.sin(t * 2.5 + i) * 6
        _face(c, x, y, 55 * k, col, m)
        if k > 0.9:
            lk = seg(p, 0.5 + i * 0.08, 0.6 + i * 0.08)
            if lk > 0:
                c.text(x, y + 90, name, 30, fade(INK, lk), "te")


NIGHT = (29, 39, 51)
LAMP = (246, 214, 120)


def _room_night(c, t, p):
    c.rrect(110, 290, 330, 500, 6, NIGHT)                       # window
    c.line([(220, 290), (220, 500)], CARD, 6)
    c.line([(110, 395), (330, 395)], CARD, 6)
    c.circle(285, 340, 26, (240, 236, 214), shadow=False)
    c.circle(274, 334, 22, NIGHT, shadow=False)                 # crescent
    for sx, sy in [(150, 330), (180, 450), (260, 455), (300, 430), (160, 420)]:
        tw = 2 + 1.5 * math.sin(t * 3 + sx)
        c.circle(sx, sy, tw, (240, 236, 214), shadow=False)
    c.circle(560, 360, 58, CARD)                                # clock at 10:05
    c.circle(560, 360, 58, None, shadow=False, outline=INK, width=4)
    c.line([(560, 360), (560 - 30, 360 - 17)], INK, 6)
    c.line([(560, 360), (560 + 8, 360 - 46)], INK, 4)


def _lamp_glow(c, x, y, k=1.0):
    for r, a in [(170, 0.18), (120, 0.3), (80, 0.45)]:
        c.circle(x, y, r * k, fade(LAMP, a), shadow=False)


def _desk(c, kid_x, droop, pages):
    _lamp_glow(c, 450, 790)
    kid(c, kid_x, GROUND, 200, angle=droop)
    c.rrect(180, 830, 560, 852, 3, (120, 86, 52))               # desk top
    c.rrect(200, 852, 230, GROUND, 2, (100, 70, 42))
    c.rrect(510, 852, 540, GROUND, 2, (100, 70, 42))
    c.line([(470, 830), (470, 760)], INK, 5)                    # lamp
    c.poly([(440, 760), (500, 760), (485, 730), (455, 730)], RED)
    for j in range(pages):
        c.rrect(250, 818 - j * 9, 340, 828 - j * 9, 2, [CARD, TEAL_L, RED][j % 3])


def night_homework(c, t, dur, p):
    ground(c)
    _room_night(c, t, p)
    droop = -0.08 - 0.06 * math.sin(t * 1.3) * seg(p, 0.2, 1)
    _desk(c, 330, droop, 3 + int(seg(p, 0, 0.8) * 6))
    # parent appears in the doorway, watching
    c.rrect(590, 600, 700, GROUND, 4, (196, 186, 168))
    k = ease_out(seg(p, 0.35, 0.65))
    if k > 0:
        person(c, lerp(760, 640, k), GROUND, 250, INK)
    if p > 0.7:
        q = ease_back(seg(p, 0.7, 0.85))
        question_mark(c, 660, 640 + math.sin(t * 2) * 5, 60 * q, color=CARD)


def ai_answers(c, t, dur, p):
    ground(c)
    _room_night(c, t, p)
    _desk(c, 330, -0.04, 5)
    rk = ease_back(seg(p, 0.05, 0.25))
    rx, ry = 600, 640 + math.sin(t * 3) * 8
    robot(c, rx, ry, 90 * rk, look=-1, blink=int(t * 2.5) % 6 == 0)
    for i in range(6):
        k = seg(p, 0.25 + i * 0.09, 0.4 + i * 0.09)
        if 0 < k < 1:
            e = ease_in_out(k)
            x = lerp(rx - 40, 300, e)
            y = lerp(ry, 800, e) - math.sin(math.pi * e) * 120
            c.rrect(x - 34, y - 16, x + 34, y + 16, 4, CARD)
            c.text(x, y, "answer", 14, GREY, "mono")
    if p > 0.75:
        c.text(300, 690, "0.2s", 30, fade(RED, seg(p, 0.75, 0.85)), "mono")


def _gift_icon(c, kind, x, y, s):
    if kind == "q":
        question_mark(c, x, y, 90 * s)
    elif kind == "eye":
        c.poly([(x - 62 * s, y), (x, y - 36 * s), (x + 62 * s, y), (x, y + 36 * s)], INK, shadow=False)
        c.poly([(x - 52 * s, y), (x, y - 28 * s), (x + 52 * s, y), (x, y + 28 * s)], WHITE, shadow=False)
        c.circle(x, y, 26 * s, TEAL_L, shadow=False)
        c.circle(x, y, 11 * s, INK, shadow=False)
    elif kind == "path":
        c.line([(x, y + 45 * s), (x, y - 40 * s)], INK, 6 * s)
        c.poly([(x, y - 40 * s), (x + 60 * s, y - 40 * s), (x + 75 * s, y - 25 * s), (x + 60 * s, y - 10 * s), (x, y - 10 * s)], TEAL_L)
        c.poly([(x, y - 5 * s), (x - 60 * s, y - 5 * s), (x - 75 * s, y + 10 * s), (x - 60 * s, y + 25 * s), (x, y + 25 * s)], RED)
    else:
        c.circle(x - 22 * s, y - 12 * s, 26 * s, RED, shadow=False)
        c.circle(x + 22 * s, y - 12 * s, 26 * s, RED, shadow=False)
        c.poly([(x - 47 * s, y - 4 * s), (x + 47 * s, y - 4 * s), (x, y + 50 * s)], RED, shadow=False)


GIFTS = [("q", "ప్రశ్నించే తెలివి"), ("eye", "నిజాన్ని చూసే కళ్ళు"),
         ("path", "ఎంచుకునే ధైర్యం"), ("heart", "అర్థం చేసుకునే మనసు")]


def four_gifts(c, t, dur, p):
    # report card shrinks away on "marks కాదు", then four gifts arrive with each phrase
    rc = 1 - ease_in_out(seg(p, 0.12, 0.25))
    if rc > 0:
        w, h = 240 * rc, 300 * rc
        c.rrect(360 - w / 2, 560 - h / 2, 360 + w / 2, 560 + h / 2, 6, CARD)
        if rc > 0.6:
            c.text(360, 480, "MARKS", 30, INK, "mono")
            cross(c, 360, 570, 160 * rc, RED, p=seg(p, 0.04, 0.12), width=12)
    starts = [0.27, 0.43, 0.59, 0.75]
    for i, ((kind, name), st) in enumerate(zip(GIFTS, starts)):
        k = ease_back(seg(p, st, st + 0.1))
        if k <= 0:
            continue
        col, row = i % 2, i // 2
        x, y = 200 + col * 320, 420 + row * 300
        w, h = 280 * k, 250 * k
        c.rrect(x - w / 2, y - h / 2, x + w / 2, y + h / 2, 14, CARD)
        if k > 0.85:
            _gift_icon(c, kind, x, y - 30, 1.0)
            c.text(x, y + 80, name, 26, INK, "te")
    if p > 0.92:
        g = seg(p, 0.92, 1)
        c.rrect(60, 260, 660, 880, 20, None, shadow=False, outline=fade(RED, g), width=3)


SCENES = {f.__name__: f for f in [kid_class5, future_door, marks, questions, basics, hands, speak, fall_rise,
                                   ai_tool, ranks_skills, end, twelve_grid, memorize, focus, adapt,
                                   split_schools, home, thinker, money, fact_check, bias_scale,
                                   two_channels, choose, feelings, night_homework,
                                   ai_answers, four_gifts]}
