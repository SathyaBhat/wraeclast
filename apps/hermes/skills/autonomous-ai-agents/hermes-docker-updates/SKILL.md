---
name: hermes-docker-updates
description: "Use when updating Hermes on Wraeclast. Pin image and push."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, docker, compose, wraeclast, deployment, updates]
    related_skills: [hermes-agent]
---

# Hermes Docker Updates on Wraeclast

The deployed Hermes Compose definition is `/opt/data/wraeclast/apps/hermes/docker-compose.yml`. The `hermes` service pins its image under `image:`.

## Procedure

1. Confirm the requested tag exists in Docker Hub before editing.
2. Change only `services.hermes.image` in the Compose file; retain all service configuration, mounted volumes, network, and Traefik labels.
3. Commit only that file in `/opt/data/wraeclast` using `chore: update Hermes image to <tag>`.
4. Push `main` with the dedicated deployment key:
   ```bash
   GIT_SSH_COMMAND='ssh -i /opt/data/.ssh/id_ed25519_wraeclast_deploy -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new' git push origin main
   ```
5. If local uncommitted work prevents rebasing after the remote advances, do not stash or alter it. Create a temporary detached worktree at `origin/main`, cherry-pick the Hermes commit there, push from that worktree, and remove it afterward.
6. Check the remote head with `git ls-remote --heads origin main`. Pushing `main` auto-deploys the Compose app (user-confirmed), so no manual redeploy is needed; the container restart ends the current session. Once the user says it is deployed, verify with `/opt/hermes/.venv/bin/python -c "import hermes_cli; print(hermes_cli.__version__)"` (the `hermes` CLI is not on PATH).
7. Docker Hub tags use semver (`v0.23.0`; `-desktop` variants exist). Check a tag via `https://hub.docker.com/v2/repositories/nousresearch/hermes-agent/tags/<tag>`.

## Safety

- Treat unrelated dirty files in the Wraeclast checkout as someone else's work.
- Never change the persistent volume, `/home/sathyabhat/obsidian` mount, `/home/sathyabhat/code/wraeclast` mount, network, ports, or Traefik labels while performing an image-only update.
