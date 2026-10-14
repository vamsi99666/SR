"""Render a faceless explainer video from scripts/<name>.json.

  python build.py jobs_pyramid            # full render -> out/jobs_pyramid.mp4
  python build.py jobs_pyramid --preview  # contact sheet of mid-scene stills
  python build.py kids_v2 --format both   # 9:16 (1080x1920) and 16:9 (1920x1080)
  python build.py kids_v2 --format both --deliver   # + posters and contact sheets

Every frame is a pure function of its index (no state carried between frames),
so any frame or section can be re-rendered on its own and comes out identical.

If audio/<name>/NN.mp3 files exist (from tts.py) each scene lasts as long as its
voice line and the voiceover is muxed in. Otherwise durations are estimated and
the video is silent (useful for checking animation before spending credits).
"""
import argparse
import importlib
import json
import os
import subprocess
import sys
import wave
from multiprocessing import Pool

import numpy as np
from PIL import Image

import engine
from engine import W, H, FPS, Canvas, caption, label_card, seg

HERE = os.path.dirname(os.path.abspath(__file__))
SCENE_MODULES = {"jobs_pyramid": "scenes_jobs", "kids_future": "scenes_kids",
                 "kids_v2": "scenes_kids", "kids_sample": "scenes_kids"}
PAD = 0.35        # silence after each line
TAIL = 1.2        # hold on the last scene
SR = 44100

_bg = None
_bg_land = None
_ctx = None
_fmt = "portrait"
OUT = {"portrait": (1080, 1920), "landscape": (1920, 1080)}


def load(name):
    with open(os.path.join(HERE, "scripts", f"{name}.json"), encoding="utf-8") as f:
        return json.load(f)


def audio_path(name, i):
    return os.path.join(HERE, "audio", name, f"{i:02d}.mp3")


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True, check=True).stdout
    return float(out.strip())


def timeline(name, script):
    have_audio = all(os.path.exists(audio_path(name, i)) for i in range(len(script["lines"])))
    durs = []
    for i, ln in enumerate(script["lines"]):
        if have_audio:
            d = probe(audio_path(name, i)) + PAD
        else:
            d = max(2.4, len(ln["te"]) / 13.0 + 0.6)
        if i == len(script["lines"]) - 1:
            d += TAIL
        durs.append(d)
    return durs, have_audio


def word_times(name):
    p = os.path.join(HERE, "audio", name, "word_times.json")
    if not os.path.exists(p):
        return {}
    with open(p, encoding="utf-8") as f:
        return {int(k): [w[1] for w in v] for k, v in json.load(f).items()}


def _init(name, fmt="portrait"):
    global _bg, _bg_land, _ctx, _fmt
    _fmt = fmt
    _bg = engine.make_paper()
    if fmt == "landscape":
        _bg_land = engine.make_paper(1920 * engine.S, 1080 * engine.S)
    script = load(name)
    durs, _ = timeline(name, script)
    mod = importlib.import_module(SCENE_MODULES[name])
    starts = np.concatenate([[0], np.cumsum(durs)[:-1]])
    _ctx = (script, durs, starts, mod.SCENES, word_times(name))


def _locate(fi):
    script, durs, starts, scenes, wt = _ctx
    tg = fi / FPS
    i = int(np.searchsorted(starts, tg, side="right") - 1)
    ln, dur = script["lines"][i], durs[i]
    t = tg - starts[i]
    speak = dur - PAD - (TAIL if i == len(durs) - 1 else 0)
    return script, i, ln, dur, t, min(1.0, t / dur), min(1.0, t / max(0.5, speak)), wt.get(i)


def _scene(fi):
    script, i, ln, dur, t, p, cp, starts = _locate(fi)
    c = Canvas(_bg)
    _ctx[3][ln["scene"]](c, t, dur, p)
    return c, script, i, ln, t, p, cp, starts


def render_portrait(fi):
    c, script, i, ln, t, p, cp, starts = _scene(fi)
    lay = script.get("layout", {})
    if ln.get("label"):
        label_card(c, ln["label"], seg(t, 0, 0.45), ln.get("label_new"),
                   seg(p, 0.3, 0.45), seg(p, 0.45, 0.6))
    if lay.get("caption_plate"):
        c.rrect(10, 968, 710, 1180, 18, engine.PAPER, shadow=False)
    caption(c, ln["te"], cp, y=lay.get("caption_y", 1110), size=lay.get("caption_size", 40),
            starts=starts, t=t)
    return c.img.resize(OUT["portrait"], Image.LANCZOS).tobytes()


class _LCanvas(Canvas):
    pass


