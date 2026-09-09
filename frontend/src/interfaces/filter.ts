import type { DownloadSortDirection, DownloadSortKey, RecentImportSortDirection, RecentImportSortKey } from "../types/filter"

export interface DownloadFilterState {
  search: string
  status: string
  mediaType: string
  protocol: string
  downloadClient: string
  indexer: string
  requestedBy: string
  progress: string
  sortBy: DownloadSortKey
  sortDirection: DownloadSortDirection
}

export interface RecentImportFilterState {
  search: string
  mediaType: string
  source: string
  quality: string
  season: number | null
  fromDate: string
  toDate: string
  sort: RecentImportSortKey
  sortDirection: RecentImportSortDirection
}