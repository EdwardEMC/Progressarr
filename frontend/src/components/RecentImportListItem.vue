<script setup lang="ts">
import type { RecentImport } from '../api/downloads'

const props = defineProps<{
  importItem: RecentImport
}>()

function formatRelativeTime(value: string): string {
  const date = new Date(value)
  const now = Date.now()
  const diff = Math.max(0, now - date.getTime())

  const seconds = Math.floor(diff / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)

  if (seconds < 60) {
    return 'Just now'
  }

  if (minutes < 60) {
    return `${minutes}m ago`
  }

  if (hours < 24) {
    return `${hours}h ago`
  }

  if (days < 7) {
    return `${days}d ago`
  }

  return date.toLocaleDateString([], {
    day: 'numeric',
    month: 'short',
  })
}

function formatSize(bytes: number | null): string {
  if (bytes === null || bytes === undefined) {
    return '—'
  }

  if (bytes < 1024 ** 2) {
    return `${(bytes / 1024).toFixed(0)} KB`
  }

  if (bytes < 1024 ** 3) {
    return `${(bytes / 1024 ** 2).toFixed(1)} MB`
  }

  return `${(bytes / 1024 ** 3).toFixed(1)} GB`
}

function formatMediaLabel(): string {
  if (props.importItem.media_type === 'movie') {
    return 'Movie'
  }

  if (
    props.importItem.season !== null &&
    props.importItem.episode !== null
  ) {
    return `S${String(props.importItem.season).padStart(2, '0')}E${String(
      props.importItem.episode,
    ).padStart(2, '0')}`
  }

  return 'Episode'
}
</script>

<template>
  <div
    class="group flex items-center gap-4 border-b border-white/5 py-3 last:border-b-0"
  >
    <!-- Poster -->
    <div
      class="h-14 w-10 shrink-0 overflow-hidden rounded-md bg-[#202020]"
    >
      <img
        v-if="importItem.artwork?.poster_url"
        :src="importItem.artwork.poster_url"
        :alt="importItem.title"
        class="h-full w-full object-cover"
        loading="lazy"
      />

      <div
        v-else
        class="flex h-full w-full items-center justify-center text-zinc-700"
      >
        <svg
          viewBox="0 0 24 24"
          fill="none"
          class="h-5 w-5"
        >
          <rect
            x="3"
            y="3"
            width="18"
            height="18"
            rx="2"
            stroke="currentColor"
            stroke-width="1.5"
          />
          <path
            d="M8 3V21M16 3V21"
            stroke="currentColor"
            stroke-width="1.5"
          />
        </svg>
      </div>
    </div>

    <!-- Main information -->
    <div class="min-w-0 flex-1">
      <div class="flex items-center gap-2">
        <h4
          class="truncate text-sm font-medium text-zinc-200 transition group-hover:text-white"
        >
          {{ importItem.title }}
        </h4>

        <span
          class="hidden shrink-0 rounded-md bg-emerald-500/10 px-1.5 py-0.5 text-[10px] font-medium uppercase tracking-wide text-emerald-400 sm:inline-flex"
        >
          Imported
        </span>
      </div>

      <div
        class="mt-1 flex min-w-0 items-center gap-2 text-xs text-zinc-500"
      >
        <span class="shrink-0">
          {{ formatMediaLabel() }}
        </span>

        <span class="text-zinc-700">•</span>

        <span v-if="importItem.quality" class="shrink-0">
          {{ importItem.quality }}
        </span>

        <span v-if="importItem.quality" class="text-zinc-700">•</span>

        <span class="shrink-0">
          {{ formatSize(importItem.size) }}
        </span>

        <span class="hidden text-zinc-700 sm:inline">•</span>

        <span class="hidden truncate sm:inline">
          {{ importItem.source }}
        </span>
      </div>
    </div>

    <!-- Time -->
    <div class="shrink-0 text-right">
      <span class="text-xs text-zinc-600">
        {{ formatRelativeTime(importItem.imported_at) }}
      </span>
    </div>
  </div>
</template>