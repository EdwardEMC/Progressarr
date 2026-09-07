<script setup lang="ts">
import type { DownloadDisplayData } from '../../interfaces/download'

defineProps<{
  download: DownloadDisplayData
}>()
</script>
<template>
  <article
    class="group overflow-hidden rounded-xl border border-white/8 bg-[#181818] transition hover:border-white/15 hover:bg-[#1c1c1c]"
  >
    <div class="relative aspect-2/3 overflow-hidden bg-[#101010]">
      <img
        v-if="download.posterUrl"
        :src="download.posterUrl"
        :alt="download.title"
        class="h-full w-full object-cover transition duration-300 group-hover:scale-105"
      />
      <div v-else class="flex h-full items-center justify-center text-zinc-600">No artwork</div>
      <div class="absolute left-2 top-2">
        <span
          class="rounded-md px-2 py-1 text-xs font-medium backdrop-blur"
          :class="download.statusClass"
        >
          {{ download.status }}
        </span>
      </div>
      <div class="absolute inset-x-0 bottom-0 h-1 bg-black/50">
        <div
          class="h-full bg-linear-to-r from-[#aa5cc3] to-[#00a4dc]"
          :style="{ width: `${download.progress}%` }"
        />
      </div>
    </div>
    <div class="p-3">
      <h3 class="truncate text-sm font-medium text-white" :title="download.title">
        {{ download.title }}
      </h3>
      
      <p v-if="download.requestedBy" class="mt-1 text-sm text-zinc-500">
        Requested by {{ download.requestedBy }}
      </p>

      <!-- Episode information -->
      <div
        v-if="
          (download.mediaType === 'tv' || download.mediaType === 'episode') && (download.season !== null || download.episode !== null)
        "
        class="mt-1 text-sm text-zinc-400"
      >
        <span v-if="download.season !== null"> Season {{ download.season }} </span>

        <span
          v-if="download.season !== null && download.episode !== null"
          class="mx-1 text-zinc-600"
        >
          •
        </span>

        <span v-if="download.episode !== null"> Episode {{ download.episode }} </span>
      </div>

      <div class="mt-1 flex items-center justify-between gap-2 text-xs text-zinc-500">
        <span>{{ download.size }}</span> <span>{{ download.progress.toFixed(0) }}%</span>
      </div>
    </div>
  </article>
</template>
