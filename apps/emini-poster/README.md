# emini poster

Every hour, draws a Home Assistant battery charge graph and the weather forecast as a 400 × 300 four-colour picture and sends it to the ZECTRIX NOTE4C's Picture screen. The NOTE4C runs the modified emini Home firmware (the `picture-screen` branch, which adds `POST /api/picture` and drops pairing). Stock emini Home can't receive it.

The device must be in **Open** power mode. In Breath mode its Wi-Fi is off between fetches, and that hour's push is skipped and logged.

## Deployment hand-off

1. Create the **emini-poster** Compose application in Dokploy, using `apps/emini-poster/docker-compose.yml` from this repository. A new app directory is not necessarily auto-registered by Dokploy.
2. Copy `.env.example` to the app's `.env`, or define the listed values in the Dokploy UI. `HA_TOKEN` is a Home Assistant long-lived access token (Profile → Security); do not commit it. `BATTERY_ENTITY` is required.
3. Deploy. The first picture is sent straight away, then a few seconds past every hour.
4. Verify in the logs: `docker logs emini-poster` shows `sent to 192.168.0.49`, and the NOTE4C shows the picture after its ~25-second refresh.
5. To find the battery sensor, or to render without sending: `docker exec emini-poster python /app/ha_poster.py --list` and `docker exec emini-poster python /app/ha_poster.py --once --out /tmp/poster.png`.

The NOTE4C is reached by IP, `192.168.0.49`, which is reserved for it in the router's DHCP. Its `home-ff2e.local` name is mDNS only: neither Tailscale's DNS nor the router's, which the Docker daemon hands to containers, can resolve it. Home Assistant is reached by its tailnet name. The container joins `dokploy-network` like the other apps, but listens on no ports and joins no Traefik route. The healthcheck turns unhealthy when no picture has reached the NOTE4C for two hours.

`home_cli.py` is vendored from emini-home's `tools/`; update both together.
