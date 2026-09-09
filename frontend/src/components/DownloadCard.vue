<script setup lang="ts">
import { computed } from 'vue'
import type { Download } from '../api/downloads'

import DownloadCardLayout from './downloads/DownloadCardLayout.vue'
import DownloadGridItem from './downloads/DownloadGridItem.vue'
import DownloadRowItem from './downloads/DownloadRowItem.vue'

import { formatBytes, formatStatus, getStatusClass } from '../shared/downloadFormatting.ts'

import type { DownloadView } from '../types/download.ts'
import type { DownloadDisplayData } from '../interfaces/download.ts'

const props = withDefaults(
  defineProps<{
    download: Download
    view?: DownloadView
  }>(),
  {
    view: 'card',
  },
)

const layoutComponent = computed(() => {
  switch (props.view) {
    case 'grid':
      return DownloadGridItem

    case 'row':
      return DownloadRowItem

    case 'card':
    default:
      return DownloadCardLayout
  }
})

const displayData = computed<DownloadDisplayData>(() => ({
  id: props.download.id,
  title: props.download.title,

  status: formatStatus(props.download.status),
  statusClass: getStatusClass(props.download.status),
  progress: props.download.progress,

  posterUrl: props.download.artwork?.poster_url ?? null,
  backdropUrl: props.download.artwork?.backdrop_url ?? null,

  protocol: props.download.protocol,
  requestedBy: props.download.requested_by_username ?? null,

  mediaType: props.download.media_type,
  season: props.download.season ?? null,
  episode: props.download.episode ?? null,

  size: formatBytes(props.download.size),
  sizeRemaining: formatBytes(props.download.size_remaining),

  downloadClient: props.download.download_client ?? null,
  indexer: props.download.indexer ?? null,
  timeLeft: props.download.time_left ?? null,

  release: props.download.release ?? null,
}))
</script>

<template>
  <component :is="layoutComponent" :download="displayData" />
</template>
