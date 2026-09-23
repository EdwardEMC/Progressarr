# Getting Started

This guide covers installing Progressarr using Docker and connecting it to an existing self-hosted media stack.

Progressarr is designed to sit alongside services such as Radarr, Sonarr, Seerr, Jellyfin, and SABnzbd.

---

## Prerequisites

Before installing Progressarr, make sure you have:

- Docker
- Docker Compose
- A running Radarr instance
- A running Sonarr instance
- A running Seerr instance

Jellyfin is required for the initial setup flow and user authentication.

Progressarr is designed primarily for self-hosted environments.

---

## 1. Create the Progressarr Data Directory

Progressarr stores its application data in `/app/data` inside the container.

Create a persistent directory on the Docker host:

```bash
mkdir -p ../progressarr/data
```

You can choose any suitable location for the host directory.

The important part is that it is mounted to:

```text
/app/data
```

inside the container.

---

## 2. Add Progressarr to Docker Compose

Add the following service to your existing media-stack `docker-compose.yml`:

```yaml
progressarr:
  image: ghcr.io/edwardemc/progressarr:latest
  container_name: progressarr
  ports:
    - ${VM_IP}:8181:8000
  volumes:
    - ../progressarr/data:/app/data
  networks:
    - media
  restart: unless-stopped
```

The example assumes your existing stack has a Docker network named `media`.

If your network has a different name, replace `media` with the appropriate network.

---

## 3. Start Progressarr

Start the container:

```bash
docker compose up -d progressarr
```

Check that it is running:

```bash
docker compose ps
```

You should see the Progressarr container running.

To view its logs:

```bash
docker compose logs -f progressarr
```

---

## 4. Open Progressarr

Open Progressarr in your browser using the host and port you configured.

For example:

```text
http://192.168.0.10:8181
```

The exact address depends on your Docker host and Compose configuration.

You should be presented with the Progressarr setup screen.

---

# Initial Setup

The first-time setup process establishes the initial Progressarr configuration.

The setup screen:

1. Connects Progressarr to your Jellyfin server.
2. Creates the default administrator account.

Complete the setup before attempting to use the main application.

If Progressarr needs to be reconfigured later, the setup/recovery paths can be used.

---

# Jellyfin Configuration

The initial setup requires a connection to Jellyfin.

If Jellyfin and Progressarr are running on the same Docker network, use the Docker service name rather than the host IP.

For example:

```text
http://jellyfin:8096
```

Avoid using:

```text
http://192.168.0.1:8096
```

when both containers can communicate directly over a shared Docker network.

Docker's internal DNS will resolve the `jellyfin` service name to the appropriate container.

---

# Docker Networking

Progressarr needs to be able to communicate with the services it integrates with.

When the services are part of the same Docker Compose stack, the simplest approach is to place them on a shared network.

For example:

```yaml
networks:
  media:
```

Then attach the relevant services:

```yaml
services:
  progressarr:
    ...
    networks:
      - media

  radarr:
    ...
    networks:
      - media

  sonarr:
    ...
    networks:
      - media

  jellyfin:
    ...
    networks:
      - media

  seerr:
    ...
    networks:
      - media
```

Once they share a network, Progressarr can communicate with them using their service names.

---

# Service URLs

Typical Docker service URLs are:

| Service | Example URL |
|---|---|
| Radarr | `http://radarr:7878` |
| Sonarr | `http://sonarr:8989` |
| Jellyfin | `http://jellyfin:8096` |
| Seerr | `http://seerr:8989` |

The exact service names and ports depend on your Docker Compose configuration.

---

# Configure Radarr, Sonarr and Seerr

After completing the initial setup, open:

**Settings**

Configure the services used by your media stack.

Currently supported service configuration includes:

- Radarr
- Sonarr
- Seerr
- Jellyfin

You will need the appropriate service URL and API key where required.

---

# Authentication

Progressarr provides application-level authentication using sessions.

Users can log in using their existing Jellyfin account credentials.

Administrators can additionally log in using the default administrator account created during setup.

Progressarr uses an HTTP cookie to maintain the authenticated session.

Protected API endpoints require a valid Progressarr session.

---

# User-Scoped Data

Progressarr associates requests and related download/history information with users.

Standard users only see information associated with their requests.

Administrators can see all downloads and historical data.

This allows Progressarr to provide a shared dashboard while keeping user activity scoped appropriately.

---

# Environment Configuration

Progressarr can bootstrap service configuration from environment variables.

An example configuration is:

```env
RADARR_URL=http://radarr:7878
RADARR_API_KEY=your-radarr-api-key

SONARR_URL=http://sonarr:8989
SONARR_API_KEY=your-sonarr-api-key

SEERR_URL=http://seerr:8989
SEERR_API_KEY=your-seerr-api-key

JELLYFIN_URL=http://jellyfin:8096
JELLYFIN_API_KEY=your-jellyfin-api-key

SESSION_SECRET=your-secret-session-key
```

Environment configuration is primarily used for initial application configuration.

Once configuration has been stored in the Progressarr database, existing database configuration may take precedence over newly supplied environment values.

After changing environment variables, restart the application:

```bash
docker compose restart progressarr
```

---

# Updating Progressarr

Progressarr is distributed through the GitHub Container Registry.

To pull the latest image:

```bash
docker compose pull progressarr
```

Then recreate the container:

```bash
docker compose up -d progressarr
```

If your Compose configuration uses `latest`, this will update the container to the current published image.

Your persistent `/app/data` volume should remain unchanged when the container is recreated.

---

# Troubleshooting

## Progressarr cannot connect to Radarr or Sonarr

Check that the containers are running:

```bash
docker compose ps
```

Check the Docker networks:

```bash
docker network ls
```

Make sure Progressarr and the relevant service share a Docker network.

If they do, use the Docker service name:

```text
http://radarr:7878
```

rather than the host's IP address.

---

## API returns `401 Unauthorized`

A `401` response generally means that the request is not authenticated or a configured service API key is invalid.

Check:

1. Your Progressarr session is valid.
2. The relevant service is reachable.
3. The configured API key is correct.
4. The configured service URL is correct.

---

## Configuration changes are not appearing

Progressarr bootstraps configuration during startup.

Restart the container:

```bash
docker compose restart progressarr
```

If configuration already exists in the Progressarr database, the stored configuration may take precedence over environment variables.

---

## Progressarr will not start after a database/model change

During development, database models may change in ways that are incompatible with an existing development database.

If the database can safely be recreated:

```bash
docker compose down -v
docker compose up -d
```

**Warning:** `docker compose down -v` removes Docker volumes and can permanently delete stored application data.

Do not use this command against a production database unless you intentionally want to destroy the stored data.

---

# Reverse Proxy

Progressarr is compatible with standard HTTP reverse-proxy deployments.

If exposing Progressarr outside your local network:

- Use HTTPS.
- Use a suitable reverse proxy.
- Restrict access where appropriate.
- Do not expose API keys or `.env` files.
- Use strong authentication credentials.

---

# Security

Progressarr is intended primarily for trusted/self-hosted environments.

Treat API keys for Radarr, Sonarr, Jellyfin, and other integrated services as secrets.

Do not commit credentials to source control.

If Progressarr is accessible outside your trusted network, use HTTPS and an appropriate access-control strategy such as a VPN or authenticated reverse proxy.

---

# Next Steps

Once Progressarr is configured:

1. Confirm Radarr and Sonarr are connected.
2. Confirm Seerr is connected.
3. Confirm Jellyfin authentication works.
4. Open the dashboard.
5. Review active downloads.
6. Review recent history.
7. Try searching and filtering the download/history data.

For development information, see the main project README.
