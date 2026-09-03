export interface Artwork {
  poster_url: string | null
  backdrop_url: string | null
}

export type DownloadStatus =
  | 'downloading'
  | 'import_pending'
  | 'failed'
  | 'completed'
  | 'unknown'

export interface Download {
  id: string
  media_type: string
  service_item_id: number | null

  requested_by_id: number | null
  requested_by_username: string | null

  title: string
  release: string | null
  
  artwork: Artwork | null

  season: number | null
  episode: number | null

  status: DownloadStatus
  progress: number

  size: number
  size_remaining: number

  time_left: string | null
  estimated_completion_time: string | null

  download_client: string | null
  protocol: string | null
  indexer: string | null

  error_message: string | null
}

export async function getDownloads(): Promise<Download[]> {
  const response = await fetch('/api/downloads')

  if (!response.ok) {
    throw new Error(
      `Failed to fetch downloads: ${response.status}`,
    )
  }

  return response.json()
}
