"""Download ElevenLabs generations into audio/<name>/NN.mp3 by matching each
generation's prompt to the script line it voices.

  python fetch_audio.py <script_name> <run_status.json> [...more status files]

The status JSON is the output of the ElevenLabs connector's
creative_get_flow_run_status call (a 'media' list with prompt + url).
"""
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    name, files = sys.argv[1], sys.argv[2:]
    with open(os.path.join(HERE, "scripts", f"{name}.json"), encoding="utf-8") as f:
        lines = [ln["te"].strip() for ln in json.load(f)["lines"]]
    out_dir = os.path.join(HERE, "audio", name)
    os.makedirs(out_dir, exist_ok=True)
    for fp in files:
        with open(fp, encoding="utf-8") as f:
            data = json.load(f)
        for m in data.get("media", []):
            prompt = m["prompt"].strip()
            if prompt not in lines:
                print(f"no matching line for: {prompt}")
                continue
            i = lines.index(prompt)
            path = os.path.join(out_dir, f"{i:02d}.mp3")
            urllib.request.urlretrieve(m["url"], path)
            print(f"{i:02d}  {m.get('duration_secs')}s  {prompt}")
    missing = [i for i in range(len(lines)) if not os.path.exists(os.path.join(out_dir, f"{i:02d}.mp3"))]
    print("missing:", missing or "none")


if __name__ == "__main__":
    main()
