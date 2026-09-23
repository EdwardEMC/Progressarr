# Progressarr

**Progressarr** is a lightweight, self-hosted dashboard for monitoring and managing media downloads across the *Arr ecosystem.

It provides a unified interface for viewing download activity, history, and media-processing information from services such as **Radarr**, **Sonarr**, **SABnzbd**, **Sonarr**, **Seerr**, and **Jellyfin**.

The application is designed to complement existing media automation tools rather than replace them.

---

## Initial Setup

Add the Progressarr container to your existing `docker-compose.yml` or Docker stack. The following is an example configuration:

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

### First-Time Setup

When you first access Progressarr, you will be presented with the setup screen. This setup process:

1. Connects Progressarr to your Jellyfin server.
2. Creates the default administrator account.

The setup screen is also available through the recovery/setup paths if Progressarr needs to be reconfigured.

Once setup is complete, navigate to **Settings** and configure your Radarr, Sonarr, and Seerr connections.

### Authentication

Setup is now complete.

Users can log in to Progressarr using their existing **Jellyfin account credentials**. Administrators can additionally log in using either their Jellyfin account or the **default administrator account** created during setup.

### Docker Networking

If Progressarr is running on a shared Docker network (such as the `media` network in the example above), services should be configured using their **Docker service/container name** rather than the host's IP address.

For example, instead of:

```text
http://192.168.0.1:8096
```

use:

```text
http://jellyfin:8096
```

This allows Docker's internal DNS to resolve the `jellyfin` container directly over the shared network.

**Setup is now complete.**

---

## Features

### Dashboard

Progressarr provides a central dashboard for monitoring media activity across your services.

Current functionality includes:

* Download overview
* Download history
* Sonarr history
* Radarr history
* User scoped requests
* Download status information
* Media/service metadata
* Search
* Advanced filtering
* Sorting
* Date/time filtering
* Authentication
* Settings management
* Logout
* Service configuration
* Responsive UI

### Download Filtering

The download interface supports filtering across a number of download attributes.

The filtering UI is designed to keep the dashboard clean by initially displaying the primary search control while allowing additional filters to be expanded when required.

Filters can be combined to narrow large download/history datasets.

Filtering and query processing are implemented with performance in mind so that expensive filtering operations are avoided where possible.

### History

Progressarr can process historical activity from:

* Sonarr
* Radarr

History information can be used to understand what happened to downloads after they were grabbed, including processing and import activity.

### Authentication

Progressarr includes application-level authentication with:

* Session-based authentication
* Admin sessions
* User sessions
* Secure session cookies
* Protected API endpoints
* Login/logout functionality

Unauthenticated requests to protected endpoints are rejected.

### Service Configuration

Service configuration is stored centrally and can be bootstrapped from environment configuration.

Currently supported service configuration includes:

* Radarr
* Sonarr
* Seerr
* Jellyfin

The architecture is designed so additional services can be integrated without tightly coupling their configuration to the rest of the application.

---

## Screenshots

Screenshots can be added here as the UI continues to evolve.

```text
Coming soon
```

---

## Architecture

Progressarr consists of two primary applications:

```text
┌─────────────────────────────┐
│          Browser            │
│                             │
│       Vue / TypeScript      │
└─────────────┬───────────────┘
              │
              │ HTTP / API
              ▼
┌─────────────────────────────┐
│       FastAPI Backend       │
│                             │
│  ┌───────────────────────┐  │
│  │ Authentication         │  │
│  │ Service Configuration  │  │
│  │ Download Processing    │  │
│  │ History Processing     │  │
│  │ API Routes             │  │
│  └───────────────────────┘  │
└─────────────┬───────────────┘
              │
       ┌──────┼─────────┐──────────┐
       │      │         │          │
       ▼      ▼         ▼          ▼
    Radarr  Sonarr   Jellyfin    Seerr
       │      │
       └──┬───┘
          │
          ▼
       SABnzbd
```

---

## Technology Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* Pydantic Settings
* Uvicorn

### Frontend

* Vue 3
* TypeScript
* Vite
* Tailwind CSS
* Pinia
* Vue Router
* Vue I18n

### Deployment

