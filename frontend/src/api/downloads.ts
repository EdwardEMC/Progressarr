import type { RecentImportFilterState } from "../interfaces/filter"

export interface Artwork {
  poster_url: string | null
  backdrop_url: string | null
}

export type DownloadStatus = 'downloading' | 'import_pending' | 'failed' | 'completed' | 'unknown'

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

export interface RecentImport {
   id: string 
   media_type: string 
   service_item_id: number | null 

   title: string 
   release: string | null 

   artwork: Artwork | null 
   
   season: number | null 
   episode: number | null 

   quality: string | null 
   size: number | null 

   imported_at: string 
   source: string 
}

export interface RecentImportResponse {
  items: RecentImport[]
  page: number
  page_size: number
  has_more: boolean
}

export async function getDownloads(): Promise<Download[]> {
  const response = await fetch('/api/downloads')

  if (!response.ok) {
    throw new Error(`Failed to fetch downloads: ${response.status}`)
  }

  return response.json()
}

export async function getRecentDownloads(): Promise<RecentImport[]> {
  const response = await fetch(
    '/api/downloads/recent?page=1&page_size=6',
  )

  if (!response.ok) {
    throw new Error(
      `Failed to fetch recent downloads: ${response.status}`,
    )
  }

  const data: RecentImportResponse = await response.json()

  return data.items
}

export async function getImportHistory(
  filters: RecentImportFilterState,
  page = 1,
  pageSize = 25,
): Promise<RecentImportResponse> {
  const params = new URLSearchParams({
    page: String(page),
    page_size: String(pageSize),
  })

  if (filters.search.trim()) {
    params.set('search', filters.search.trim())
  }

  if (filters.mediaType) {
    params.set('media_type', filters.mediaType)
  }

  if (filters.source) {
    params.set('source', filters.source)
  }

  if (filters.quality) {
    params.set('quality', filters.quality)
  }

  if (filters.season !== null) {
    params.set('season', String(filters.season))
  }

  if (filters.fromDate) {
    params.set('from_date', filters.fromDate)
  }

  if (filters.toDate) {
    params.set('to_date', filters.toDate)
  }

  params.set('sort', filters.sort)
  params.set('sort_direction', filters.sortDirection)

  const response = await fetch(
    `/api/downloads/recent?${params.toString()}`,
  )

  if (!response.ok) {
    throw new Error(
      `Failed to fetch import history: ${response.status}`,
    )
  }

  return response.json()
}