export interface RecentImportDisplayData {
  id: string
  title: string

  posterUrl: string | null
  backdropUrl: string | null

  mediaType: string
  season: number | null
  episode: number | null

  quality: string | null
  size: string

  importedAt: string
  source: string

  release: string | null
}