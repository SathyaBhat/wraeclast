# SearXNG

Private metasearch service routed at `https://wraeclast.bishop-bass.ts.net/searxng/` through the tailnet-protected Traefik hostname. It must not be registered against a public Internet domain without adding request limiting and explicit client authentication.

## Deployment hand-off

1. Create the **SearXNG** Compose application in Dokploy, using `apps/searxng/docker-compose.yml` from this repository. A new app directory is not necessarily auto-registered by Dokploy.
2. Copy `.env.example` to the app's `.env`, or define the listed values in the Dokploy UI. Generate `SEARXNG_SECRET` once with `openssl rand -hex 32`; do not commit it.
3. Deploy and wait for `searxng` to become healthy.
4. Verify the UI: `curl --fail --location https://wraeclast.bishop-bass.ts.net/searxng/`
5. Verify the trusted JSON endpoint: `curl --fail --get --data-urlencode 'q=SearXNG' --data-urlencode 'format=json' https://wraeclast.bishop-bass.ts.net/searxng/search`

The `searxng` service alone joins `dokploy-network`; Valkey stays on the private `searxng` network. Persistent named volumes retain the SearXNG cache and Valkey data across container replacement.
