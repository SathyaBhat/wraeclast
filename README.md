### Wraeclast

Wraeclast is my homeserver powered by ArchLinux. This repo is a monorepo of various applications that are running on the homeserver using Docker. Every application gets a sub-directory under the `apps/` directory. The repo is integrated with dokploy running on the same server. Whenever a change is made to the repo, dokploy will automatically deploy the changes to the server.

### Apps

- `actualbudget` - Actual Budget, personal finance tracker
- `amex-sync` - Amex transaction sync backend
- `beszel-agent` / `beszel-hub` - Beszel server monitoring
- `dawarich` - Dawarich, location history tracker
- `emini-poster` - Hourly Home Assistant battery + weather picture for the NOTE4C e-paper
- `firecrawl` - Firecrawl self-hosted scraping API
- `grafana` - Grafana dashboards
- `hermes` - Hermes agent gateway
- `influxdb` - InfluxDB
- `miniflux` - Miniflux RSS reader
- `restaurants` - Restaurants datasette + submission form
- `searxng` - Private SearXNG metasearch service
- `silverbullet` - SilverBullet notes
- `tandoor` - Tandoor recipe manager
