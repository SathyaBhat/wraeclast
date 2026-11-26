---
name: research-discovery
description: "Research content discovery umbrella: arXiv papers (API, Semantic Scholar, BibTeX), and RSS/blog feed monitoring via blogwatcher-cli."
version: 1.0.0
author: Hermes Agent (curator)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Research, Arxiv, Papers, Academic, RSS, Blogs, Feed-Reader, Monitoring, Semantic-Scholar, BibTeX]
    related_skills: [llm-wiki, research-paper-writing]
    homepage_blogwatcher: https://github.com/JulienTant/blogwatcher-cli
prerequisites:
  commands: [curl, jq, python3]
---

# Research Discovery

Two complementary research-discovery workflows:

| Tool | Best for |
|------|----------|
| **arXiv + Semantic Scholar** | Find, read, cite academic papers |
| **blogwatcher-cli** | Monitor blogs and RSS/Atom feeds for new posts |

---

## Section 1 — arXiv + Semantic Scholar

Search and retrieve academic papers from arXiv via their free REST API. No API key needed.

### Quick reference

| Action | Command |
|--------|---------|
| Search papers | `curl "https://export.arxiv.org/api/query?search_query=all:QUERY&max_results=5"` |
| Get specific paper | `curl "https://export.arxiv.org/api/query?id_list=2402.03300"` |
| Read abstract (web) | `web_extract(urls=["https://arxiv.org/abs/2402.03300"])` |
| Read full paper (PDF) | `web_extract(urls=["https://arxiv.org/pdf/2402.03300"])` |
| Helper script | `python scripts/search_arxiv.py "QUERY"` |

### Clean output (parse XML)

```bash
curl -s "https://export.arxiv.org/api/query?search_query=all:GRPO+reinforcement+learning&max_results=5&sortBy=submittedDate&sortOrder=descending" | python3 -c "
import sys, xml.etree.ElementTree as ET
ns = {'a': 'http://www.w3.org/2005/Atom'}
root = ET.parse(sys.stdin).getroot()
for i, entry in enumerate(root.findall('a:entry', ns)):
    title = entry.find('a:title', ns).text.strip().replace('\n', ' ')
    arxiv_id = entry.find('a:id', ns).text.strip().split('/abs/')[-1]
    published = entry.find('a:published', ns).text[:10]
    authors = ', '.join(a.find('a:name', ns).text for a in entry.findall('a:author', ns))
    summary = entry.find('a:summary', ns).text.strip()[:200]
    cats = ', '.join(c.get('term') for c in entry.findall('a:category', ns))
    print(f'{i+1}. [{arxiv_id}] {title}')
    print(f'   Authors: {authors}')
    print(f'   Published: {published} | Categories: {cats}')
    print(f'   Abstract: {summary}...')
    print(f'   PDF: https://arxiv.org/pdf/{arxiv_id}')
    print()
"
```

### Search query syntax

| Prefix | Searches | Example |
|--------|----------|---------|
| `all:` | All fields | `all:transformer+attention` |
| `ti:` | Title | `ti:large+language+models` |
| `au:` | Author | `au:vaswani` |
| `abs:` | Abstract | `abs:reinforcement+learning` |
| `cat:` | Category | `cat:cs.AI` |
| `co:` | Comment | `co:accepted+NeurIPS` |

Boolean: `AND` (default `+`), `OR`, `ANDNOT`, `"exact phrase"`.

### Sort and pagination

```bash
# Latest in cs.AI
curl -s "https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=10"
```

Parameters: `sortBy` = `relevance|lastUpdatedDate|submittedDate`, `sortOrder` = `ascending|descending`, `start` = offset, `max_results` (default 10, max 30000).

### Semantic Scholar (citations, recommendations)

```bash
# Paper details + citation count
curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:2402.03300?fields=title,authors,citationCount,referenceCount,influentialCitationCount,year,abstract" | python3 -m json.tool

# Who cited this paper
curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:2402.03300/citations?fields=title,authors,year,citationCount&limit=10" | python3 -m json.tool

# References from a paper
curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:2402.03300/references?fields=title,authors,year,citationCount&limit=10" | python3 -m json.tool

# Related-paper recommendations
curl -s -X POST "https://api.semanticscholar.org/recommendations/v1/papers/" \
  -H "Content-Type: application/json" \
  -d '{"positivePaperIds": ["arXiv:2402.03300"], "negativePaperIds": []}' | python3 -m json.tool

# Author profile
curl -s "https://api.semanticscholar.org/graph/v1/author/search?query=Yann+LeCun&fields=name,hIndex,citationCount,paperCount" | python3 -m json.tool
```

Rate limits: arXiv ~1 req/3s (no auth); Semantic Scholar 1 req/s (100/s with API key).

### BibTeX generation

