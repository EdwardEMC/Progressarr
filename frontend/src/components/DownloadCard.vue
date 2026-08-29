<script setup lang="ts">
import type { Download } from '../api/downloads'

defineProps<{
  download: Download
}>()

function formatBytes(bytes: number): string {
  if (bytes === 0) {
    return '0 B'
  }

  const units = ['B', 'KB', 'MB', 'GB', 'TB']
  const index = Math.floor(
    Math.log(bytes) / Math.log(1024),
  )

  return `${(bytes / Math.pow(1024, index)).toFixed(2)} ${units[index]}`
}
</script>

<template>
  <article
    class="rounded-xl border border-zinc-800 bg-zinc-900 p-5 shadow-lg"
  >
    <div class="mb-4 flex items-start justify-between gap-4">
      <div>
        <h2 class="text-lg font-semibold text-white">
          {{ download.title }}
        </h2>

        <p
          v-if="download.media_type === 'episode'"
          class="mt-1 text-sm text-zinc-400"
        >
          Season {{ download.season }} · Episode {{ download.episode }}
        </p>
      </div>

      <span
        class="rounded-full bg-zinc-800 px-3 py-1 text-xs font-medium text-zinc-300"
      >
        {{ download.status.replace('_', ' ') }}
      </span>
    </div>

    <div class="mb-2 flex items-center justify-between text-sm">
      <span class="text-zinc-400">
        Progress
      </span>

      <span class="font-medium text-white">
        {{ download.progress.toFixed(0) }}%
      </span>
    </div>

    <div class="h-2 overflow-hidden rounded-full bg-zinc-800">
      <div
        class="h-full rounded-full bg-blue-500 transition-all duration-500"
        :style="{ width: `${download.progress}%` }"
      />
    </div>

    <div class="mt-4 grid grid-cols-2 gap-4 text-sm">
      <div>
        <p class="text-zinc-500">Size</p>
        <p class="text-zinc-200">
          {{ formatBytes(download.size) }}
        </p>
      </div>

      <div>
        <p class="text-zinc-500">Remaining</p>
        <p class="text-zinc-200">
          {{ formatBytes(download.size_remaining) }}
        </p>
      </div>

      <div>
        <p class="text-zinc-500">Client</p>
        <p class="text-zinc-200">
          {{ download.download_client ?? 'Unknown' }}
        </p>
      </div>

      <div>
        <p class="text-zinc-500">Indexer</p>
        <p class="truncate text-zinc-200">
          {{ download.indexer ?? 'Unknown' }}
        </p>
      </div>
    </div>

    <div
      v-if="download.time_left && download.status === 'downloading'"
      class="mt-4 border-t border-zinc-800 pt-4 text-sm"
    >
      <span class="text-zinc-500">ETA</span>
      <span class="ml-2 text-zinc-200">
        {{ download.time_left }}
      </span>
    </div>
  </article>
</template>
