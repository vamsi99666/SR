"""Paper-cutout animation engine: drawing primitives, captions, label cards.

All coordinates are in a 720x1280 design space. Frames are drawn at 2x and
downscaled for antialiasing.
"""
import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, S, FPS = 720, 1280, 2, 30
HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")

PAPER = (236, 230, 217)
CARD = (247, 244, 236)
INK = (30, 30, 30)
RED = (212, 38, 43)
TEAL = (31, 74, 76)
TEAL_L = (44, 95, 97)
GREY = (185, 177, 163)
SHADOW = (207, 199, 183)
WHITE = (250, 248, 242)
ROBOT = (74, 79, 85)

FONTS = {
    "te": "NotoSansTelugu-Bold.ttf",
    "te_reg": "NotoSansTelugu-Regular.ttf",
    "hand": "Gurajada.ttf",
    "mono": "IBMPlexMono.ttf",
    "soft": "Mandali.ttf",
}
_font_cache = {}


def font(name, size):
    key = (name, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(
            os.path.join(FONT_DIR, FONTS[name]), int(size * S),
            layout_engine=ImageFont.Layout.RAQM)
    return _font_cache[key]


# ---------- easing / timing ----------

def clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


def seg(p, a, b):
    """Map p in [a,b] to [0,1], clamped."""
    return clamp((p - a) / (b - a)) if b > a else float(p >= b)


def ease_out(x):
    return 1 - (1 - x) ** 3


def ease_in_out(x):
    return 3 * x * x - 2 * x * x * x


def ease_back(x):
    if x <= 0:
        return 0.0
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def lerp(a, b, t):
    return a + (b - a) * t


def mix(c1, c2, t):
    return tuple(int(lerp(a, b, t)) for a, b in zip(c1, c2))


def fade(color, a):
    """Fade a colour into the paper (fake alpha on a flat background)."""
    return mix(PAPER, color, clamp(a))


# ---------- background ----------

def make_paper(w=W * S, h=H * S):
    rng = np.random.default_rng(7)
    base = np.empty((h, w, 3), np.float32)
    base[:] = PAPER
    noise = rng.normal(0, 3.2, (h // 4, w // 4)).astype(np.float32)
    noise = np.kron(noise, np.ones((4, 4), np.float32))[:h, :w]
    fine = rng.normal(0, 2.0, (h, w)).astype(np.float32)
    yy, xx = np.mgrid[0:h, 0:w]
    vig = ((xx / w - 0.5) ** 2 + (yy / h - 0.5) ** 2) * 22
    base -= (noise + fine + vig)[..., None]
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    r = random.Random(3)
    for _ in range(260):  # paper fibres
        x, y = r.uniform(0, w), r.uniform(0, h)
        a, ln = r.uniform(0, math.pi), r.uniform(6, 22) * S
        c = r.choice([(222, 215, 200), (243, 239, 230)])
        d.line([(x, y), (x + math.cos(a) * ln, y + math.sin(a) * ln)], fill=c, width=1)
    return img


# ---------- canvas ----------

class Canvas:
    def __init__(self, bg):
        self.img = bg.copy()
        self.d = ImageDraw.Draw(self.img)

    @staticmethod
    def _p(pts):
        return [(x * S, y * S) for x, y in pts]

    def poly(self, pts, fill, shadow=True, outline=None):
        if shadow:
            self.d.polygon(self._p([(x + 4, y + 5) for x, y in pts]), fill=SHADOW)
        self.d.polygon(self._p(pts), fill=fill, outline=outline)

    def circle(self, x, y, r, fill, shadow=True, outline=None, width=0):
        if r < 0.5:
            return
        if shadow:
            self.d.ellipse([(x - r + 4) * S, (y - r + 5) * S, (x + r + 4) * S, (y + r + 5) * S], fill=SHADOW)
        self.d.ellipse([(x - r) * S, (y - r) * S, (x + r) * S, (y + r) * S], fill=fill,
                       outline=outline, width=int(width * S))

    def rrect(self, x0, y0, x1, y1, r, fill, shadow=True, outline=None, width=0):
        if x1 - x0 < 1 or y1 - y0 < 1:
            return
        r = min(r, (x1 - x0) / 2, (y1 - y0) / 2)
        if shadow:
            self.d.rounded_rectangle([(x0 + 4) * S, (y0 + 5) * S, (x1 + 4) * S, (y1 + 5) * S], r * S, fill=SHADOW)
        self.d.rounded_rectangle([x0 * S, y0 * S, x1 * S, y1 * S], r * S, fill=fill,
                                 outline=outline, width=int(width * S))

    def line(self, pts, fill, width=3):
        self.d.line(self._p(pts), fill=fill, width=int(width * S), joint="curve")

    def arc(self, x, y, r, a0, a1, fill, width=3):
        self.d.arc([(x - r) * S, (y - r) * S, (x + r) * S, (y + r) * S], a0, a1, fill=fill, width=int(width * S))

    def text(self, x, y, s, size, fill=INK, fname="te", anchor="mm"):
        size = int(round(size))
        if size < 4:
            return
        self.d.text((x * S, y * S), s, font=font(fname, size), fill=fill, anchor=anchor)

    def text_w(self, s, size, fname="te"):
        return self.d.textlength(s, font=font(fname, size)) / S

    def dashed(self, p0, p1, fill, width=2, dash=10):
        (x0, y0), (x1, y1) = p0, p1
        n = max(1, int(math.hypot(x1 - x0, y1 - y0) / dash))
        for i in range(0, n, 2):
            a, b = i / n, min(1, (i + 1) / n)
            self.line([(lerp(x0, x1, a), lerp(y0, y1, a)), (lerp(x0, x1, b), lerp(y0, y1, b))], fill, width)

    def arrow(self, p0, p1, fill=INK, width=2.5, head=12):
        self.line([p0, p1], fill, width)
        ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
        for s in (2.6, -2.6):
            self.line([p1, (p1[0] + head * math.cos(ang + s), p1[1] + head * math.sin(ang + s))], fill, width)

    def finish(self):
        return self.img.resize((W, H), Image.LANCZOS)


# ---------- characters ----------

def _rot(pts, cx, cy, ang):
    ca, sa = math.cos(ang), math.sin(ang)
    return [(cx + (x - cx) * ca - (y - cy) * sa, cy + (x - cx) * sa + (y - cy) * ca) for x, y in pts]


def person(c, x, y, h, color, angle=0.0, kid=False, walk=None, arm=None, head_color=None,
           scale=1.0, shadow=True):
    """Cutout figure with feet at (x, y). angle rotates around the feet (radians).
    walk: phase in radians for leg swing. arm: None | 'up' | 'point' | 'wave:<phase>'."""
    h = h * scale
    if h <= 1:
        return
    head_r = h * (0.15 if kid else 0.12)
    head_y = -h + head_r
    hip = -h * (0.40 if not kid else 0.36)
    sh = head_y + head_r + h * 0.03

    def T(pts):
        pts = [(x + px, y + py) for px, py in pts]
        return _rot(pts, x, y, angle) if angle else pts

    lw = h * 0.12
    swing = math.sin(walk) * 0.45 if walk is not None else 0.0
    for side, sgn in ((-1, 1), (1, -1)):
        lx = side * h * 0.07
        leg = [(lx - lw / 2, hip), (lx + lw / 2, hip), (lx + lw / 2, 0), (lx - lw / 2, 0)]
        leg = _rot(leg, lx, hip, swing * sgn)
        c.poly(T(leg), color, shadow)
    bw_top, bw_bot = h * 0.36, h * 0.30
    body = [(-bw_top / 2, sh), (bw_top / 2, sh), (bw_bot / 2, hip + h * 0.04), (-bw_bot / 2, hip + h * 0.04)]
    c.poly(T(body), color, shadow)
    if arm:
        aw = h * 0.09
        if arm == "up":
            ap = [(bw_top / 2 - aw, sh), (bw_top / 2, sh), (bw_top / 2 + h * 0.18, sh - h * 0.30),
                  (bw_top / 2 + h * 0.18 - aw, sh - h * 0.32)]
        elif arm == "point":
            ap = [(bw_top / 2 - aw / 2, sh + 2), (bw_top / 2, sh + aw), (bw_top / 2 + h * 0.34, sh - h * 0.04 + aw),
                  (bw_top / 2 + h * 0.34, sh - h * 0.04)]
        else:  # wave:<phase>
            ph = float(arm.split(":")[1])
            a = -0.9 + math.sin(ph) * 0.45
            ap = _rot([(bw_top / 2 - aw / 2, sh), (bw_top / 2 + aw / 2, sh), (bw_top / 2 + aw / 2, sh + h * 0.32),
                       (bw_top / 2 - aw / 2, sh + h * 0.32)], bw_top / 2, sh, a + math.pi)
        c.poly(T(ap), color, shadow)
    hx, hy = T([(0, head_y)])[0]
    c.circle(hx, hy, head_r, head_color or color, shadow)


def robot(c, x, y, s, color=ROBOT, look=0.0, blink=False, shadow=True):
    """Boxy robot centred at (x, y), size s (head width)."""
    if s <= 1:
        return
    c.line([(x, y - s * 0.5), (x, y - s * 0.78)], color, max(2, s * 0.05))
    c.circle(x, y - s * 0.82, s * 0.08, RED, shadow)
    c.rrect(x - s / 2, y - s / 2, x + s / 2, y + s * 0.25, s * 0.16, color, shadow)
    c.rrect(x - s * 0.38, y - s * 0.36, x + s * 0.38, y + s * 0.12, s * 0.10, TEAL_L, False)
    ex = s * 0.17
    for sx in (-1, 1):
        if blink:
            c.line([(x + sx * ex - s * 0.07 + look * s * 0.06, y - s * 0.12),
                    (x + sx * ex + s * 0.07 + look * s * 0.06, y - s * 0.12)], WHITE, s * 0.04)
        else:
            c.circle(x + sx * ex + look * s * 0.06, y - s * 0.12, s * 0.07, WHITE, False)
    c.rrect(x - s * 0.36, y + s * 0.30, x + s * 0.36, y + s * 0.80, s * 0.10, color, shadow)
    c.circle(x, y + s * 0.55, s * 0.08, RED, False)


def question_mark(c, x, y, size, color=RED):
    c.text(x, y, "?", size, color, "te")


def check(c, x, y, s, color=RED, p=1.0):
    pts = [(x - s * 0.5, y), (x - s * 0.15, y + s * 0.35), (x + s * 0.55, y - s * 0.45)]
    if p <= 0:
        return
    if p < 0.5:
        q = p / 0.5
        c.line([pts[0], (lerp(pts[0][0], pts[1][0], q), lerp(pts[0][1], pts[1][1], q))], color, s * 0.14)
    else:
        q = (p - 0.5) / 0.5
        c.line([pts[0], pts[1], (lerp(pts[1][0], pts[2][0], q), lerp(pts[1][1], pts[2][1], q))], color, s * 0.14)


def cross(c, x, y, s, color=RED, p=1.0, width=None):
    w = width or s * 0.14
    a = clamp(p * 2)
    b = clamp(p * 2 - 1)
    if a > 0:
        c.line([(x - s / 2, y - s / 2), (x - s / 2 + s * a, y - s / 2 + s * a)], color, w)
    if b > 0:
        c.line([(x + s / 2, y - s / 2), (x + s / 2 - s * b, y - s / 2 + s * b)], color, w)


def ground(c, y=960, color=INK):
    c.line([(0, y), (W, y)], color, 2)


# ---------- label card (top) ----------

def label_card(c, text, p_in, new_text=None, p_strike=0.0, p_new=0.0, y=170):
    """Handwritten label on a paper card, sliding in from the top."""
    if p_in <= 0:
        return
    e = ease_out(p_in)
    yy = lerp(y - 120, y, e)
    size = 54
    tw = c.text_w(text, size, "hand")
    nw = c.text_w(new_text, size, "hand") if new_text else 0
    w = max(tw, nw) + 70
    hgt = 96 if not new_text else 160
    x0 = W / 2 - w / 2
    c.rrect(x0, yy - 40, x0 + w, yy - 40 + hgt, 4, CARD)
    c.line([(x0 + 18, yy + 38), (x0 + 18 + (w - 36) * clamp(p_in * 1.3), yy + 38)], RED, 2)
    c.text(W / 2, yy - 2, text, size, INK, "hand")
    if new_text:
        if p_strike > 0:
            c.line([(W / 2 - tw / 2 - 6, yy + 2), (W / 2 - tw / 2 - 6 + (tw + 12) * ease_out(p_strike), yy - 4)], RED, 4)
        if p_new > 0:
            c.text(W / 2, yy + 66, new_text, size, fade(RED, p_new), "hand")


# ---------- captions ----------

def _caption_layout(c, words, size, max_w):
    lines, cur, cur_w = [], [], 0
    sp = c.text_w(" ", size)
    for wd in words:
        ww = c.text_w(wd, size)
        if cur and cur_w + sp + ww > max_w:
            lines.append(cur)
            cur, cur_w = [], 0
        cur_w += (sp if cur else 0) + ww
        cur.append((wd, ww))
    if cur:
        lines.append(cur)
    return lines, sp


def caption(c, text, p, y=1110, size=40, max_w=620, cx=None, starts=None, t=None):
    """Word-by-word reveal: spoken words in ink, upcoming words greyed.
    starts: measured word start times (s) from speech-to-text; when given, each
    script word lights up exactly when it is spoken (mapped by index if the
    transcript splits words differently)."""
    cx = W / 2 if cx is None else cx
    words = text.split()
    if starts and t is not None:
        n, m = len(words), len(starts)
        shown = 0
        for i in range(n):
            j = round(i * (m - 1) / max(1, n - 1)) if m != n else i
            if t >= starts[j] - 0.05:
                shown = i + 1
    else:
        weights = [len(w) + 2 for w in words]
        tot = sum(weights)
        span = clamp((p - 0.02) / 0.88)
        acc, shown = 0, 0
        for wt in weights:
            if span * tot >= acc + wt * 0.3:
                shown += 1
            acc += wt
    lines, sp = _caption_layout(c, words, size, max_w)
    lh = size * 1.55
    y0 = y - (len(lines) - 1) * lh / 2
    idx = 0
    for li, ln in enumerate(lines):
        total = sum(w for _, w in ln) + sp * (len(ln) - 1)
        x = cx - total / 2
        for wd, ww in ln:
            col = INK if idx < shown else (170, 162, 150)
            c.text(x, y0 + li * lh, wd, size, col, "te", anchor="lm")
            x += ww + sp
            idx += 1
