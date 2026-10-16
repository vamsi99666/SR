"""Shorten long pauses in VO lines using word timings, then speed up (pitch kept).

  python tighten.py <name> <raw_words.json> [--tempo 1.15] [--cap-word 0.12] [--cap-punct 0.30]

Reads audio/<name>_raw/NN.mp3 and a JSON {line_index: [[word, start, end], ...]}
(times relative to the start of each raw line). Writes audio/<name>/NN.mp3 and
audio/<name>/word_times.json with the word times mapped through the edit, so
captions stay in sync with the tightened audio.
"""
import argparse
import json
import os
import subprocess
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SR = 44100


def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("words")
    ap.add_argument("--tempo", type=float, default=1.15)
    ap.add_argument("--cap-word", type=float, default=0.12)
    ap.add_argument("--cap-punct", type=float, default=0.30)
    a = ap.parse_args()

    with open(a.words, encoding="utf-8") as f:
        words = {int(k): v for k, v in json.load(f).items()}
    out_dir = os.path.join(HERE, "audio", a.name)
    os.makedirs(out_dir, exist_ok=True)
    timings = {}
    fade = int(0.008 * SR)
    for i, ws in sorted(words.items()):
        x = load(os.path.join(HERE, "audio", f"{a.name}_raw", f"{i:02d}.mp3"))
        # keep-segments in raw time; long gaps lose their middle portion
        lead = max(0.0, ws[0][1] - 0.06)
        cuts = []  # (cut_start, cut_end) in raw seconds
        for (pw, ps, pe), (w, s, e) in zip(ws, ws[1:]):
            cap = a.cap_punct if pw[-1] in ",.?:;!" else a.cap_word
            gap = s - pe
            if gap > cap:
                mid = (pe + s) / 2
                cuts.append((mid - (gap - cap) / 2, mid + (gap - cap) / 2))
        end = min(len(x) / SR, ws[-1][2] + 0.25)
        keep, t = [], lead
        for c0, c1 in cuts:
            keep.append((t, c0))
            t = c1
        keep.append((t, end))
        pieces = []
        for k0, k1 in keep:
            seg = x[int(k0 * SR):int(k1 * SR)].copy()
            if len(seg) > 2 * fade:
                seg[:fade] *= np.linspace(0, 1, fade)
                seg[-fade:] *= np.linspace(1, 0, fade)
            pieces.append(seg)
        y = np.concatenate(pieces)

        def remap(tr):
            out, acc = 0.0, 0.0
            for k0, k1 in keep:
                if tr <= k1:
                    return (acc + max(0.0, tr - k0)) / a.tempo
                acc += k1 - k0
            return acc / a.tempo

        tmp = os.path.join(out_dir, f"_{i:02d}.wav")
        with wave.open(tmp, "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes(np.clip(y, -32768, 32767).astype(np.int16).tobytes())
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", f"atempo={a.tempo}", "-b:a", "160k",
                        os.path.join(out_dir, f"{i:02d}.mp3")], check=True)
        os.remove(tmp)
        timings[str(i)] = [[w, round(remap(s), 3), round(remap(e), 3)] for w, s, e in ws]
        print(f"{i:02d}: {ws[-1][2] - ws[0][1]:.2f}s -> {len(y) / SR / a.tempo:.2f}s")
    with open(os.path.join(out_dir, "word_times.json"), "w", encoding="utf-8") as f:
        json.dump(timings, f, ensure_ascii=False, indent=0)


if __name__ == "__main__":
    main()
