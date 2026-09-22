<script setup lang="ts">
import type { DownloadDisplayData } from '../../interfaces/download'

defineProps<{
  download: DownloadDisplayData
}>()
</script>

<template>
  <article
    class="flex items-center gap-4 rounded-xl border border-zinc-200 bg-white p-3 transition hover:border-zinc-300 hover:bg-zinc-50 dark:border-white/8 dark:bg-[#181818] dark:hover:border-white/15 dark:hover:bg-[#1c1c1c]"
  >
    <div class="h-20 w-14 shrink-0 overflow-hidden rounded-lg bg-zinc-50 dark:bg-[#101010]">
      <img
        v-if="download.posterUrl"
        :src="download.posterUrl"
        :alt="download.title"
        class="h-full w-full object-cover"
      />
    </div>

    <div class="min-w-0 flex-1">
      <div class="flex items-center gap-2">
        <h3 class="truncate font-medium text-zinc-900 dark:text-white">
          {{ download.title }}
        </h3>

        <span
          class="shrink-0 rounded-md px-2 py-1 text-xs font-medium"
          :class="download.statusClass"
        >
          {{ download.status }}
        </span>
      </div>

      <div class="mt-1 flex items-center gap-2 text-xs">
        <!-- Episode information -->
        <div
          v-if="
            (download.mediaType === 'tv' || download.mediaType === 'episode') &&
            (download.season !== null || download.episode !== null)
          "
          class="flex items-center text-zinc-600 dark:text-zinc-400"
        >
          <span v-if="download.season !== null"> Season {{ download.season }} </span>

          <span
            v-if="download.season !== null && download.episode !== null"
            class="mx-1 text-zinc-400 dark:text-zinc-600"
          >
            •
          </span>

          <span v-if="download.episode !== null"> Episode {{ download.episode }} </span>
        </div>

        <p v-if="download.requestedBy" class="text-zinc-500">
          Requested by {{ download.requestedBy }}
        </p>
      </div>

      <div class="mt-1 flex flex-wrap gap-x-4 gap-y-1 text-xs text-zinc-500">
        <span v-if="download.downloadClient">
          {{ download.downloadClient }}
        </span>

        <span v-if="download.indexer">
          {{ download.indexer }}
        </span>

        <span>
          {{ download.size }}
        </span>

        <span v-if="download.timeLeft">
          {{ download.timeLeft }}
        </span>
      </div>

      <div class="mt-3 flex items-center gap-3">
        <div class="h-1.5 flex-1 overflow-hidden rounded-full bg-zinc-200 dark:bg-black/40">
          <div
            class="h-full rounded-full bg-linear-to-r from-[#aa5cc3] to-[#00a4dc]"
            :style="{ width: `${download.progress}%` }"
          />
        </div>

        <span class="w-10 text-right text-xs text-zinc-600 dark:text-zinc-400">
          {{ download.progress.toFixed(0) }}%
        </span>
      </div>
    </div>
  </article>
</template>
