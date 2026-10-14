"""Render a faceless explainer video from scripts/<name>.json.

  python build.py jobs_pyramid            # full render -> out/jobs_pyramid.mp4
  python build.py jobs_pyramid --preview  # contact sheet of mid-scene stills

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
SCENE_MODULES = {"jobs_pyramid": "scenes_jobs", "kids_future": "scenes_kids"}
PAD = 0.35        # silence after each line
TAIL = 1.2        # hold on the last scene
SR = 44100

_bg = None
_ctx = None


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


def _init(name):
    global _bg, _ctx
    _bg = engine.make_paper()
    script = load(name)
    durs, _ = timeline(name, script)
    mod = importlib.import_module(SCENE_MODULES[name])
    starts = np.concatenate([[0], np.cumsum(durs)[:-1]])
    _ctx = (script, durs, starts, mod.SCENES)


def render_frame(fi):
    script, durs, starts, scenes = _ctx
    tg = fi / FPS
    i = int(np.searchsorted(starts, tg, side="right") - 1)
    ln, dur = script["lines"][i], durs[i]
    t = tg - starts[i]
    speak = dur - PAD - (TAIL if i == len(durs) - 1 else 0)
    p = min(1.0, t / dur)
    c = Canvas(_bg)
    scenes[ln["scene"]](c, t, dur, p)
    if ln.get("label"):
        label_card(c, ln["label"], seg(t, 0, 0.45), ln.get("label_new"),
                   seg(p, 0.3, 0.45), seg(p, 0.45, 0.6))
    caption(c, ln["te"], min(1.0, t / max(0.5, speak)))
    return c.finish().tobytes()


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name", choices=sorted(SCENE_MODULES))
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--workers", type=int, default=os.cpu_count())
    args = ap.parse_args()

    script = load(args.name)
    durs, have_audio = timeline(args.name, script)
    out_dir = os.path.join(HERE, "out")
    os.makedirs(out_dir, exist_ok=True)
    total = sum(durs)
    print(f"{args.name}: {len(durs)} scenes, {total:.1f}s, audio={'yes' if have_audio else 'no (estimated timing)'}")

    if args.preview:
        _init(args.name)
        starts = np.concatenate([[0], np.cumsum(durs)[:-1]])
        frames = []
        for s, d in zip(starts, durs):
            for frac in (0.3, 0.85):
                fi = int((s + d * frac) * FPS)
                frames.append(Image.frombytes("RGB", (W, H), render_frame(fi)).resize((W // 3, H // 3)))
        cols = 6
        rows = (len(frames) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * W // 3, rows * H // 3), "white")
        for k, im in enumerate(frames):
            sheet.paste(im, ((k % cols) * W // 3, (k // cols) * H // 3))
        path = os.path.join(out_dir, f"{args.name}_preview.jpg")
        sheet.save(path, quality=85)
        print(path)
        return

    n_frames = int(total * FPS)
    silent = os.path.join(out_dir, f"{args.name}_silent.mp4")
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                           "-pix_fmt", "yuv420p", silent], stdin=subprocess.PIPE)
    with Pool(args.workers, initializer=_init, initargs=(args.name,)) as pool:
        for k, fr in enumerate(pool.imap(render_frame, range(n_frames), chunksize=8)):
            ff.stdin.write(fr)
            if k % 300 == 0:
                print(f"  frame {k}/{n_frames}", file=sys.stderr)
    ff.stdin.close()
    ff.wait()

    final = os.path.join(out_dir, f"{args.name}.mp4")
    if have_audio:
        wav = os.path.join(out_dir, f"{args.name}_voice.wav")
        build_audio(args.name, durs, wav)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", silent, "-i", wav, "-c:v", "copy", "-c:a", "aac",
                        "-b:a", "160k", "-shortest", "-movflags", "+faststart", final], check=True)
        os.remove(silent)
    else:
        os.replace(silent, final)
    print(final)


if __name__ == "__main__":
    main()
