import type { Download } from '../api/downloads'

export interface DownloadDisplayData {
  id: Download['id']
  title: Download['title']

  status: string
  statusClass: string
  progress: Download['progress']

  posterUrl: string | null
  backdropUrl: string | null

  protocol: Download['protocol']
  requestedBy: string | null

  mediaType: Download['media_type']
  season: Download['season'] | null
  episode: Download['episode'] | null

  size: string
  sizeRemaining: string

  downloadClient: string | null
  indexer: string | null
  timeLeft: string | null

  release: string | null
}
