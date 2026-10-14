# Review — kids film v2

## Renderer and why
Python + Pillow (with libraqm for Telugu shaping), piped frame by frame into ffmpeg/x264.
- **Telugu shaping:** browser-based renderers would also work. This route was already proven here, and libraqm draws conjuncts correctly.
- **Deterministic:** every frame is a pure function of `frame_index`. The scene functions take `(t, dur, p)` and carry no state, so any frame or section re-renders identically.
- **One timeline:** shot lengths come from the VO files, and captions use measured word times from the same audio. Animation, captions and sound share one clock.
- **Repeatable:** run `python build.py kids_v2 --format both --deliver`.

## Pronunciation check (strict)
Method: all 12 VO lines were joined and transcribed with ElevenLabs Scribe (Telugu, confidence 0.9999), then compared word by word against the script.

| Line | Scripted | Heard | Action |
|---|---|---|---|
| 5 | నిజం **వెతకడం** | నిజం **బెతకటం** (వ→బ) | Re-worded to "నిజం ఏంటో **కనిపెట్టడం**", regenerated, re-checked: clean |
| 12 | **తీసుకెళ్తాయి** ×2 | **తీసుకెళ్తే** ×2 (ending swallowed, meaning changes) | Full form "**తీసుకువెళ్తాయి**", regenerated, re-checked: clean |
| 1 | దేనికోసం అని | దేనికోసమని | Natural spoken sandhi, kept |
| 2 | పెద్దయ్యే సరికి | పెద్ద అయ్యేసరికి | Same sounds, kept |
| 3 | ఇంకొకరిని | ఇంకొకర్ని | Colloquial contraction, kept |
| 5 | check | చెక్ | Same word, kept |

Limitation: speech-to-text agreeing with the script is strong evidence of correct pronunciation, but it is not proof. A native listener should still play it once. Stress, tone and "AI" said as "ఏఐ" are things a transcript can't judge.

## Scores (after fixes)
| Criterion | Before | After | Notes |
|---|---|---|---|
| Hook | 4 | 4 | Night homework + the question lands in 3 s |
| Readability | 3 | 4 | Captions on a paper plate above the Reels UI zone; 16:9 captions 50 px |
| Continuity | 3 | 5 | Shot 11 now uses the same 4 skill names as shot 3 |
| Motion | 4 | 4 | |
| Sound sync | 4 | 5 | Captions follow measured word starts; gift cards land within ~0.2 s of each spoken name |

## The three worst defects, and what was fixed
1. **Shot 11 showed stale skill chips** (ప్రశ్నలు / basics / projects / మాట / ధైర్యం) from the old cut. Replaced with a new scene, `rank_vs_habit`, using the four skill names.
2. **9:16 captions collided with artwork** in shots 10–12 (audience heads, skill stack, teal ground). Added a caption plate, lifted the end-scene ground band and the audience row, and moved the stack up.
3. **16:9 crop clipped the ground line and feet.** The crop window moved to y 250–970.

## Still needs human review
- **Listen once with headphones**, especially the emphasis on "ఏడవకు" in shot 9, which is the most emotional line.
- **"AI" pronunciation:** it's spoken as English "A-I". Decide whether you'd prefer "ఏఐ" written out.
- **Shot 6 has only one VO line** (bias). If you want it as strong as the other skills, add a "do at home" line (e.g. two news channels) for about 80 credits.
- **Platform crops:** check the 9:16 file in the Instagram/YouTube upload preview, because each app's UI overlay differs slightly.
- **No background music** (none was supplied). A soft bed would add emotion; give me a licensed track and I'll mix it under the VO at −22 dB.
