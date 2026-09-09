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
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}
</script>

<template>
  <article
    class="group relative overflow-hidden rounded-xl border border-white/8 bg-[#181818]"
  >
    <!-- Backdrop -->
    <div class="relative h-48 overflow-hidden">
      <img
        v-if="importItem.backdropUrl"
        :src="importItem.backdropUrl"
        :alt="importItem.title"
        class="h-full w-full object-cover transition duration-300 group-hover:scale-105"
      />

      <div
        v-else
        class="h-full w-full bg-linear-to-br from-[#181818] to-[#101010]"
      />

      <!-- Backdrop gradient -->
      <div
        class="absolute inset-0 bg-linear-to-t from-[#181818] via-[#181818]/40 to-transparent"
      />

      <!-- Imported status -->
      <div class="absolute left-4 top-4">
        <span
          class="rounded-md bg-green-500/15 px-2.5 py-1 text-xs font-medium text-green-400 backdrop-blur-md"
        >
          Imported
        </span>
      </div>

      <!-- Source -->
      <div class="absolute right-4 top-4">
        <span
          class="rounded-md bg-black/50 px-2.5 py-1 text-xs font-medium uppercase text-zinc-300 backdrop-blur-md"
        >
          {{ importItem.source }}
        </span>
      </div>

      <!-- Poster -->
      <div
        class="absolute bottom-0 left-5 h-32 w-22 overflow-hidden rounded-lg border border-white/10 bg-[#101010] shadow-xl"
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
    </div>

    <!-- Content -->
    <div class="p-5 pt-4">
      <div class="ml-26 min-h-32">
        <h3
          class="line-clamp-2 text-lg font-semibold text-white"
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
          class="mt-3 text-sm text-zinc-400"
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

        <!-- Movie type -->
        <div
          v-else
          class="mt-3 text-sm text-zinc-400"
        >
          Movie
        </div>
      </div>

      <!-- Metadata -->
      <div class="mt-5 grid grid-cols-2 gap-3 sm:grid-cols-4">
        <!-- Quality -->
        <div
          v-if="importItem.quality"
          class="rounded-lg bg-[#101010] p-3"
        >
          <p class="text-xs text-zinc-600">Quality</p>

          <p
            class="mt-1 truncate text-sm font-medium text-zinc-300"
            :title="importItem.quality"
          >
            {{ importItem.quality }}
          </p>
        </div>

        <!-- Size -->
        <div class="rounded-lg bg-[#101010] p-3">
          <p class="text-xs text-zinc-600">Size</p>

          <p class="mt-1 text-sm font-medium text-zinc-300">
            {{ importItem.size }}
          </p>
        </div>

        <!-- Imported -->
        <div class="rounded-lg bg-[#101010] p-3">
          <p class="text-xs text-zinc-600">Imported</p>

          <p class="mt-1 text-sm font-medium text-zinc-300">
            {{ formatImportedAt(importItem.importedAt) }}
          </p>
        </div>

        <!-- Source -->
        <div class="rounded-lg bg-[#101010] p-3">
          <p class="text-xs text-zinc-600">Source</p>

          <p
            class="mt-1 truncate text-sm font-medium capitalize text-zinc-300"
          >
            {{ importItem.source }}
          </p>
        </div>
      </div>

      <!-- Release -->
      <div
        v-if="importItem.release"
        class="mt-4 rounded-lg bg-[#101010] p-3"
      >
        <p class="text-xs text-zinc-600">Release</p>

        <p
          class="mt-1 truncate text-sm text-zinc-400"
          :title="importItem.release"
        >
          {{ importItem.release }}
        </p>
      </div>
    </div>
  </article>
</template>