<script setup lang="ts">
import { computed } from 'vue'
import type { RecentImport } from '../api/downloads'

import RecentImportCardLayout from './imports/RecentImportCardLayout.vue'
import RecentImportGridItem from './imports/RecentImportGridItem.vue'
import RecentImportRowItem from './imports/RecentImportRowItem.vue'

import { formatBytes } from '../shared/downloadFormatting.ts'

import type { DownloadView } from '../types/download.ts'

const props = withDefaults(
  defineProps<{
    importItem: RecentImport
    view?: DownloadView
  }>(),
  {
    view: 'card',
  },
)

const layoutComponent = computed(() => {
  switch (props.view) {
    case 'grid':
      return RecentImportGridItem

    case 'row':
      return RecentImportRowItem

    case 'card':
    default:
      return RecentImportCardLayout
  }
})

const displayData = computed(() => ({
  id: props.importItem.id,
  title: props.importItem.title,

  posterUrl: props.importItem.artwork?.poster_url ?? null,
  backdropUrl: props.importItem.artwork?.backdrop_url ?? null,

  mediaType: props.importItem.media_type,
  season: props.importItem.season,
  episode: props.importItem.episode,

  quality: props.importItem.quality,
  size: formatBytes(props.importItem.size),

  importedAt: props.importItem.imported_at,
  source: props.importItem.source,

  release: props.importItem.release,
}))
</script>

<template>
  <component :is="layoutComponent" :import-item="displayData" />
</template>