<script setup lang="ts">
import { onMounted, ref } from 'vue'

import DownloadCard from './components/DownloadCard.vue'
import {
  getDownloads,
  type Download,
} from './api/downloads'

const downloads = ref<Download[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

async function loadDownloads(): Promise<void> {
  try {
    loading.value = true
    error.value = null

    downloads.value = await getDownloads()
  } catch (err) {
    error.value =
      err instanceof Error
        ? err.message
        : 'Unable to load downloads.'
  } finally {
    loading.value = false
  }
}

onMounted(loadDownloads)
</script>

<template>
  <div class="min-h-screen bg-zinc-950 text-white">
    <header class="border-b border-zinc-800">
      <div class="mx-auto max-w-6xl px-6 py-6">
        <h1 class="text-2xl font-bold">
          Progressarr
        </h1>

        <p class="mt-1 text-sm text-zinc-400">
          Media download progress
        </p>
      </div>
    </header>

    <main class="mx-auto max-w-6xl px-6 py-8">
      <div
        v-if="loading"
        class="text-sm text-zinc-400"
      >
        Loading downloads...
      </div>

      <div
        v-else-if="error"
        class="rounded-xl border border-red-900 bg-red-950/40 p-5"
      >
        <h2 class="font-semibold text-red-400">
          Unable to load downloads
        </h2>

        <p class="mt-2 text-sm text-red-300">
          {{ error }}
        </p>
      </div>

      <div
        v-else-if="downloads.length === 0"
        class="rounded-xl border border-zinc-800 bg-zinc-900 p-8 text-center"
      >
        <h2 class="font-semibold">
          Nothing downloading
        </h2>

        <p class="mt-2 text-sm text-zinc-400">
          There are currently no active downloads.
        </p>
      </div>

      <div
        v-else
        class="grid gap-5 md:grid-cols-2"
      >
        <DownloadCard
          v-for="download in downloads"
          :key="download.id"
          :download="download"
        />
      </div>
    </main>
  </div>
</template>