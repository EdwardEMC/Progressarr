<script setup lang="ts">
import type { DownloadDisplayData } from '../../interfaces/download'

defineProps<{
  download: DownloadDisplayData
}>()
</script>
<template>
  <article
    class="flex items-center gap-4 rounded-xl border border-white/8 bg-[#181818] p-3 transition hover:border-white/15 hover:bg-[#1c1c1c]"
  >
    <div class="h-20 w-14 shrink-0 overflow-hidden rounded-lg bg-[#101010]">
      <img
        v-if="download.posterUrl"
        :src="download.posterUrl"
        :alt="download.title"
        class="h-full w-full object-cover"
      />
    </div>
    <div class="min-w-0 flex-1">
      <div class="flex items-center gap-2">
        <h3 class="truncate font-medium text-white">{{ download.title }}</h3>
        <span
          class="shrink-0 rounded-md px-2 py-1 text-xs font-medium"
          :class="download.statusClass"
        >
          {{ download.status }}
        </span>
      </div>
      <div class="mt-1 flex flex-wrap gap-x-4 gap-y-1 text-xs text-zinc-500">
        <span v-if="download.downloadClient"> {{ download.downloadClient }} </span>
        <span v-if="download.indexer"> {{ download.indexer }} </span>
        <span> {{ download.size }} </span>
        <span v-if="download.timeLeft"> {{ download.timeLeft }} </span>
      </div>
      <div class="mt-3 flex items-center gap-3">
        <div class="h-1.5 flex-1 overflow-hidden rounded-full bg-black/40">
          <div
            class="h-full rounded-full bg-linear-to-r from-[#aa5cc3] to-[#00a4dc]"
            :style="{ width: `${download.progress}%` }"
          />
        </div>
        <span class="w-10 text-right text-xs text-zinc-400">
          {{ download.progress.toFixed(0) }}%
        </span>
      </div>
    </div>
  </article>
</template>