* Docker
* Docker Compose
* Nginx/reverse proxy compatible

---

## Project Structure

The project is separated into frontend and backend applications.

A simplified structure is:

```text
Progressarr/
│
├── backend/
│   ├── app/
│   │   ├── auth/
│   │   ├── clients/
│   │   ├── routers/
│   │   ├── services/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── db_models.py
│   │   └── main.py
│   │
│   ├── Dockerfile
│   └── ...
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── views/
│   │   ├── router/
│   │   ├── stores/
│   │   └── ...
│   │
│   ├── Dockerfile
│   └── ...
│
├── docker-compose.yml
└── README.md
```

The exact structure may evolve as the project develops.

---

# Getting Started

## Prerequisites

For a Docker-based installation, you will need:

* Docker
* Docker Compose
* A running Radarr instance
* A running Sonarr instance
* A running Seerr instance

Jellyfin is optional.

Progressarr is designed primarily for self-hosted environments.

---

## Docker Installation

Clone the repository:

```bash
git clone <repository-url>
cd Progressarr
```

Create the environment configuration:

```bash
cp .env.example .env
```

Edit `.env` and provide the required configuration.

Then start Progressarr:

```bash
docker compose up -d
```

Check the containers:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs -f
```

Once the containers are running, open the Progressarr web interface in your browser.

---

# Configuration

Progressarr uses environment variables for initial application configuration.

An example configuration looks like:

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

The exact environment variables may change as the configuration system evolves.

### Docker Networking

When Progressarr is deployed alongside the media stack using Docker Compose, services can generally be accessed using their Docker Compose service names.

For example:

```env
RADARR_URL=http://radarr:7878
SONARR_URL=http://sonarr:8989
JELLYFIN_URL=http://jellyfin:8096
```

This avoids relying on container IP addresses, which can change when containers are recreated.

---

# Authentication

Progressarr protects application endpoints using session-based authentication.

The authentication system supports different session types, including:

* Administrator sessions
* Standard user sessions

Authentication is handled by the FastAPI backend and uses an HTTP cookie to maintain the authenticated session.

Protected endpoints require a valid Progressarr session.

If a session is missing or invalid, the API returns:

```text
401 Unauthorized
```

---

# Database

Progressarr currently uses **SQLite** through SQLAlchemy.

The database is initialized when the application starts.

Configuration/bootstrap data can be populated during application startup.

The database stores application-specific information such as service configuration and other Progressarr state.

The external media services remain the source of truth for media and download information.

---

# Service Integration

## Radarr

Progressarr integrates with Radarr to retrieve movie-related information and history.

Radarr provides information about:

* Movies
* Downloads
* History
* Grab events
* Import activity

---

## Sonarr

Progressarr integrates with Sonarr for television-related information.

Sonarr provides information about:

* Series
* Episodes
* Downloads
* History
* Grab events
* Import activity

---

## Seerr

Progressarr integrates with Seerr for user request information.

Seerr provides information about:

* User requested media

---

## Jellyfin

Jellyfin integration provides access to media-server information.

Jellyfin is not intended to replace Jellyfin's primary interface.

Instead, the integration allows Progressarr to provide additional context around media activity.

---

# Download Processing

One of Progressarr's primary responsibilities is turning information from the *Arr applications into a unified download representation.

Downloads can originate from different applications and have different metadata.

Progressarr normalizes this information into a common download model so the frontend can display it consistently.

This allows the dashboard to provide a unified experience instead of requiring users to switch between multiple applications.

The downloads are scoped by user requests, meaning users only see what they have requested. The administrator can see all downloads.

---

# History Processing

History processing is performed separately for Radarr and Sonarr.

The backend processes history entries and associates them with the appropriate download/media information.

The processing pipeline is designed to avoid repeatedly querying external services when the required information can be determined from already available data.

This is particularly important for large history datasets where naïvely processing every record can result in significant delays.

The history is scoped by user requests, meaning users only see what they have requested. The administrator can see all historic data.

---

# Searching, Filtering & Sorting

The dashboard provides a flexible interface for navigating download data.

Users can:

* Search downloads
* Filter results
* Combine multiple filters
* Filter by date/time
* Sort results
* Narrow results based on download metadata

The primary search field is visible by default, while additional filtering controls can be expanded when required.

This keeps the interface clean while still allowing detailed queries.

---

# Frontend

The Progressarr frontend is built using Vue 3 and TypeScript.

The UI uses Tailwind CSS and follows a dark, media-server-inspired visual design.

The frontend is structured around reusable components and API modules.

For example:

```text
components/
├── DownloadCard.vue
└── ...

