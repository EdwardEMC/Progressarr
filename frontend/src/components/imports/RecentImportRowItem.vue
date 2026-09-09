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

  return importedAt.toLocaleString([], {
    day: 'numeric',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
  })
}
</script>

<template>
  <article
    class="flex items-center gap-4 rounded-xl border border-white/8 bg-[#181818] p-3 transition hover:border-white/15 hover:bg-[#1c1c1c]"
  >
    <!-- Poster -->
    <div
      class="h-20 w-14 shrink-0 overflow-hidden rounded-lg bg-[#101010]"
    >
      <img
        v-if="importItem.posterUrl"
        :src="importItem.posterUrl"
        :alt="importItem.title"
        class="h-full w-full object-cover"
      />

      <div
        v-else
        class="flex h-full items-center justify-center text-xs text-zinc-600"
      >
        No artwork
      </div>
    </div>

    <!-- Content -->
    <div class="min-w-0 flex-1">
      <div class="flex items-center gap-2">
        <h3
          class="truncate font-medium text-white"
          :title="importItem.title"
        >
          {{ importItem.title }}
        </h3>

        <span
          class="shrink-0 rounded-md bg-green-500/15 px-2 py-1 text-xs font-medium text-green-400"
        >
          Imported
        </span>
      </div>

      <div class="mt-1 flex items-center gap-2 text-xs">
        <!-- Episode information -->
        <div
          v-if="
            (importItem.mediaType === 'tv' ||
              importItem.mediaType === 'episode') &&
            (importItem.season !== null || importItem.episode !== null)
          "
          class="flex items-center text-zinc-400"
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

        <span
          v-else
          class="text-zinc-400"
        >
          Movie
        </span>
      </div>

      <div
        class="mt-1 flex flex-wrap gap-x-4 gap-y-1 text-xs text-zinc-500"
      >
        <span v-if="importItem.quality">
          {{ importItem.quality }}
        </span>

        <span>
          {{ importItem.size }}
        </span>

        <span>
          {{ importItem.source }}
        </span>

        <span>
          {{ formatImportedAt(importItem.importedAt) }}
        </span>
      </div>

      <!-- Release -->
      <div
        v-if="importItem.release"
        class="mt-1 truncate text-xs text-zinc-600"
        :title="importItem.release"
      >
        {{ importItem.release }}
      </div>
    </div>
  </article>
</template>