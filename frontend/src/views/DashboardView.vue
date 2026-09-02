<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'

import DownloadCard from '../components/DownloadCard.vue'
import {
  getDownloads,
  type Download,
} from '../api/downloads'

const downloads = ref<Download[]>([])
const loading = ref(true)
const refreshing = ref(false)
const error = ref<string | null>(null)
const lastUpdated = ref<Date | null>(null)

let pollingInterval: ReturnType<typeof setInterval> | undefined

async function loadDownloads(
  showLoading = true,
  showRefreshing = false,
): Promise<void> {
  try {
    if (showLoading) {
      loading.value = true
    }

    if (showRefreshing) {
      refreshing.value = true
    }

    error.value = null
    downloads.value = await getDownloads()
    lastUpdated.value = new Date()
  } catch (err) {
    error.value =
      err instanceof Error
        ? err.message
        : 'Unable to load downloads.'
  } finally {
    loading.value = false
    refreshing.value = false
  }
}

function activeDownloads(): Download[] {
  return downloads.value.filter(
    (download) =>
      download.status === 'downloading' ||
      download.status === 'import_pending',
  )
}

function completedDownloads(): Download[] {
  return downloads.value.filter(
    (download) => download.status === 'completed',
  )
}

function formatUpdated(): string {
  if (!lastUpdated.value) {
    return ''
  }

  return lastUpdated.value.toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit',
  })
}

onMounted(() => {
  loadDownloads()

  pollingInterval = setInterval(() => {
    loadDownloads(false)
  }, 5000)
})

onUnmounted(() => {
  if (pollingInterval) {
    clearInterval(pollingInterval)
  }
})
</script>

<template>
  <div class="min-h-screen bg-[#101010] text-white">
    <!-- Header -->
    <header
      class="sticky top-0 z-50 border-b border-white/6 bg-[#101010]/90 backdrop-blur-xl"
    >
      <div
        class="mx-auto flex h-20 max-w-7xl items-center justify-between px-6 lg:px-8"
      >
        <div class="flex items-center gap-4">
          <!-- Progressarr mark -->
          <div
            class="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-[#aa5cc3] to-[#00a4dc] shadow-lg shadow-[#00a4dc]/10"
          >
            <svg
              viewBox="0 0 24 24"
              fill="none"
              class="h-6 w-6 text-white"
            >
              <path
                d="M5 19V5M5 19H19M9 15L12 11L15 14L20 7"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
          </div>

          <div>
            <h1 class="text-lg font-semibold tracking-tight">
              Progressarr
            </h1>

            <p class="hidden text-xs text-zinc-500 sm:block">
              Download progress
            </p>
          </div>
        </div>

        <div class="flex items-center gap-4">
          <span
            v-if="lastUpdated"
            class="hidden text-xs text-zinc-600 sm:block"
          >
            Updated {{ formatUpdated() }}
          </span>

          <button
            type="button"
            class="flex h-9 w-9 items-center justify-center rounded-lg text-zinc-400 transition hover:bg-white/5 hover:text-white disabled:opacity-50"
            :disabled="refreshing"
            title="Refresh"
            @click="loadDownloads(false, true)"
          >
            <svg
              viewBox="0 0 24 24"
              fill="none"
              class="h-5 w-5"
              :class="{ 'animate-spin': refreshing }"
            >
              <path
                d="M20 11A8.1 8.1 0 0 0 5.4 6.5L4 8M4 8V4M4 8H8M4 13A8.1 8.1 0 0 0 18.6 17.5L20 16M20 16V20M20 16H16"
                stroke="currentColor"
                stroke-width="1.8"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
          </button>
        </div>
      </div>
    </header>

    <main class="mx-auto max-w-7xl px-6 py-10 lg:px-8">
      <!-- Page heading -->
      <section class="mb-10">
        <p
          class="mb-2 text-sm font-medium uppercase tracking-widest text-[#00a4dc]"
        >
          Media server
        </p>

        <h2
          class="text-3xl font-semibold tracking-tight sm:text-4xl"
        >
          Downloads
        </h2>

        <p class="mt-2 max-w-2xl text-sm text-zinc-500">
          Track movies and episodes as they move through your
          download and import pipeline.
        </p>
      </section>

      <!-- Loading -->
      <div
        v-if="loading"
        class="flex min-h-64 items-center justify-center"
      >
        <div class="text-center">
          <div
            class="mx-auto mb-4 h-8 w-8 animate-spin rounded-full border-2 border-zinc-700 border-t-[#00a4dc]"
          />

          <p class="text-sm text-zinc-500">
            Loading downloads...
          </p>
        </div>
      </div>

      <!-- Error -->
      <div
        v-else-if="error"
        class="rounded-xl border border-red-500/20 bg-red-500/5 p-6"
      >
        <h3 class="font-medium text-red-300">
          Unable to connect
        </h3>

        <p class="mt-2 text-sm text-red-400/80">
          {{ error }}
        </p>

        <button
          type="button"
          class="mt-4 rounded-lg bg-red-500/10 px-4 py-2 text-sm text-red-300 transition hover:bg-red-500/20"
          @click="loadDownloads()"
        >
          Try again
        </button>
      </div>

      <template v-else>
        <!-- Active downloads -->
        <section>
          <div class="mb-5 flex items-center justify-between">
            <div>
              <h3 class="text-xl font-medium">
                In progress
              </h3>

              <p class="mt-1 text-sm text-zinc-600">
                {{ activeDownloads().length }}
                {{ activeDownloads().length === 1 ? 'item' : 'items' }}
              </p>
            </div>
          </div>

          <div
            v-if="activeDownloads().length"
            class="grid gap-6 lg:grid-cols-2"
          >
            <DownloadCard
              v-for="download in activeDownloads()"
              :key="download.id"
              :download="download"
            />
          </div>

          <div
            v-else
            class="rounded-xl border border-white/6 bg-[#181818] px-6 py-12 text-center"
          >
            <div
              class="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-white/5"
            >
              <svg
                viewBox="0 0 24 24"
                fill="none"
                class="h-6 w-6 text-zinc-600"
              >
                <path
                  d="M12 3V21M3 12H21"
                  stroke="currentColor"
                  stroke-width="1.5"
                  stroke-linecap="round"
                />
              </svg>
            </div>

            <h3 class="font-medium text-zinc-300">
              Nothing downloading
            </h3>

            <p class="mt-1 text-sm text-zinc-600">
              New requests will appear here.
            </p>
          </div>
        </section>

        <!-- Completed -->
        <section
          v-if="completedDownloads().length"
          class="mt-12"
        >
          <div class="mb-5">
            <h3 class="text-xl font-medium">
              Recently completed
            </h3>

            <p class="mt-1 text-sm text-zinc-600">
              Recently finished downloads
            </p>
          </div>

          <div class="grid gap-4 lg:grid-cols-2">
            <DownloadCard
              v-for="download in completedDownloads()"
              :key="download.id"
              :download="download"
            />
          </div>
        </section>
      </template>
    </main>
  </div>
</template>