api/
├── downloads.ts
└── ...

views/
├── Dashboard.vue
└── ...
```

State that needs to be shared across views is handled through Pinia.

Vue Router is used for application navigation.

---

# Development

## Backend

The backend can be run locally using Uvicorn.

From the backend directory:

```bash
python -m uvicorn app.main:app --reload
```

The `--reload` option automatically reloads the application when Python source files change.

---

## Frontend

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend development server is provided by Vite.

---

# Docker Development

The recommended development environment is Docker Compose when working with the complete Progressarr/media stack.

Build the containers:

```bash
docker compose build
```

Start them:

```bash
docker compose up -d
```

Follow logs:

```bash
docker compose logs -f
```

Rebuild a specific service:

```bash
docker compose build backend
docker compose up -d backend
```

Stop the stack:

```bash
docker compose down
```

---

# Troubleshooting

## Container cannot connect to Radarr/Sonarr

First check that the services are running:

```bash
docker compose ps
```

Then check the Docker network:

```bash
docker network ls
```

If Progressarr and the *Arr services are running in different Docker networks, they may not be able to communicate using their service names.

Make sure the relevant containers share a Docker network.

---

## API returns `401 Unauthorized`

A `401` response generally means the request is not authenticated or the configured service API key is invalid.

Check:

1. The Progressarr session is valid.
2. The relevant service is reachable.
3. The configured API key is correct.
4. The service URL is correct.

---

## Configuration changes are not appearing

Progressarr bootstraps configuration during startup.

After changing environment variables, restart the application:

```bash
docker compose restart backend
```

If the application already has configuration stored in the database, existing configuration may take precedence over newly supplied environment variables.

---

## Database schema changes

When database models change during development, the local database may no longer match the current SQLAlchemy models.

For development environments where the database can safely be recreated, the Docker volume can be removed and recreated.

```bash
docker compose down -v
docker compose up -d
```

**Warning:** removing volumes deletes data stored in those volumes.

Do not use this command against a production database unless you intentionally want to destroy the stored data.

---

# Security

Progressarr is intended primarily for trusted/self-hosted environments.

When exposing Progressarr outside the local network:

* Use HTTPS.
* Protect the application behind a suitable reverse proxy where appropriate.
* Do not commit API keys to source control.
* Do not expose `.env` files.
* Use strong authentication credentials.
* Restrict access using your network/VPN infrastructure where possible.

API keys for Radarr, Sonarr, and Jellyfin should be treated as secrets.

---

# Roadmap

Progressarr is actively being developed.

Potential future improvements include:

* Additional *Arr integrations
* Improved download status tracking
* More detailed media statistics
* Enhanced history analysis
* Dashboard statistics
* More advanced filtering
* Improved caching
* Background synchronization
* Improved mobile UI
* More granular user permissions
* Additional authentication options
* Expanded Jellyfin integration
* Improved performance for very large histories

---

# Contributing

Contributions, bug reports, and feature suggestions are welcome.

Before submitting a pull request:

1. Keep changes focused.
2. Follow the existing project structure.
3. Keep backend and frontend responsibilities separated.
4. Avoid introducing unnecessary dependencies.
5. Test changes locally.
6. Update documentation when behaviour changes.

---

# License

License information will be added once the project's licensing terms have been finalized.

---

## About Progressarr

Progressarr is designed to sit alongside an existing self-hosted media stack and provide a single, clean interface for understanding what is happening across the download and media-processing pipeline.

Instead of replacing the tools that already do the heavy lifting, Progressarr brings their information together into one dashboard.

**Radarr → Download → Import → Jellyfin**

**Sonarr → Download → Import → Jellyfin**

Progressarr provides the visibility layer across that workflow.
