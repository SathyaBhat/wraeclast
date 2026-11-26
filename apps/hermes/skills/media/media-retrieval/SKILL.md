---
name: media-retrieval
description: "Media retrieval umbrella: YouTube transcripts→summaries/threads/blogs, and GIF search/download from Tenor."
version: 1.0.0
author: Hermes Agent (curator)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [YouTube, Transcripts, Summaries, GIF, Tenor, Media, Retrieval, Content]
    related_skills: [audio-and-music]
prerequisites:
  env_vars: [TENOR_API_KEY]
  commands: [curl, jq]
---

# Media Retrieval

Two complementary media-retrieval workflows: YouTube transcript processing and GIF search.

---

## Section 1 — YouTube Content

Turn YouTube videos into summaries, Twitter/X threads, or blog posts using transcripts.

### When to use
- User pastes a YouTube URL and wants a summary, blog post, or thread
- User asks "what does this video say about X"
- User wants a transcript of a YouTube video

### Workflow

#### 1. Extract the transcript

**Option A — yt-dlp (most reliable):**
```bash
pip install yt-dlp  # or: brew install yt-dlp

# Download transcript/subtitles only
yt-dlp --write-auto-sub --sub-lang en --skip-download \
  "https://www.youtube.com/watch?v=VIDEO_ID"

# Direct transcript extraction
yt-dlp --skip-download --write-auto-sub --sub-format vtt \
  --output "%(title)s.%(ext)s" "VIDEO_URL"
```

**Option B — youtube-transcript-api:**
```bash
pip install youtube-transcript-api
```
```python
from youtube_transcript_api import YouTubeTranscriptApi

transcript = YouTubeTranscriptApi.get_transcript("VIDEO_ID")
text = " ".join(t["text"] for t in transcript)
print(text[:5000])
```

**Option C — web_extract on the YouTube page:**
```
web_extract(["https://www.youtube.com/watch?v=VIDEO_ID"])
```
This captures auto-generated subtitles/description from the page markup when they're available.

#### 2. Process the transcript

**Summary:**
```
Read the transcript. Write a clear, structured summary with:
- Title and key topic
- Main points (3-7 bullets)
- Notable quotes or examples
- Conclusion / key takeaway
```

**Twitter/X thread:**
```
Write a Twitter thread of 8-12 tweets covering the key insights.
Tweet 1: hook with the core insight. Tweet 2-N: one insight per tweet.
Final tweet: CTA or summary. Each tweet ≤ 280 chars. Number each 1/ 2/ etc.
```

**Blog post:**
```
Turn the transcript into a 600-1200 word blog post with:
- Compelling headline
- Intro paragraph (hook the reader)
- 3-5 sections with headers
- Conclusion with takeaway
Use the xurl skill to post the thread if user wants to publish.
```

### Pitfalls

- Auto-generated transcripts have no punctuation — add it during processing
- Some videos have no transcripts (music, live-only, CC disabled) — detect early
- yt-dlp `.vtt` format has markup tags (`<00:00:00.000>`) — strip with regex or convert with `--sub-format txt`
- Long videos (>1h) produce large transcripts; summarize in chunks if needed

---

## Section 2 — GIF Search (Tenor API)

Search and download GIFs via the Tenor API using curl + jq.

### Setup

```bash
# Add to ${HERMES_HOME:-~/.hermes}/.env:
TENOR_API_KEY=your_key_here
```

Get a free API key at https://developers.google.com/tenor/guides/quickstart

### Search for GIFs

```bash
# Get GIF URLs
curl -s "https://tenor.googleapis.com/v2/search?q=thumbs+up&limit=5&key=${TENOR_API_KEY}" \
  | jq -r '.results[].media_formats.gif.url'

# Smaller preview versions
curl -s "https://tenor.googleapis.com/v2/search?q=nice+work&limit=3&key=${TENOR_API_KEY}" \
  | jq -r '.results[].media_formats.tinygif.url'
```

### Download a GIF

```bash
URL=$(curl -s "https://tenor.googleapis.com/v2/search?q=celebration&limit=1&key=${TENOR_API_KEY}" \
  | jq -r '.results[0].media_formats.gif.url')
curl -sL "$URL" -o celebration.gif
```

### Full metadata

```bash
curl -s "https://tenor.googleapis.com/v2/search?q=cat&limit=3&key=${TENOR_API_KEY}" \
  | jq '.results[] | {title: .title, url: .media_formats.gif.url, preview: .media_formats.tinygif.url}'
```

### API parameters

| Parameter | Description |
|-----------|-------------|
| `q` | Search query (URL-encode spaces as `+`) |
| `limit` | Max results (1-50, default 20) |
| `key` | Tenor API key |
| `media_filter` | Filter: `gif`, `tinygif`, `mp4`, `tinymp4`, `webm` |
| `contentfilter` | Safety: `off`, `low`, `medium`, `high` |
| `locale` | Language: `en_US`, `es`, `fr`, etc. |

### Available formats

| Format | Use case |
|--------|----------|
| `gif` | Full quality GIF |
| `tinygif` | Small preview (lighter for chat) |
| `mp4` | Smaller file size video |
| `tinymp4` | Small preview video |
| `webm` | WebM video |
| `nanogif` | Tiny thumbnail |

GIF URLs can be used directly in markdown: `![alt](url)`
