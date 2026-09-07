<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'

import DownloadCard from '../components/DownloadCard.vue'
import DownloadFilters from '../components/DownloadFilters.vue'
import { getDownloads, type Download } from '../api/downloads'
import type { DownloadView } from '../types/download.ts'
import type { DownloadFilterState } from '../interfaces/filter.ts'

const downloads = ref<Download[]>([])
const loading = ref(true)
const refreshing = ref(false)
const error = ref<string | null>(null)
const lastUpdated = ref<Date | null>(null)

const downloadView = ref<DownloadView>(
  (localStorage.getItem('progressarr-download-view') as DownloadView) || 'card',
)

const filters = ref<DownloadFilterState>({
  search: '',
  status: '',
  mediaType: '',
  protocol: '',
  downloadClient: '',
  indexer: '',
  requestedBy: '',
  progress: '',
  sortBy: 'title',
  sortDirection: 'asc',
})

function setDownloadView(view: DownloadView): void {
  downloadView.value = view
  localStorage.setItem('progressarr-download-view', view)
}

let pollingInterval: ReturnType<typeof setInterval> | undefined

async function loadDownloads(showLoading = true, showRefreshing = false): Promise<void> {
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
    error.value = err instanceof Error ? err.message : 'Unable to load downloads.'
  } finally {
    loading.value = false
    refreshing.value = false
  }
}

const filteredDownloads = computed(() => {
  const result = downloads.value.filter((download) => {
    const search = filters.value.search.trim().toLowerCase()

    // Search is intentionally title-only.
    if (search && !download.title.toLowerCase().includes(search)) {
      return false
    }

    if (
      filters.value.status &&
      download.status !== filters.value.status
    ) {
      return false
    }

    if (
      filters.value.mediaType &&
      download.media_type !== filters.value.mediaType
    ) {
      return false
    }

    if (
      filters.value.protocol &&
      download.protocol !== filters.value.protocol
    ) {
      return false
    }

    if (
      filters.value.downloadClient &&
      download.download_client !== filters.value.downloadClient
    ) {
      return false
    }

    if (
      filters.value.indexer &&
      download.indexer !== filters.value.indexer
    ) {
      return false
    }

    if (
      filters.value.requestedBy &&
      download.requested_by_username !== filters.value.requestedBy
    ) {
      return false
    }

    if (filters.value.progress) {
      const progress = download.progress

      switch (filters.value.progress) {
        case '0-25':
          if (progress > 25) return false
          break

        case '25-50':
          if (progress <= 25 || progress > 50) return false
          break

        case '50-75':
          if (progress <= 50 || progress > 75) return false
          break

        case '75-99':
          if (progress <= 75 || progress >= 100) return false
          break

        case '100':
          if (progress < 100) return false
          break
      }
    }

    return true
  })

  const direction = filters.value.sortDirection === 'asc' ? 1 : -1

  result.sort((a, b) => {
    let comparison = 0

    switch (filters.value.sortBy) {
      case 'title':
        comparison = a.title.localeCompare(b.title)
        break

      case 'status':
        comparison = a.status.localeCompare(b.status)
        break

      case 'progress':
        comparison = a.progress - b.progress
        break

      case 'size':
        comparison = a.size - b.size
        break

      case 'size_remaining':
        comparison = a.size_remaining - b.size_remaining
        break

      case 'media_type':
        comparison = a.media_type.localeCompare(b.media_type)
        break

      case 'download_client':
        comparison = (a.download_client ?? '').localeCompare(
          b.download_client ?? '',
        )
        break

      case 'indexer':
        comparison = (a.indexer ?? '').localeCompare(b.indexer ?? '')
        break

      case 'requested_by':
        comparison = (
          a.requested_by_username ?? ''
        ).localeCompare(b.requested_by_username ?? '')
        break
    }

    return comparison * direction
  })

  return result
})

