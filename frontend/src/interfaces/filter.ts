import type { DownloadSortDirection, DownloadSortKey } from "../types/filter"

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
