export type DownloadSortKey =
  | 'title'
  | 'status'
  | 'progress'
  | 'size'
  | 'size_remaining'
  | 'media_type'
  | 'download_client'
  | 'indexer'
  | 'requested_by'

export type DownloadSortDirection = 'asc' | 'desc'

export type RecentImportSortKey =
  | 'imported_at'
  | 'title'
  | 'size'
  | 'quality'

export type RecentImportSortDirection =
  | 'asc'
  | 'desc'
  