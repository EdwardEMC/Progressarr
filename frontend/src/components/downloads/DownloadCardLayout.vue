<script setup lang="ts">
import type { DownloadDisplayData } from '../../interfaces/download'

defineProps<{
  download: DownloadDisplayData
}>()
</script>

<template>
  <article class="group relative overflow-hidden rounded-xl border border-white/8 bg-[#181818]">
    <!-- Backdrop -->
    <div class="relative h-48 overflow-hidden">
      <img
        v-if="download.backdropUrl"
        :src="download.backdropUrl"
        :alt="download.title"
        class="h-full w-full object-cover transition duration-300 group-hover:scale-105"
      />

      <div v-else class="h-full w-full bg-linear-to-br from-[#181818] to-[#101010]" />

      <!-- Backdrop gradient -->
      <div class="absolute inset-0 bg-linear-to-t from-[#181818] via-[#181818]/40 to-transparent" />

      <!-- Status -->
      <div class="absolute left-4 top-4">
        <span
          class="rounded-md px-2.5 py-1 text-xs font-medium backdrop-blur-md"
          :class="download.statusClass"
        >
          {{ download.status }}
        </span>
      </div>

      <!-- Protocol -->
      <div class="absolute right-4 top-4">
        <span
          class="rounded-md bg-black/50 px-2.5 py-1 text-xs font-medium text-zinc-300 backdrop-blur-md"
        >
          {{ download.protocol }}
        </span>
      </div>

      <!-- Poster -->
      <div
        class="absolute bottom-0 left-5 h-32 w-22 overflow-hidden rounded-lg border border-white/10 bg-[#101010] shadow-xl"
      >
        <img
          v-if="download.posterUrl"
          :src="download.posterUrl"
          :alt="download.title"
          class="h-full w-full object-cover"
        />

        <div v-else class="flex h-full items-center justify-center text-xs text-zinc-600">
          No artwork
        </div>
      </div>
    </div>

    <!-- Content -->
    <div class="p-5 pt-4">
      <div class="ml-26 min-h-32">
        <h3 class="line-clamp-2 text-lg font-semibold text-white" :title="download.title">
          {{ download.title }}
        </h3>

        <p v-if="download.requestedBy" class="mt-1 text-sm text-zinc-500">
          Requested by {{ download.requestedBy }}
        </p>

        <!-- Episode information -->
        <div
          v-if="
            download.mediaType === 'tv' && (download.season !== null || download.episode !== null)
          "
          class="mt-3 text-sm text-zinc-400"
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
      </div>

      <!-- Progress -->
      <div class="mt-5">
        <div class="mb-2 flex items-center justify-between text-xs">
          <span class="text-zinc-500"> Progress </span>

          <span class="font-medium text-zinc-300"> {{ download.progress.toFixed(1) }}% </span>
        </div>

        <div class="h-2 overflow-hidden rounded-full bg-black/40">
          <div
            class="h-full rounded-full bg-linear-to-r from-[#aa5cc3] to-[#00a4dc] transition-all duration-300"
            :style="{ width: `${download.progress}%` }"
          />
        </div>
      </div>

      <!-- Metadata -->
      <div class="mt-5 grid grid-cols-2 gap-3 sm:grid-cols-4">
        <!-- Download client -->
        <div v-if="download.downloadClient" class="rounded-lg bg-[#101010] p-3">
          <p class="text-xs text-zinc-600">Client</p>

          <p
            class="mt-1 truncate text-sm font-medium text-zinc-300"
            :title="download.downloadClient"
          >
            {{ download.downloadClient }}
          </p>
        </div>

        <!-- Indexer -->
        <div v-if="download.indexer" class="rounded-lg bg-[#101010] p-3">
          <p class="text-xs text-zinc-600">Indexer</p>

          <p class="mt-1 truncate text-sm font-medium text-zinc-300" :title="download.indexer">
            {{ download.indexer }}
          </p>
        </div>

        <!-- Time remaining -->
        <div v-if="download.timeLeft" class="rounded-lg bg-[#101010] p-3">
          <p class="text-xs text-zinc-600">Time Remaining</p>

          <p class="mt-1 text-sm font-medium text-zinc-300">
            {{ download.timeLeft }}
          </p>
        </div>

        <!-- Remaining -->
        <div class="rounded-lg bg-[#101010] p-3">
          <p class="text-xs text-zinc-600">Remaining</p>

          <p class="mt-1 text-sm font-medium text-zinc-300">
            {{ download.sizeRemaining }}
          </p>
        </div>
      </div>

      <!-- Release -->
      <div v-if="download.release" class="mt-4 rounded-lg bg-[#101010] p-3">
        <p class="text-xs text-zinc-600">Release</p>

        <p class="mt-1 truncate text-sm text-zinc-400" :title="download.release">
          {{ download.release }}
        </p>
      </div>
    </div>
  </article>
</template>
