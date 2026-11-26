---
name: media
description: "Media umbrella: audio/music creation, YouTube transcripts, GIF retrieval — route to the right skill."
version: 1.0.0
author: Hermes Agent (curator)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [media, audio, music, youtube, transcripts, gif, tenor, suno, songwriting, visualization]
    related_skills: [audio-and-music, media-retrieval]
---

# Media Umbrella

Two sibling skills cover the media domain — creating audio/music and retrieving/processing media content. Load this umbrella to orient; load the specific skill for execution.

## Skill Map

| Skill | Load when… |
|---|---|
| **audio-and-music** | Write songs, generate music with Suno AI or HeartMuLa, create audio visualizations, work with audio craft (chord progressions, lyrics, structure) |
| **media-retrieval** | Extract and process YouTube video transcripts (→ summaries, threads, blog posts), or search and download GIFs via Tenor API |

## Routing Guide

**"Write / generate / produce a song or music"** → **audio-and-music**

**"Make an audio visualizer"** → **audio-and-music**

**"Summarise this YouTube video"** → **media-retrieval**

**"Turn this YouTube video into a Twitter thread / blog post"** → **media-retrieval**

**"Find me a GIF of X"** → **media-retrieval**

**"Make ASCII art from a video"** → NOT this umbrella → load **ascii-video** (under **creative-coding**)

**"Animate something to music"** → **audio-and-music** (for the music), then **manim-video** or **p5js** (for the animation)

## Pitfalls

- **YouTube transcripts availability** — auto-generated captions may be missing for music videos, live streams with disabled captions, or short clips; check early
- **Suno AI vs HeartMuLa** — Suno is the cloud API (requires account); HeartMuLa runs locally via Python; `audio-and-music` covers both
- **GIF Tenor API** — requires `TENOR_API_KEY` in `${HERMES_HOME:-~/.hermes}/.env`; get a free key at https://developers.google.com/tenor/guides/quickstart
