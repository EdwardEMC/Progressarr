export interface ServiceSettings {
  url: string | null
  configured: boolean
}

export interface SettingsResponse {
  radarr: ServiceSettings
  sonarr: ServiceSettings
  jellyfin: ServiceSettings
  seerr: ServiceSettings
}

export interface ServiceSettingsUpdate {
  url: string
  api_key?: string
}

export async function getSettings(): Promise<SettingsResponse> {
  const response = await fetch('/api/settings', {
    credentials: 'include',
  })

  if (!response.ok) {
    throw new Error('Unable to load settings.')
  }

  return response.json()
}

export async function updateSettings(settings: {
  radarr?: ServiceSettingsUpdate
  sonarr?: ServiceSettingsUpdate
  jellyfin?: ServiceSettingsUpdate
  seerr?: ServiceSettingsUpdate
}): Promise<SettingsResponse> {
  const response = await fetch('/api/settings', {
    method: 'PUT',

    headers: {
      'Content-Type': 'application/json',
    },

    credentials: 'include',

    body: JSON.stringify(settings),
  })

  if (!response.ok) {
    throw new Error('Unable to save settings.')
  }

  return response.json()
}

export async function testRadarrConnection(
  url: string,
  apiKey: string,
): Promise<{
  success: boolean
  message: string
}> {
  const response = await fetch('/api/settings/radarr/test', {
    method: 'POST',

    headers: {
      'Content-Type': 'application/json',
    },

    credentials: 'include',

    body: JSON.stringify({
      url,
      api_key: apiKey,
    }),
  })

  if (!response.ok) {
    throw new Error('Unable to test Radarr connection.')
  }

  return response.json()
}

export async function testSonarrConnection(
  url: string,
  apiKey: string,
): Promise<{
  success: boolean
  message: string
}> {
  const response = await fetch('/api/settings/sonarr/test', {
    method: 'POST',

    headers: {
      'Content-Type': 'application/json',
    },

    credentials: 'include',

    body: JSON.stringify({
      url,
      api_key: apiKey,
    }),
  })

  if (!response.ok) {
    throw new Error('Unable to test Sonarr connection.')
  }

  return response.json()
}

export async function testJellyfinConnection(
  url: string,
  apiKey: string,
): Promise<{
  success: boolean
  message: string
}> {
  const response = await fetch('/api/settings/jellyfin/test', {
    method: 'POST',

    headers: {
      'Content-Type': 'application/json',
    },

    credentials: 'include',

    body: JSON.stringify({
      url,
      api_key: apiKey,
    }),
  })

  if (!response.ok) {
    throw new Error('Unable to test Jellyfin connection.')
  }

  return response.json()
}

export async function testSeerrConnection(
  url: string,
  apiKey: string,
): Promise<{
  success: boolean
  message: string
}> {
  const response = await fetch('/api/settings/seerr/test', {
    method: 'POST',

    headers: {
      'Content-Type': 'application/json',
    },

    credentials: 'include',

    body: JSON.stringify({
      url,
      api_key: apiKey,
    }),
  })

  if (!response.ok) {
    throw new Error('Unable to test Seerr connection.')
  }

  return response.json()
}
