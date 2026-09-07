import type { Download } from '../../api/downloads'

export function formatBytes(bytes: number | null | undefined): string {
  if (!bytes || bytes <= 0) {
    return '0 B'
  }

  const units = ['B', 'KB', 'MB', 'GB', 'TB']
  const exponent = Math.min(Math.floor(Math.log(bytes) / Math.log(1024)), units.length - 1)

  return `${(bytes / Math.pow(1024, exponent)).toFixed(1)} ${units[exponent]}`
}

export function formatStatus(status: Download['status']): string {
  switch (status) {
    case 'downloading':
      return 'Downloading'
    case 'import_pending':
      return 'Import Pending'
    case 'completed':
      return 'Completed'
    case 'failed':
      return 'Failed'
    default:
      return 'Waiting'
  }
}

export function getStatusClass(status: Download['status']): string {
  switch (status) {
    case 'downloading':
      return 'bg-[#00a4dc]/15 text-[#00a4dc]'
    case 'import_pending':
      return 'bg-yellow-500/15 text-yellow-400'
    case 'completed':
      return 'bg-green-500/15 text-green-400'
    case 'failed':
      return 'bg-red-500/15 text-red-400'
    default:
      return 'bg-zinc-500/15 text-zinc-400'
  }
}
