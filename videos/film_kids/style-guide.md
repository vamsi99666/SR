# Style guide — "4 skills" kids film (Telugu, female VO)

Derived from the reference reel (bird & fish paper-cutout piece) and the two films already rendered in this repo.

## 1. Look

| Token | Hex | Use |
|---|---|---|
| Paper | `#ECE6D9` + noise/fibre texture, light vignette | Background, always |
| Card | `#F7F4EE` | Label cards, speech bubbles, report card |
| Ink | `#1E1E1E` | Adults, outlines, text |
| Red | `#D4262B` | The child (hero), the "answer" accent, check marks, strikes |
| Teal | `#1F4A4C` / `#2C5F61` | Ground bands, secondary blocks, screens |
| Grey | `#B9B1A3` | Dimmed / rejected / "past" states |
| Shadow | `#CFC7B7`, offset (+4, +5) px, no blur | Every cutout shape — the paper-cutout signature |

Rules
- **The child is always red.** Adults are ink. Robots are slate with a teal face. A viewer should find the child in under 0.5 s in every shot.
- Flat shapes, hard drop shadow, no gradients, no outlines except deliberate strokes (magnifier, focus ring).
- Max 3 accent colours per shot.

## 2. Type

| Role | Font | Size (9:16 @720w) | Notes |
|---|---|---|---|
| Captions | Noto Sans Telugu Bold | 40 px, line-height 1.55 | Word-by-word reveal: spoken = ink, upcoming = `#AAA296` |
| Label card | Gurajada (hand-written feel) | 54 px | Card slides down 0.45 s, red underline draws in |
| Diagram tags | IBM Plex Mono | 18–30 px | English UI words only ("option 5", "CH 1", "FAKE?") |

Telugu shaping uses libraqm (verified conjuncts render correctly). English loan words stay in Latin script, as spoken.

## 3. Motion

- Entrances: `ease_back` pop, 0.25–0.45 s. Exits: hard cut or fall under gravity (`y += k²·d`).
- Idle life: everything on screen breathes (bob ±6 px at 2.5–4 Hz) so no frame is dead.
- One main action per line of VO; the action lands on the key word (± 0.3 s).
- Transitions: **hard cuts** between lines (matches reference). The label card persists across the two lines of the same skill, so each skill reads as one chapter.
- No camera moves, no zooms (keeps the paper-on-table feel).

## 4. Layout and safe zones

**9:16 (1080×1920 export, designed at 720×1280)**
- Label card: y 120–220
- Illustration: y 240–940
- Captions: centred y ≈ 1045 (38 px) on a paper-coloured plate (y 968–1180) so artwork never collides with text. v1 sat at y≈1110.
- Side gutters 40 px.

**16:9 (1920×1080)**
- Left: illustration square (9:16 art region y 250–970) scaled to 1000×1000 at (40, 40).
- Right panel (840 px): skill tracker (4 chips, current one red) → label → captions at 52 px.
- Same timeline, same frames-per-shot; only the composition differs.

## 5. Sound

- VO: ElevenLabs `eleven_v3`, female Telugu voice **Chandana M – Bright, Clear Tutor** (chosen by audition after Chaitra G was rejected). Every line is checked with Telugu speech-to-text against the script before render (see review.md).
- One VO file per shot; shot length = VO length + 0.35 s breath (last shot + 1.2 s hold). Captions are timed to the same clock.
- No music or SFX in v2 (none supplied).
- Night palette for the emotional opening: window `#1D2733`, lamp glow `#F6D678` in 3 soft rings.

## 6. Voice & copy rules

- Spoken Telugu, not textbook Telugu. English words where Telugu parents actually use them (tuition, marks, forward, judgment).
- Original wording only. The reference reel is used for **structure inspiration** (announce the skills first, then go one by one), not text.
- Every skill = one "why" line + one "do this at home" line.
