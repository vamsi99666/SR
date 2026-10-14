"""Generate Telugu voiceover lines with ElevenLabs -> audio/<name>/NN.mp3

  export ELEVENLABS_API_KEY=...            # set as an environment secret, never commit it
  python tts.py --list-voices              # find a voice_id
  python tts.py jobs_pyramid --voice <voice_id> [--model eleven_v3] [--force]

One file per script line, so each scene is timed exactly to its line.
Existing files are skipped unless --force (saves credits on re-runs).
"""
import argparse
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
API = "https://api.elevenlabs.io/v1"


def call(method, path, key, body=None, raw=False):
    req = urllib.request.Request(API + path, method=method, headers={
        "xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg" if raw else "application/json"},
        data=json.dumps(body).encode() if body is not None else None)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
    except urllib.error.HTTPError as e:
        sys.exit(f"ElevenLabs {e.code}: {e.read().decode(errors='replace')[:500]}")
    return data if raw else json.loads(data)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name", nargs="?")
    ap.add_argument("--voice", default=os.environ.get("ELEVENLABS_VOICE_ID"))
    ap.add_argument("--model", default=os.environ.get("ELEVENLABS_MODEL", "eleven_v3"))
    ap.add_argument("--list-voices", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--stability", type=float, default=0.5)
    args = ap.parse_args()

    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        sys.exit("ELEVENLABS_API_KEY is not set")

    if args.list_voices:
        for v in call("GET", "/voices", key)["voices"]:
            labels = ", ".join(f"{k}={val}" for k, val in (v.get("labels") or {}).items())
            print(f"{v['voice_id']}  {v['name']}  [{v.get('category')}]  {labels}")
        return

    if not args.name or not args.voice:
        sys.exit("usage: tts.py <script_name> --voice <voice_id>")

    with open(os.path.join(HERE, "scripts", f"{args.name}.json"), encoding="utf-8") as f:
        lines = json.load(f)["lines"]
    out_dir = os.path.join(HERE, "audio", args.name)
    os.makedirs(out_dir, exist_ok=True)
    for i, ln in enumerate(lines):
        path = os.path.join(out_dir, f"{i:02d}.mp3")
        if os.path.exists(path) and not args.force:
            print(f"skip {path}")
            continue
        body = {"text": ln["te"], "model_id": args.model, "language_code": "te",
                "voice_settings": {"stability": args.stability, "similarity_boost": 0.8}}
        if args.model != "eleven_v3":  # request stitching keeps prosody consistent across lines
            if i > 0:
                body["previous_text"] = lines[i - 1]["te"]
            if i + 1 < len(lines):
                body["next_text"] = lines[i + 1]["te"]
        audio = call("POST", f"/text-to-speech/{args.voice}?output_format=mp3_44100_128", key, body, raw=True)
        with open(path, "wb") as f:
            f.write(audio)
        print(f"wrote {path} ({len(audio) // 1024} KB)")


if __name__ == "__main__":
    main()