def _tracker(lc, script, ln):
    names = script.get("skills")
    if not names:
        return
    lab = ln.get("label") or ""
    cur = int(lab[0]) - 1 if lab[:1].isdigit() else -1
    for k, nm in enumerate(names):
        x0, y0 = 1110 + (k % 2) * 390, 70 + (k // 2) * 90
        if k == cur:
            fill, col = engine.RED, engine.WHITE
        elif cur >= 0 and k < cur:
            fill, col = engine.INK, engine.WHITE
        else:
            fill, col = engine.CARD, (150, 142, 130)
        lc.rrect(x0, y0, x0 + 370, y0 + 70, 10, fill)
        lc.text(x0 + 185, y0 + 35, nm, 30, col, "te")


def render_landscape(fi):
    c, script, i, ln, t, p, cp, starts = _scene(fi)
    S = engine.S
    art = c.img.crop((0, 250 * S, 720 * S, 970 * S)).resize((1000 * S, 1000 * S), Image.LANCZOS)
    lc = _LCanvas(_bg_land)
    lc.img.paste(art, (40 * S, 40 * S))
    lc.line([(1070, 80), (1070, 1000)], (210, 202, 188), 2)
    _tracker(lc, script, ln)
    if ln.get("label"):
        k = engine.ease_out(seg(t, 0, 0.45))
        lc.text(1495, 330 - 30 * (1 - k), ln["label"], 66, engine.fade(engine.INK, k), "hand")
        w = lc.text_w(ln["label"], 66, "hand")
        lc.line([(1495 - w / 2, 385), (1495 - w / 2 + w * k, 385)], engine.RED, 3)
    caption(lc, ln["te"], cp, y=720, size=50, max_w=740, cx=1495, starts=starts, t=t)
    return lc.img.resize(OUT["landscape"], Image.LANCZOS).tobytes()


def render_frame(fi):
    return render_landscape(fi) if _fmt == "landscape" else render_portrait(fi)


def build_audio(name, durs, out_wav):
    chunks = []
    for i, d in enumerate(durs):
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", audio_path(name, i), "-f", "s16le", "-ac", "1",
                              "-ar", str(SR), "-"], capture_output=True, check=True).stdout
        a = np.frombuffer(raw, np.int16)
        n = int(round(d * SR))
        buf = np.zeros(n, np.int16)
        buf[:min(n, len(a))] = a[:n]
        chunks.append(buf)
    with wave.open(out_wav, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(np.concatenate(chunks).tobytes())


def contact_sheet(name, fmt, durs, out_dir, fracs=(0.3, 0.85)):
    """Two stills per shot, stamped with shot number and time."""
    from PIL import ImageDraw
    _init(name, fmt)
    starts = np.concatenate([[0], np.cumsum(durs)[:-1]])
    ow, oh = OUT[fmt]
    tw = 270 if fmt == "portrait" else 480
    th = int(tw * oh / ow)
    tiles = []
    for k, (s0, d) in enumerate(zip(starts, durs)):
        for frac in fracs:
            fi = int((s0 + d * frac) * FPS)
            im = Image.frombytes("RGB", (ow, oh), render_frame(fi)).resize((tw, th), Image.LANCZOS)
            dr = ImageDraw.Draw(im)
            dr.rectangle([0, 0, 150, 22], fill=(30, 30, 30))
            dr.text((6, 5), f"#{k + 1}  {fi / FPS:5.2f}s", fill=(255, 255, 255))
            tiles.append(im)
    cols = 6 if fmt == "portrait" else 4
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * th), "white")
    for k, im in enumerate(tiles):
        sheet.paste(im, ((k % cols) * tw, (k // cols) * th))
    path = os.path.join(out_dir, f"{name}_{fmt}_contact.jpg")
    sheet.save(path, quality=85)
    return path


def poster(name, fmt, durs, out_dir, at=None):
    _init(name, fmt)
    total = sum(durs)
    fi = int((at if at is not None else total - 0.6) * FPS)
    path = os.path.join(out_dir, f"{name}_{fmt}_poster.png")
    Image.frombytes("RGB", OUT[fmt], render_frame(fi)).save(path)
    return path


def render_video(name, fmt, durs, have_audio, out_dir, workers):
    total = sum(durs)
    n_frames = int(total * FPS)
    ow, oh = OUT[fmt]
    suffix = "" if fmt == "portrait" else "_16x9"
    silent = os.path.join(out_dir, f"{name}{suffix}_silent.mp4")
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{ow}x{oh}",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                           "-pix_fmt", "yuv420p", silent], stdin=subprocess.PIPE)
    with Pool(workers, initializer=_init, initargs=(name, fmt)) as pool:
        for k, fr in enumerate(pool.imap(render_frame, range(n_frames), chunksize=8)):
            ff.stdin.write(fr)
            if k % 300 == 0:
                print(f"  [{fmt}] frame {k}/{n_frames}", file=sys.stderr)
    ff.stdin.close()
    ff.wait()
    final = os.path.join(out_dir, f"{name}{suffix}.mp4")
    if have_audio:
        wav = os.path.join(out_dir, f"{name}_voice.wav")
        build_audio(name, durs, wav)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", silent, "-i", wav, "-c:v", "copy", "-c:a", "aac",
                        "-b:a", "160k", "-shortest", "-movflags", "+faststart", final], check=True)
        os.remove(silent)
    else:
        os.replace(silent, final)
    return final


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name", choices=sorted(SCENE_MODULES))
    ap.add_argument("--preview", action="store_true", help="contact sheet(s) only")
    ap.add_argument("--format", choices=["portrait", "landscape", "both"], default="portrait")
    ap.add_argument("--deliver", action="store_true", help="also write posters and contact sheets")
    ap.add_argument("--workers", type=int, default=os.cpu_count())
    args = ap.parse_args()

    script = load(args.name)
    durs, have_audio = timeline(args.name, script)
    out_dir = os.path.join(HERE, "out")
    os.makedirs(out_dir, exist_ok=True)
    print(f"{args.name}: {len(durs)} scenes, {sum(durs):.1f}s, audio={'yes' if have_audio else 'no (estimated timing)'}")
    fmts = ["portrait", "landscape"] if args.format == "both" else [args.format]
    for fmt in fmts:
        if args.preview or args.deliver:
            print(contact_sheet(args.name, fmt, durs, out_dir))
        if args.preview:
            continue
        print(render_video(args.name, fmt, durs, have_audio, out_dir, args.workers))
        if args.deliver:
            print(poster(args.name, fmt, durs, out_dir))


if __name__ == "__main__":
    main()