const activeDownloads = computed(() => {
  return filteredDownloads.value.filter(
    (download) =>
      download.status === 'downloading' ||
      download.status === 'import_pending',
  )
})

const completedDownloads = computed(() => {
  return filteredDownloads.value.filter(
    (download) => download.status === 'completed',
  )
})

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
    <header class="sticky top-0 z-50 border-b border-white/6 bg-[#101010]/90 backdrop-blur-xl">
      <div class="mx-auto flex h-20 max-w-7xl items-center justify-between px-6 lg:px-8">
        <div class="flex items-center gap-4">
          <!-- Progressarr mark -->
          <div
            class="flex h-10 w-10 items-center justify-center rounded-xl bg-linear-to-br from-[#aa5cc3] to-[#00a4dc] shadow-lg shadow-[#00a4dc]/10"
          >
            <svg viewBox="0 0 24 24" fill="none" class="h-6 w-6 text-white">
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
            <h1 class="text-lg font-semibold tracking-tight">Progressarr</h1>

            <p class="hidden text-xs text-zinc-500 sm:block">Download progress</p>
          </div>
        </div>

        <div class="flex items-center gap-4">
          <span v-if="lastUpdated" class="hidden text-xs text-zinc-600 sm:block">
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
        <div class="flex items-end justify-between gap-6">
          <div>
            <p class="mb-2 text-sm font-medium uppercase tracking-widest text-[#00a4dc]">
              Media server
            </p>

            <h2 class="text-3xl font-semibold tracking-tight sm:text-4xl">Downloads</h2>

            <p class="mt-2 max-w-2xl text-sm text-zinc-500">
              Track movies and episodes as they move through your download and import pipeline.
            </p>
          </div>

          <!-- View switcher -->
          <div class="flex shrink-0 items-center rounded-lg border border-white/8 bg-[#181818] p-1">
            <!-- Card -->
            <button
              type="button"
              title="Card view"
              aria-label="Card view"
              class="rounded-md p-2 transition"
              :class="
                downloadView === 'card'
                  ? 'bg-white/10 text-white shadow-sm'
                  : 'text-zinc-500 hover:bg-white/5 hover:text-zinc-300'
              "
              @click="setDownloadView('card')"
            >
              <svg viewBox="0 0 24 24" fill="none" class="h-4 w-4">
                <rect
                  x="3"
                  y="4"
                  width="18"
                  height="16"
                  rx="2"
                  stroke="currentColor"
                  stroke-width="1.8"
                />
                <path d="M3 10H21M9 10V20" stroke="currentColor" stroke-width="1.8" />
              </svg>
            </button>

            <!-- Grid -->
            <button
              type="button"
              title="Grid view"
              aria-label="Grid view"
              class="rounded-md p-2 transition"
              :class="
                downloadView === 'grid'
                  ? 'bg-white/10 text-white shadow-sm'
                  : 'text-zinc-500 hover:bg-white/5 hover:text-zinc-300'
              "
              @click="setDownloadView('grid')"
            >
              <svg viewBox="0 0 24 24" fill="none" class="h-4 w-4">
                <rect
                  x="3"
                  y="3"
                  width="7"
                  height="7"
                  rx="1"
                  stroke="currentColor"
                  stroke-width="1.8"
                />
                <rect
                  x="14"
                  y="3"
                  width="7"
                  height="7"
                  rx="1"
                  stroke="currentColor"
                  stroke-width="1.8"
                />
                <rect
                  x="3"
                  y="14"
                  width="7"
                  height="7"
                  rx="1"
                  stroke="currentColor"
                  stroke-width="1.8"
                />
                <rect
                  x="14"
                  y="14"
                  width="7"
                  height="7"
                  rx="1"
                  stroke="currentColor"
                  stroke-width="1.8"
                />
              </svg>
            </button>

            <!-- Row -->
            <button
              type="button"
              title="Row view"
              aria-label="Row view"
              class="rounded-md p-2 transition"
              :class="
                downloadView === 'row'
                  ? 'bg-white/10 text-white shadow-sm'
                  : 'text-zinc-500 hover:bg-white/5 hover:text-zinc-300'
              "
              @click="setDownloadView('row')"
            >
              <svg viewBox="0 0 24 24" fill="none" class="h-4 w-4">
                <rect
                  x="3"
                  y="4"
                  width="18"
                  height="4"
                  rx="1"
                  stroke="currentColor"
                  stroke-width="1.8"
                />
                <rect
                  x="3"
                  y="10"
                  width="18"
                  height="4"
                  rx="1"
                  stroke="currentColor"
                  stroke-width="1.8"
                />
                <rect
                  x="3"
                  y="16"
                  width="18"
                  height="4"
                  rx="1"
                  stroke="currentColor"
                  stroke-width="1.8"
                />
              </svg>
            </button>
          </div>
        </div>
      </section>

      <!-- Filtering and Sorting -->
      <DownloadFilters
        v-model="filters"
        :downloads="downloads"
      />

      <!-- Loading -->
      <div v-if="loading" class="flex min-h-64 items-center justify-center">
        <div class="text-center">
          <div
            class="mx-auto mb-4 h-8 w-8 animate-spin rounded-full border-2 border-zinc-700 border-t-[#00a4dc]"
          />

          <p class="text-sm text-zinc-500">Loading downloads...</p>
        </div>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="rounded-xl border border-red-500/20 bg-red-500/5 p-6">
        <h3 class="font-medium text-red-300">Unable to connect</h3>

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
              <h3 class="text-xl font-medium">In progress</h3>

              <p class="mt-1 text-sm text-zinc-600">
                {{ activeDownloads.length }}
                {{ activeDownloads.length === 1 ? 'item' : 'items' }}
              </p>
            </div>
          </div>

          <div
            v-if="activeDownloads.length"
            :class="{
              'grid gap-6 lg:grid-cols-2': downloadView === 'card',

              'grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5':
                downloadView === 'grid',

              'flex flex-col gap-3': downloadView === 'row',
            }"
          >
            <DownloadCard
              v-for="download in activeDownloads"
              :key="download.id"
              :download="download"
              :view="downloadView"
            />
          </div>

          <div v-else class="rounded-xl border border-white/6 bg-[#181818] px-6 py-12 text-center">
            <div
              v-if="activeDownloads.length === 0"
              class="rounded-xl border border-dashed border-zinc-800 bg-zinc-900/50 px-6 py-12 text-center"
            >
              <svg
                class="mx-auto mb-4 h-10 w-10 text-zinc-600"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="1.5"
              >
                <path d="M3 12h18" />
                <path d="M12 3v18" />
              </svg>

              <h3 class="text-sm font-medium text-zinc-300">
                {{
                  filteredDownloads.length === 0 && downloads.length > 0
                    ? 'No downloads match your filters'
                    : 'Nothing downloading'
                }}
              </h3>

              <p class="mt-1 text-sm text-zinc-500">
                {{
                  filteredDownloads.length === 0 && downloads.length > 0
                    ? 'Try adjusting your search or filters.'
                    : 'There are currently no downloads in progress.'
                }}
              </p>
            </div>
          </div>
        </section>

        <!-- Completed -->
        <section v-if="completedDownloads.length" class="mt-12">
          <div class="mb-5">
            <h3 class="text-xl font-medium">Recently completed</h3>

            <p class="mt-1 text-sm text-zinc-600">Recently finished downloads</p>
          </div>

          <div
            :class="{
              'grid gap-6 lg:grid-cols-2': downloadView === 'card',

              'grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5':
                downloadView === 'grid',

              'flex flex-col gap-3': downloadView === 'row',
            }"
          >
            <DownloadCard
              v-for="download in completedDownloads"
              :key="download.id"
              :download="download"
              :view="downloadView"
            />
          </div>
        </section>
      </template>
    </main>
  </div>
</template>
