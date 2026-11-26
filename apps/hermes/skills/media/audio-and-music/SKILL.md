---
name: audio-and-music
description: "Songwriting craft, Suno AI prompts, HeartMuLa local generation, and audio analysis/spectrograms."
version: 1.0.0
platforms: [linux, macos, windows]
tags: [songwriting, music, suno, parody, lyrics, heartmula, heartcodec, audio, generation, spectrogram, visualization, analysis]
related_skills: []
triggers:
  - writing a song
  - song lyrics
  - music prompt
  - suno prompt
  - parody song
  - adapting a song
  - AI music generation
  - generate music locally
  - open-source music generation
  - HeartMuLa
  - heartlib
  - spectrogram
  - audio analysis
  - visualizing audio features
  - mel spectrogram
  - chroma
  - MFCC
  - debugging audio output
---

# Audio & Music

This skill covers three areas:
1. **Songwriting craft & Suno AI prompts** — writing, structuring, and AI-generating songs
2. **HeartMuLa local generation** — open-source Suno-like offline music from lyrics + tags
3. **Audio analysis & spectrograms** — visualizing audio files with songsee

For Meta AudioCraft (MusicGen/AudioGen), see **Part 4** of this skill below.

---

## Part 1: Songwriting Craft & Suno AI

Everything here is a GUIDELINE, not a rule. Art breaks rules on purpose.
Use what serves the song. Ignore what doesn't.

### 1.1 Song Structure

Common skeletons — mix, modify, or throw out as needed:

```
ABABCB  Verse/Chorus/Verse/Chorus/Bridge/Chorus    (most pop/rock)
AABA    Verse/Verse/Bridge/Verse (refrain-based)    (jazz standards, ballads)
ABAB    Verse/Chorus alternating                    (simple, direct)
AAA     Verse/Verse/Verse (strophic, no chorus)     (folk, storytelling)
```

The six building blocks:
- Intro      — set the mood, pull the listener in
- Verse      — the story, the details, the world-building
- Pre-Chorus — optional tension ramp before the payoff
- Chorus     — the emotional core, the part people remember
- Bridge     — a detour, a shift in perspective or key
- Outro      — the farewell, can echo or subvert the rest

### 1.2 Rhyme, Meter, and Sound

RHYME TYPES (from tight to loose):
- Perfect: lean/mean
- Family: crate/braid
- Assonance: had/glass (same vowels, different endings)
- Consonance: scene/when (different vowels, similar endings)
- Near/slant: enough to suggest connection without locking it down

Mix them. All perfect rhymes can sound like a nursery rhyme.
All slant rhymes can sound lazy. The blend is where it lives.

INTERNAL RHYME: Rhyming within a line, not just at the ends.
  "We pruned the lies from bleeding trees / Distilled the storm
   from entropy" — "lies/flies," "trees/entropy" create internal echoes.

METER: The rhythm of stressed vs unstressed syllables.
- Matching syllable counts between parallel lines helps singability
- The STRESSED syllables matter more than total count
- Say it out loud. If you stumble, the meter needs work.
- Intentionally breaking meter can create emphasis or surprise

### 1.3 Emotional Arc and Dynamics

Think of a song as a journey, not a flat road.

ENERGY MAPPING (rough idea, not prescription):
  Intro: 2-3  |  Verse: 5-6  |  Pre-Chorus: 7
  Chorus: 8-9  |  Bridge: varies  |  Final Chorus: 9-10

The most powerful dynamic trick: CONTRAST.
- Whisper before a scream hits harder than just screaming
- Sparse before dense. Slow before fast. Low before high.
- The drop only works because of the buildup
- Silence is an instrument

"Whisper to roar to whisper" — start intimate, build to full power,
strip back to vulnerability. Works for ballads, epics, anthems.

### 1.4 Writing Lyrics That Work

SHOW, DON'T TELL (usually):
- "I was sad" = flat
- "Your hoodie's still on the hook by the door" = alive
- But sometimes "I give my life" said plainly IS the power

THE HOOK:
- The line people remember, hum, repeat
- Usually the title or core phrase
- Works best when melody + lyric + emotion all align
- Place it where it lands hardest (often first/last line of chorus)

PROSODY — lyrics and music supporting each other:
- Stable feelings (resolution, peace) pair with settled melodies,
  perfect rhymes, resolved chords
- Unstable feelings (longing, doubt) pair with wandering melodies,
  near-rhymes, unresolved chords
