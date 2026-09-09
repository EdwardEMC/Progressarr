<script setup lang="ts">
import type { RecentImportDisplayData } from '../../interfaces/import'

defineProps<{
  importItem: RecentImportDisplayData
}>()

function formatImportedAt(date: string): string {
  const importedAt = new Date(date)

  if (Number.isNaN(importedAt.getTime())) {
    return date
  }

  return importedAt.toLocaleDateString([], {
    day: 'numeric',
    month: 'short',
  })
}
</script>

<template>
  <article
    class="group overflow-hidden rounded-xl border border-white/8 bg-[#181818] transition hover:border-white/15 hover:bg-[#1c1c1c]"
  >
    <div class="relative aspect-2/3 overflow-hidden bg-[#101010]">
      <img
        v-if="importItem.posterUrl"
        :src="importItem.posterUrl"
        :alt="importItem.title"
        class="h-full w-full object-cover transition duration-300 group-hover:scale-105"
      />

      <div
        v-else
        class="flex h-full items-center justify-center text-zinc-600"
      >
        No artwork
      </div>

      <!-- Imported status -->
      <div class="absolute left-2 top-2">
        <span
          class="rounded-md bg-green-500/15 px-2 py-1 text-xs font-medium text-green-400 backdrop-blur"
        >
          Imported
        </span>
      </div>

      <!-- Source -->
      <div class="absolute right-2 top-2">
        <span
          class="rounded-md bg-black/50 px-2 py-1 text-xs font-medium uppercase text-zinc-300 backdrop-blur"
        >
          {{ importItem.source }}
        </span>
      </div>
    </div>

    <div class="p-3">
      <h3
        class="truncate text-sm font-medium text-white"
        :title="importItem.title"
      >
        {{ importItem.title }}
      </h3>

      <!-- Episode information -->
      <div
        v-if="
          (importItem.mediaType === 'tv' ||
            importItem.mediaType === 'episode') &&
          (importItem.season !== null || importItem.episode !== null)
        "
        class="mt-1 text-sm text-zinc-400"
      >
        <span v-if="importItem.season !== null">
          Season {{ importItem.season }}
        </span>

        <span
          v-if="
            importItem.season !== null &&
            importItem.episode !== null
          "
          class="mx-1 text-zinc-600"
        >
          •
        </span>

        <span v-if="importItem.episode !== null">
          Episode {{ importItem.episode }}
        </span>
      </div>

      <div
        v-else
        class="mt-1 text-sm text-zinc-400"
      >
        Movie
      </div>

      <div
        class="mt-2 flex items-center justify-between gap-2 text-xs text-zinc-500"
      >
        <span>
          {{ importItem.quality ?? 'Unknown quality' }}
        </span>

        <span>
          {{ importItem.size }}
        </span>
      </div>

      <div class="mt-1 text-xs text-zinc-600">
        Imported {{ formatImportedAt(importItem.importedAt) }}
      </div>
    </div>
  </article>
</template>