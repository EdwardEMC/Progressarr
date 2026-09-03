<script setup lang="ts">
import type { Download } from '../api/downloads'

defineProps<{
  download: Download
}>()

function formatBytes(bytes: number): string {
  if (bytes <= 0) {
    return '0 B'
  }

  const units = ['B', 'KB', 'MB', 'GB', 'TB']
  const index = Math.min(Math.floor(Math.log(bytes) / Math.log(1024)), units.length - 1)

  return `${(bytes / Math.pow(1024, index)).toFixed(1)} ${units[index]}`
}

function formatStatus(status: string): string {
  switch (status) {
    case 'downloading':
      return 'Downloading'

    case 'import_pending':
      return 'Importing'

    case 'completed':
      return 'Completed'

    case 'failed':
      return 'Failed'

    default:
      return 'Waiting'
  }
}

function statusClass(status: string): string {
  switch (status) {
    case 'downloading':
      return 'bg-[#00a4dc]/15 text-[#4dc8ed]'

    case 'import_pending':
      return 'bg-purple-500/15 text-purple-300'

    case 'completed':
      return 'bg-emerald-500/15 text-emerald-300'

    case 'failed':
      return 'bg-red-500/15 text-red-300'

    default:
      return 'bg-zinc-800 text-zinc-300'
  }
}
</script>

<template>
  <article
    class="group overflow-hidden rounded-xl border border-white/8 bg-[#181818] shadow-xl transition duration-300 hover:border-white/15 hover:bg-[#1c1c1c]"
  >
    <!-- Artwork / hero area -->
    <div class="relative h-64 overflow-hidden bg-zinc-900">
      <img
        v-if="download.artwork?.backdrop_url"
        :src="download.artwork.backdrop_url"
        :alt="download.title"
        class="absolute inset-0 h-full w-full object-cover opacity-40 transition-transform duration-700 group-hover:scale-105"
        @load="console.log('BACKDROP LOADED:', download.artwork.backdrop_url)"
        @error="console.error('BACKDROP ERROR:', download.artwork.backdrop_url)"
      />

      <div
        class="absolute inset-0 bg-gradient-to-t from-[#181818] via-[#181818]/60 to-transparent"
      />

      <div
        class="absolute inset-0 bg-gradient-to-r from-[#181818]/80 via-transparent to-transparent"
      />

      <div class="relative z-10 flex h-full items-end p-4 sm:p-6">
        <div class="flex min-w-0 w-full gap-3 sm:gap-5">
          <img
            v-if="download.artwork?.poster_url"
            :src="download.artwork.poster_url"
            :alt="download.title"
            class="h-auto w-24 sm:w-28 md:w-32 lg:w-36 max-h-48 shrink-0 self-end rounded-md object-cover shadow-xl"
            @load="console.log('POSTER LOADED:', download.artwork.poster_url)"
            @error="console.error('POSTER ERROR:', download.artwork.poster_url)"
          />

          <div class="min-w-0 flex-1 self-end">
            <div class="mb-2 sm:mb-3 flex flex-wrap items-center gap-2">
              <span
                class="rounded-full px-2.5 py-1 text-xs font-medium"
                :class="statusClass(download.status)"
              >
                {{ formatStatus(download.status) }}
              </span>

              <span
                v-if="download.protocol"
                class="rounded-full bg-black/40 px-2.5 py-1 text-xs text-zinc-300"
              >
                {{ download.protocol }}
              </span>
            </div>

            <h2 class="text-xl sm:text-2xl font-semibold tracking-tight text-white line-clamp-2">
              {{ download.title }}
            </h2>

            <div v-if="download.requested_by_username" class="text-sm text-gray-400">
              Requested by {{ download.requested_by_username }}
            </div>

            <p v-if="download.media_type === 'episode'" class="mt-1 text-sm text-zinc-300">
              Season {{ download.season }} · Episode {{ download.episode }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Main content -->
    <div class="p-6">
      <div class="mb-2 flex items-end justify-between">
        <div>
          <p class="text-sm text-zinc-500">
            {{ formatBytes(download.size - download.size_remaining) }}
            of
            {{ formatBytes(download.size) }}
          </p>
        </div>

        <span class="text-2xl font-semibold text-white"> {{ download.progress.toFixed(0) }}% </span>
      </div>

      <!-- Progress -->
      <div class="h-2 overflow-hidden rounded-full bg-zinc-800">
        <div
          class="h-full rounded-full bg-gradient-to-r from-[#aa5cc3] to-[#00a4dc] transition-all duration-700"
          :style="{ width: `${download.progress}%` }"
        />
      </div>

      <!-- Download information -->
      <div class="mt-6 grid grid-cols-2 gap-x-6 gap-y-5 border-t border-white/6 pt-5">
        <div>
          <p class="text-xs uppercase tracking-wider text-zinc-600">Client</p>

          <p class="mt-1 text-sm text-zinc-300">
            {{ download.download_client ?? 'Unknown' }}
          </p>
        </div>

        <div>
          <p class="text-xs uppercase tracking-wider text-zinc-600">Indexer</p>

          <p class="mt-1 truncate text-sm text-zinc-300" :title="download.indexer ?? undefined">
            {{ download.indexer ?? 'Unknown' }}
          </p>
        </div>

        <div v-if="download.time_left">
          <p class="text-xs uppercase tracking-wider text-zinc-600">Time remaining</p>

          <p class="mt-1 text-sm text-zinc-300">
            {{ download.time_left }}
          </p>
        </div>

        <div>
          <p class="text-xs uppercase tracking-wider text-zinc-600">Remaining</p>

          <p class="mt-1 text-sm text-zinc-300">
            {{ formatBytes(download.size_remaining) }}
          </p>
        </div>
      </div>

      <!-- Release -->
      <div v-if="download.release" class="mt-5 border-t border-white/6 pt-4">
        <p class="mb-1 text-xs uppercase tracking-wider text-zinc-600">Release</p>

        <p class="truncate text-xs text-zinc-500" :title="download.release">
          {{ download.release }}
        </p>
      </div>
    </div>
  </article>
</template>