- Verse melody typically sits lower, chorus goes higher
- But flip this if it serves the song

AVOID (unless you're doing it on purpose):
- Cliches on autopilot ("heart of gold" without earning it)
- Forcing word order to hit a rhyme ("Yoda-speak")
- Same energy in every section (flat dynamics)
- Treating your first draft as sacred — revision is creation

### 1.5 Parody and Adaptation

When rewriting an existing song with new lyrics:

THE SKELETON: Map the original's structure first.
- Count syllables per line
- Mark the rhyme scheme (ABAB, AABB, etc.)
- Identify which syllables are STRESSED
- Note where held/sustained notes fall

FITTING NEW WORDS:
- Match stressed syllables to the same beats as the original
- Total syllable count can flex by 1-2 unstressed syllables
- On long held notes, try to match the VOWEL SOUND of the original
  (if original holds "LOOOVE" with an "oo" vowel, "FOOOD" fits
   better than "LIFE")
- Monosyllabic swaps in key spots keep rhythm intact
  (Crime -> Code, Snake -> Noose)
- Sing your new words over the original — if you stumble, revise

CONCEPT:
- Pick a concept strong enough to sustain the whole song
- Start from the title/hook and build outward
- Generate lots of raw material (puns, phrases, images) FIRST,
  then fit the best ones into the structure
- If you need a specific line somewhere, reverse-engineer the
  rhyme scheme backward to set it up

KEEP SOME ORIGINALS: Leaving a few original lines or structures
intact adds recognizability and lets the audience feel the connection.

### 1.6 Suno AI Prompt Engineering

#### Style/Genre Description Field

FORMULA (adapt as needed):
  Genre + Mood + Era + Instruments + Vocal Style + Production + Dynamics

```
BAD:  "sad rock song"
GOOD: "Cinematic orchestral spy thriller, 1960s Cold War era, smoky
       sultry female vocalist, big band jazz, brass section with
       trumpets and french horns, sweeping strings, minor key,
       vintage analog warmth"
```

DESCRIBE THE JOURNEY, not just the genre:
```
"Begins as a haunting whisper over sparse piano. Gradually layers
 in muted brass. Builds through the chorus with full orchestra.
 Second verse erupts with raw belting intensity. Outro strips back
 to a lone piano and a fragile whisper fading to silence."
```

TIPS:
- V4.5+ supports up to 1,000 chars in Style field — use them
- NO artist names or trademarks. Describe the sound instead.
  "1960s Cold War spy thriller brass" not "James Bond style"
  "90s grunge" not "Nirvana-style"
- Specify BPM and key when you have a preference
- Use Exclude Styles field for what you DON'T want
- Unexpected genre combos can be gold: "bossa nova trap",
  "Appalachian gothic", "chiptune jazz"
- Build a vocal PERSONA, not just a gender:
  "A weathered torch singer with a smoky alto, slight rasp,
   who starts vulnerable and builds to devastating power"

#### Metatags (place in [brackets] inside lyrics field)

STRUCTURE:
  [Intro] [Verse] [Verse 1] [Pre-Chorus] [Chorus]
  [Post-Chorus] [Hook] [Bridge] [Interlude]
  [Instrumental] [Instrumental Break] [Guitar Solo]
  [Breakdown] [Build-up] [Outro] [Silence] [End]

VOCAL PERFORMANCE:
  [Whispered] [Spoken Word] [Belted] [Falsetto] [Powerful]
  [Soulful] [Raspy] [Breathy] [Smooth] [Gritty]
  [Staccato] [Legato] [Vibrato] [Melismatic]
  [Harmonies] [Choir] [Harmonized Chorus]

DYNAMICS:
  [High Energy] [Low Energy] [Building Energy] [Explosive]
  [Emotional Climax] [Gradual swell] [Orchestral swell]
  [Quiet arrangement] [Falling tension] [Slow Down]

GENDER:
  [Female Vocals] [Male Vocals]

ATMOSPHERE:
  [Melancholic] [Euphoric] [Nostalgic] [Aggressive]
  [Dreamy] [Intimate] [Dark Atmosphere]

SFX:
  [Vinyl Crackle] [Rain] [Applause] [Static] [Thunder]

Put tags in BOTH style field AND lyrics for reinforcement.
Keep to 5-8 tags per section max — too many confuses the AI.
Don't contradict yourself ([Calm] + [Aggressive] in same section).

#### Custom Mode
- Always use Custom Mode for serious work (separate Style + Lyrics)
- Lyrics field limit: ~3,000 chars (~40-60 lines)
- Always add structural tags — without them Suno defaults to
  flat verse/chorus/verse with no emotional arc

### 1.7 Phonetic Tricks for AI Singers

AI vocalists don't read — they pronounce. Help them:

PHONETIC RESPELLING:
- Spell words as they SOUND: "through" -> "thru"
- Proper nouns are highest failure rate — test early
- "Nous" -> "Noose" (forces correct pronunciation)
- Hyphenate to guide syllables: "Re-search", "bio-engineering"

DELIVERY CONTROL:
- ALL CAPS = louder, more intense
- Vowel extension: "lo-o-o-ove" = sustained/melisma
- Ellipses: "I... need... you" = dramatic pauses
- Hyphenated stretch: "ne-e-ed" = emotional stretch

ALWAYS:
- Spell out numbers: "24/7" -> "twenty four seven"
- Space acronyms: "AI" -> "A I" or "A-I"
- Test proper nouns/unusual words in a short 30-second clip first
- Once generated, pronunciation is baked in — fix in lyrics BEFORE

### 1.8 Songwriting Workflow

1. Write the concept/hook first — what's the emotional core?
2. If adapting, map the original structure (syllables, rhyme, stress)
3. Generate raw material — brainstorm freely before structuring
4. Draft lyrics into the structure
5. Read/sing aloud — catch stumbles, fix meter
6. Build the Suno style description — paint the dynamic journey
7. Add metatags to lyrics for performance direction
8. Generate 3-5 variations minimum — treat them like recording takes
9. Pick the best, use Extend/Continue to build on promising sections
10. If something great happens by accident, keep it

EXPECT: ~3-5 generations per 1 good result. Revision is normal.
Style can drift in extensions — restate genre/mood when extending.

### 1.9 Lessons Learned

- Describing the dynamic ARC in the style field matters way more
  than just listing genres. "Whisper to roar to whisper" gives
  Suno a performance map.
- Keeping some original lines intact in a parody adds recognizability
  and emotional weight — the audience feels the ghost of the original.
- The bridge slot in a song is where you can transform imagery.
  Swap the original's specific references for your theme's metaphors
  while keeping the emotional function (reflection, shift, revelation).
- Monosyllabic word swaps in hooks/tags are the cleanest way to
  maintain rhythm while changing meaning.
- A strong vocal persona description in the style field makes a
  bigger difference than any single metatag.
- Don't be precious about rules. If a line breaks meter but hits
  harder, keep it. The feeling is what matters. Craft serves art,
  not the other way around.

---

## Part 2: HeartMuLa — Local Open-Source Music Generation

HeartMuLa is a family of open-source music foundation models (Apache-2.0) that generates music conditioned on lyrics and tags, with multilingual support. Comparable to Suno for open-source use. Includes:
- **HeartMuLa** — Music language model (3B/7B) for generation from lyrics + tags
- **HeartCodec** — 12.5Hz music codec for high-fidelity audio reconstruction
- **HeartTranscriptor** — Whisper-based lyrics transcription
- **HeartCLAP** — Audio-text alignment model

Links: [Repo](https://github.com/HeartMuLa/heartlib) | [Models](https://huggingface.co/HeartMuLa) | [Paper](https://arxiv.org/abs/2601.10547) | License: Apache-2.0

### 2.1 Hardware Requirements

- **Minimum**: 8GB VRAM with `--lazy_load true` (loads/unloads models sequentially)
- **Recommended**: 16GB+ VRAM for comfortable single-GPU usage
- **Multi-GPU**: Use `--mula_device cuda:0 --codec_device cuda:1` to split across GPUs
- 3B model with lazy_load peaks at ~6.2GB VRAM
- **No GPU?** Run on CPU with `--mula_device cpu --codec_device cpu`, but expect 30-60+ min per song. Consider cloud GPU (Google Colab T4, Lambda Labs) or the [online demo](https://heartmula.github.io/).

### 2.2 Installation

```bash
# 1. Clone
git clone https://github.com/HeartMuLa/heartlib.git
cd heartlib

# 2. Virtual environment (Python 3.10 required)
uv venv --python 3.10 .venv
. .venv/bin/activate
uv pip install -e .

# 3. Fix dependency conflicts (as of Feb 2026)
uv pip install --upgrade datasets transformers
```

### 2.3 Source Code Patches (Required for transformers 5.x)

**Patch 1 — RoPE cache fix** in `src/heartlib/heartmula/modeling_heartmula.py`:

In the `setup_caches` method of the `HeartMuLa` class, add after the `reset_caches` try/except block and before `with device:`:

```python
# Re-initialize RoPE caches that were skipped during meta-device loading
from torchtune.models.llama3_1._position_embeddings import Llama3ScaledRoPE
for module in self.modules():
    if isinstance(module, Llama3ScaledRoPE) and not module.is_cache_built:
        module.rope_init()
        module.to(device)
```

**Why**: `from_pretrained` creates model on meta device first; `Llama3ScaledRoPE.rope_init()` skips cache building on meta tensors, then never rebuilds after weights are loaded to real device.

**Patch 2 — HeartCodec loading fix** in `src/heartlib/pipelines/music_generation.py`:

Add `ignore_mismatched_sizes=True` to ALL `HeartCodec.from_pretrained()` calls (there are 2).

**Why**: VQ codebook `initted` buffers have shape `[1]` in checkpoint vs `[]` in model. Same data, just scalar vs 0-d tensor. Safe to ignore.

### 2.4 Download Model Checkpoints

```bash
cd heartlib  # project root
# All 3 can be downloaded in parallel (total: several GB)
hf download --local-dir './ckpt' 'HeartMuLa/HeartMuLaGen'
hf download --local-dir './ckpt/HeartMuLa-oss-3B' 'HeartMuLa/HeartMuLa-oss-3B-happy-new-year'
hf download --local-dir './ckpt/HeartCodec-oss' 'HeartMuLa/HeartCodec-oss-20260123'
```

### 2.5 Generating Music

```bash
cd heartlib
. .venv/bin/activate
python ./examples/run_music_generation.py \
  --model_path=./ckpt \
  --version="3B" \
  --lyrics="./assets/lyrics.txt" \
  --tags="./assets/tags.txt" \
  --save_path="./assets/output.mp3" \
  --lazy_load true
```

**Tags** (comma-separated, no spaces):
```
piano,happy,wedding,synthesizer,romantic
```

**Lyrics** (bracketed structural tags):
```
[Intro]

[Verse]
Your lyrics here...

[Chorus]
Chorus lyrics...

[Bridge]
Bridge lyrics...

[Outro]
```

### 2.6 Key Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--max_audio_length_ms` | 240000 | Max length in ms (240s = 4 min) |
| `--topk` | 50 | Top-k sampling |
| `--temperature` | 1.0 | Sampling temperature |
| `--cfg_scale` | 1.5 | Classifier-free guidance scale |
| `--lazy_load` | false | Load/unload models on demand (saves VRAM) |
| `--mula_dtype` | bfloat16 | Dtype for HeartMuLa (bf16 recommended) |
| `--codec_dtype` | float32 | Dtype for HeartCodec (fp32 recommended for quality) |

Performance: RTF ≈ 1.0 — a 4-minute song takes ~4 minutes to generate. Output: MP3, 48kHz stereo, 128kbps.

### 2.7 HeartMuLa Pitfalls

1. **Do NOT use bf16 for HeartCodec** — degrades audio quality. Use fp32 (default).
2. **Tags may be ignored** — known issue (#90). Lyrics tend to dominate; experiment with tag ordering.
3. **Triton not available on macOS** — Linux/CUDA only for GPU acceleration.
4. **RTX 5080 incompatibility** reported in upstream issues.
5. Dependency pin conflicts require the manual upgrades and patches described above.
6. `torchtune` may report version `0.4.0+cpu` — this is just package metadata; it still uses CUDA via PyTorch. Look for "CUDA memory" lines in output to confirm GPU use.

---

## Part 3: Audio Analysis & Spectrograms (songsee)

Generate spectrograms and multi-panel audio feature visualizations from audio files using the songsee Go CLI.

Homepage: https://github.com/steipete/songsee

### 3.1 Installation

```bash
# Requires Go: https://go.dev/doc/install
go install github.com/steipete/songsee/cmd/songsee@latest
```

Optional: `ffmpeg` for formats beyond WAV/MP3.

### 3.2 Quick Start

```bash
# Basic spectrogram
songsee track.mp3

# Save to specific file
songsee track.mp3 -o spectrogram.png

# Multi-panel visualization grid
songsee track.mp3 --viz spectrogram,mel,chroma,hpss,selfsim,loudness,tempogram,mfcc,flux

# Time slice (start at 12.5s, 8s duration)
songsee track.mp3 --start 12.5 --duration 8 -o slice.jpg

# From stdin
cat track.mp3 | songsee - --format png -o out.png
```

### 3.3 Visualization Types

Use `--viz` with comma-separated values. Multiple types render as a grid in a single image.

| Type | Description |
|------|-------------|
| `spectrogram` | Standard frequency spectrogram |
| `mel` | Mel-scaled spectrogram |
| `chroma` | Pitch class distribution |
| `hpss` | Harmonic/percussive separation |
| `selfsim` | Self-similarity matrix |
| `loudness` | Loudness over time |
| `tempogram` | Tempo estimation |
| `mfcc` | Mel-frequency cepstral coefficients |
| `flux` | Spectral flux (onset detection) |

### 3.4 Common Flags

| Flag | Description |
|------|-------------|
| `--viz` | Visualization types (comma-separated) |
| `--style` | Color palette: `classic`, `magma`, `inferno`, `viridis`, `gray` |
| `--width` / `--height` | Output image dimensions |
| `--window` / `--hop` | FFT window and hop size |
| `--min-freq` / `--max-freq` | Frequency range filter |
| `--start` / `--duration` | Time slice of the audio |
| `--format` | Output format: `jpg` or `png` |
| `-o` | Output file path |

---

## Part 4: AudioCraft — Meta's Text-to-Music / Text-to-Sound

> *Previously a separate `audiocraft-audio-generation` skill — consolidated here because both tools generate music/audio and users pick based on use-case, not provider.*

Meta's AudioCraft library: **MusicGen** (text-to-music, melody conditioning), **AudioGen** (text-to-sound effects), **EnCodec** (neural audio codec). Use AudioCraft when you need pure text-description-to-audio without lyrics structure, or need environment/sound-effect generation.

| When | Tool |
|------|------|
| Text description → music (no lyrics needed) | AudioCraft/MusicGen |
| Sound effects / environmental audio | AudioCraft/AudioGen |
| Song with lyrics, AI vocalist | Suno AI / HeartMuLa (Parts 1–2) |

### Installation

```bash
pip install audiocraft                          # PyPI
pip install git+https://github.com/facebookresearch/audiocraft.git  # latest
pip install transformers torch torchaudio       # HuggingFace Transformers alternative
```

### Quick start — MusicGen (text-to-music)

```python
from audiocraft.models import MusicGen
import audiocraft.data.audio as audio_utils

model = MusicGen.get_pretrained('facebook/musicgen-small')  # or -medium, -large
model.set_generation_params(duration=8)  # seconds

descriptions = ['happy rock music with guitar', 'ambient electronic chill']
wav = model.generate(descriptions)  # shape: [B, C, T]

for i, wav_out in enumerate(wav):
    audio_utils.audio_write(f'output_{i}', wav_out.cpu(), model.sample_rate, strategy='loudness')
```

### Quick start — AudioGen (text-to-sound effects)

```python
from audiocraft.models import AudioGen

model = AudioGen.get_pretrained('facebook/audiogen-medium')
model.set_generation_params(duration=5)

descriptions = ['dog barking in the rain', 'thunder with light wind']
wav = model.generate(descriptions)
```

### Model sizes

| Model | VRAM | Notes |
|-------|------|-------|
| `musicgen-small` (300M) | 2–4GB | Fast, reasonable quality |
| `musicgen-medium` (1.5B) | 6–8GB | Good balance |
| `musicgen-large` (3.3B) | 12–16GB | Best quality |
| `musicgen-stereo-*` | +50% | Stereo output variants |

### HuggingFace Transformers alternative (no audiocraft package)

```python
from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy.io.wavfile as wavfile
import numpy as np

processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")

inputs = processor(text=["80s pop track with bassy synths"], return_tensors="pt", padding=True)
audio_values = model.generate(**inputs, max_new_tokens=256)
wavfile.write("output.wav", rate=model.config.audio_encoder.sampling_rate, data=audio_values[0, 0].numpy())
```

### Key generation parameters

| Parameter | Description | Typical |
|-----------|-------------|---------|
| `duration` | Length in seconds | 5–30 |
| `temperature` | Sampling temperature | 1.0 |
| `top_k` | Top-k sampling | 250 |
| `top_p` | Nucleus sampling | 0.0 (off) |
| `cfg_coef` | Classifier-free guidance | 3.0 |

### See also

- `references/audiocraft-advanced.md` — melody conditioning, style transfer, batching, streaming
- `references/audiocraft-troubleshooting.md` — CUDA OOM, audio artifact fixes, common errors