```bash
curl -s "https://export.arxiv.org/api/query?id_list=1706.03762" | python3 -c "
import sys, xml.etree.ElementTree as ET
ns = {'a': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}
root = ET.parse(sys.stdin).getroot()
entry = root.find('a:entry', ns)
title = entry.find('a:title', ns).text.strip().replace('\n', ' ')
authors = ' and '.join(a.find('a:name', ns).text for a in entry.findall('a:author', ns))
year = entry.find('a:published', ns).text[:4]
raw_id = entry.find('a:id', ns).text.strip().split('/abs/')[-1]
cat = entry.find('arxiv:primary_category', ns)
primary = cat.get('term') if cat is not None else 'cs.LG'
last_name = entry.find('a:author', ns).find('a:name', ns).text.split()[-1]
print(f'@article{{{last_name}{year}_{raw_id.replace(\".\", \"\")},')
print(f'  title     = {{{title}}},')
print(f'  author    = {{{authors}}},')
print(f'  year      = {{{year}}},')
print(f'  eprint    = {{{raw_id}}},')
print(f'  archivePrefix = {{arXiv}},')
print(f'  primaryClass  = {{{primary}}},')
print(f'  url       = {{https://arxiv.org/abs/{raw_id}}}')
print('}')
"
```

### Common arXiv categories

| Category | Field |
|----------|-------|
| `cs.AI` | Artificial Intelligence |
| `cs.CL` | Computation and Language (NLP) |
| `cs.CV` | Computer Vision |
| `cs.LG` | Machine Learning |
| `stat.ML` | Machine Learning (Statistics) |

Full list: https://arxiv.org/category_taxonomy

### Helper script

```bash
python scripts/search_arxiv.py "GRPO reinforcement learning"
python scripts/search_arxiv.py "transformer attention" --max 10 --sort date
python scripts/search_arxiv.py --author "Yann LeCun" --max 5
python scripts/search_arxiv.py --category cs.AI --sort date
python scripts/search_arxiv.py --id 2402.03300
```

No dependencies — Python stdlib only.

### URL patterns

- Abstract: `https://arxiv.org/abs/{id}`
- PDF: `https://arxiv.org/pdf/{id}`
- HTML: `https://arxiv.org/html/{id}`
- Versioned: `https://arxiv.org/abs/1706.03762v7` (stable citation; unversioned resolves to latest)

### Complete research workflow

1. **Discover**: `python scripts/search_arxiv.py "your topic" --sort date --max 10`
2. **Assess impact**: Semantic Scholar citation count
3. **Read abstract**: `web_extract(urls=["https://arxiv.org/abs/ID"])`
4. **Read full paper**: `web_extract(urls=["https://arxiv.org/pdf/ID"])`
5. **Find related work**: Semantic Scholar references/recommendations
6. **Generate BibTeX**: use snippet above

### Notes

- arXiv returns Atom XML — use helper script or parsing snippet
- Withdrawn papers: check `<summary>` for "withdrawn" / "retracted" before treating as valid
- Preserve version suffix in citations to prevent drift

---

## Section 2 — blogwatcher-cli (RSS/Blog Monitoring)

Track blog and RSS/Atom feed updates with `blogwatcher-cli`.

### Installation

Choose one:

```bash
# Go
go install github.com/JulienTant/blogwatcher-cli/cmd/blogwatcher-cli@latest

# Binary (Linux amd64)
curl -sL https://github.com/JulienTant/blogwatcher-cli/releases/latest/download/blogwatcher-cli_linux_amd64.tar.gz | tar xz -C /usr/local/bin blogwatcher-cli

# Docker (persistent storage)
docker run --rm -v blogwatcher-cli:/data -e BLOGWATCHER_DB=/data/blogwatcher-cli.db \
  ghcr.io/julientant/blogwatcher-cli scan
```

All releases: https://github.com/JulienTant/blogwatcher-cli/releases

### Managing blogs

```bash
blogwatcher-cli add "My Blog" https://example.com
blogwatcher-cli add "My Blog" https://example.com --feed-url https://example.com/feed.xml
blogwatcher-cli add "My Blog" https://example.com --scrape-selector "article h2 a"
blogwatcher-cli blogs           # list tracked
blogwatcher-cli remove "My Blog" --yes
blogwatcher-cli import subscriptions.opml  # bulk import from Feedly/Inoreader
```

### Scanning and reading

```bash
blogwatcher-cli scan                         # scan all
blogwatcher-cli scan "My Blog"               # scan one
blogwatcher-cli articles                     # list unread
blogwatcher-cli articles --all               # list all
blogwatcher-cli articles --blog "My Blog"
blogwatcher-cli articles --category "Engineering"
blogwatcher-cli read 1                       # mark read by ID
blogwatcher-cli read-all                     # mark all read
blogwatcher-cli read-all --blog "My Blog" --yes
```

### Environment variables

| Variable | Description |
|----------|-------------|
| `BLOGWATCHER_DB` | Path to SQLite database (default `~/.blogwatcher-cli/blogwatcher-cli.db`) |
| `BLOGWATCHER_WORKERS` | Concurrent scan workers (default 8) |
| `BLOGWATCHER_SILENT` | Only output "scan done" |
| `BLOGWATCHER_YES` | Skip confirmations |
| `BLOGWATCHER_CATEGORY` | Default article filter category |

### Notes

- Auto-discovers RSS/Atom feeds from blog homepages when no `--feed-url` given
- Falls back to HTML scraping when `--scrape-selector` is configured
- Import OPML files from Feedly, Inoreader, NewsBlur, etc.
- Database at `~/.blogwatcher-cli/blogwatcher-cli.db` — override with `--db` or `BLOGWATCHER_DB`
- Migrating from `Hyaxia/blogwatcher`: `mv ~/.blogwatcher/blogwatcher.db ~/.blogwatcher-cli/blogwatcher-cli.db`

---

## Scripts

- `scripts/search_arxiv.py` — standalone arXiv search + clean output (no dependencies)
