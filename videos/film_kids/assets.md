# Assets list — kids film v2

| Asset | Source | Location | Licence / notes |
|---|---|---|---|
| Voice-over, 12 lines | ElevenLabs `eleven_v3`, voice "Chaitra G – Calm, Motivational Narrator" (`PnktIx9i1QQBGfm7h7cd`) | `audio/kids_v2/00–11.mp3` (not committed; regenerate from the flow or `tts.py`) | Generated in your ElevenLabs account |
| Word timings | ElevenLabs Scribe transcript of the VO | `audio/kids_v2/word_times.json` | Derived data |
| Noto Sans Telugu (Bold, Regular) | Google Fonts | `fonts/` | SIL Open Font License |
| Gurajada (labels) | Google Fonts | `fonts/` | SIL OFL |
| Mandali | Google Fonts | `fonts/` | SIL OFL (unused in this film) |
| IBM Plex Mono (UI tags) | Google Fonts | `fonts/` | SIL OFL |
| All illustrations, characters, paper texture | Drawn in code | `engine.py`, `scenes_kids.py` | Original |
| Script | Original Telugu copy written for this film | `scripts/kids_v2.json` | Yours. The reference reel informed only the structure (announce the skills, then explain each) |
| Music / SFX | None | — | None supplied |

## Outputs
- `out/kids_v2.mp4`: 9:16, 1080×1920, 30 fps, H.264 + AAC
- `out/kids_v2_16x9.mp4`: 16:9, 1920×1080
- `out/kids_v2_portrait_poster.png`, `out/kids_v2_landscape_poster.png`
- `out/kids_v2_portrait_contact.jpg`, `out/kids_v2_landscape_contact.jpg`

## Render command
```
cd videos
python build.py kids_v2 --format both --deliver
```
