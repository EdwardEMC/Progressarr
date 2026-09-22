<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useRouter } from 'vue-router'

import DownloadCard from '../components/DownloadCard.vue'
import RecentImportListItem from '../components/RecentImportListItem.vue'
import DownloadFilters from '../components/filters/DownloadFilters.vue'

import {
  getDownloads,
  getRecentDownloads,
  type Download,
  type RecentImport,
} from '../api/downloads'

import type { DownloadView } from '../types/download.ts'
import type { DownloadFilterState } from '../interfaces/filter.ts'

const router = useRouter()

const downloads = ref<Download[]>([])
const recentImports = ref<RecentImport[]>([])

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

    const downloadsPromise = getDownloads()
    const recentImportsPromise = getRecentDownloads()

    const [downloadResults, recentImportResults] = await Promise.all([
      downloadsPromise,
      recentImportsPromise.catch(() => []),
    ])

    downloads.value = downloadResults
    recentImports.value = recentImportResults
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

    if (filters.value.status && download.status !== filters.value.status) {
      return false
    }

    if (filters.value.mediaType && download.media_type !== filters.value.mediaType) {
      return false
    }

    if (filters.value.protocol && download.protocol !== filters.value.protocol) {
      return false
    }

    if (filters.value.downloadClient && download.download_client !== filters.value.downloadClient) {
      return false
    }

    if (filters.value.indexer && download.indexer !== filters.value.indexer) {
      return false
    }

    if (filters.value.requestedBy && download.requested_by_username !== filters.value.requestedBy) {
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
        comparison = (a.download_client ?? '').localeCompare(b.download_client ?? '')
        break

      case 'indexer':
        comparison = (a.indexer ?? '').localeCompare(b.indexer ?? '')
        break

      case 'requested_by':
        comparison = (a.requested_by_username ?? '').localeCompare(b.requested_by_username ?? '')
        break
    }

    return comparison * direction
  })

  return result
})

const activeDownloads = computed(() => {
  return filteredDownloads.value.filter(
    (download) => download.status === 'downloading' || download.status === 'import_pending',
  )
})

const completedDownloads = computed(() => {
  return filteredDownloads.value.filter((download) => download.status === 'completed')
})

const displayedRecentImports = computed(() => {
  return recentImports.value.slice(0, 6)
})

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
  <!-- Page heading -->
  <section class="mb-10">
    <div class="flex items-end justify-between gap-6">
      <div>
        <p class="mb-2 text-sm font-medium uppercase tracking-widest text-[#00a4dc]">
          Media server
        </p>

        <h2 class="text-3xl font-semibold tracking-tight text-zinc-900 dark:text-white sm:text-4xl">
          Downloads
        </h2>

        <p class="mt-2 max-w-2xl text-sm text-zinc-500">
          Track movies and episodes as they move through your download and import pipeline.
        </p>
      </div>

      <!-- View switcher -->
      <div
        class="flex shrink-0 items-center rounded-lg border border-zinc-200 bg-white p-1 shadow-sm dark:border-white/8 dark:bg-[#181818]"
      >
        <!-- Card -->
        <button
          type="button"
          title="Card view"
          aria-label="Card view"
          class="rounded-md p-2 transition"
          :class="
            downloadView === 'card'
              ? 'bg-zinc-200 text-zinc-900 shadow-sm dark:bg-white/10 dark:text-white'
              : 'text-zinc-500 hover:bg-zinc-100 hover:text-zinc-800 dark:hover:bg-white/5 dark:hover:text-zinc-300'
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
              ? 'bg-zinc-200 text-zinc-900 shadow-sm dark:bg-white/10 dark:text-white'
              : 'text-zinc-500 hover:bg-zinc-100 hover:text-zinc-800 dark:hover:bg-white/5 dark:hover:text-zinc-300'
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
              ? 'bg-zinc-200 text-zinc-900 shadow-sm dark:bg-white/10 dark:text-white'
              : 'text-zinc-500 hover:bg-zinc-100 hover:text-zinc-800 dark:hover:bg-white/5 dark:hover:text-zinc-300'
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
  <DownloadFilters v-model="filters" :downloads="downloads" />

  <!-- Loading -->
  <div v-if="loading" class="flex min-h-64 items-center justify-center">
    <div class="text-center">
      <div
        class="mx-auto mb-4 h-8 w-8 animate-spin rounded-full border-2 border-zinc-300 border-t-[#00a4dc] dark:border-zinc-700"
      ></div>

      <p class="text-sm text-zinc-500">Loading downloads...</p>
    </div>
  </div>

  <!-- Error -->
  <div
    v-else-if="error"
    class="rounded-xl border border-red-200 bg-red-50 p-6 dark:border-red-500/20 dark:bg-red-500/5"
  >
    <h3 class="font-medium text-red-700 dark:text-red-300">Unable to connect</h3>

    <p class="mt-2 text-sm text-red-600/80 dark:text-red-400/80">
      {{ error }}
    </p>

    <button
      type="button"
      class="mt-4 rounded-lg bg-red-500/10 px-4 py-2 text-sm text-red-700 transition hover:bg-red-500/20 dark:text-red-300"
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
          <h3 class="text-xl font-medium text-zinc-900 dark:text-white">In progress</h3>

          <p class="mt-1 text-sm text-zinc-500">
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

      <div
        v-else
        class="rounded-xl border border-zinc-200 bg-white px-6 py-12 text-center dark:border-white/6 dark:bg-[#181818]"
      >
        <div
          class="rounded-xl border border-dashed border-zinc-300 bg-zinc-50 px-6 py-12 text-center dark:border-zinc-800 dark:bg-zinc-900/50"
        >
          <svg
            class="mx-auto mb-4 h-10 w-10 text-zinc-400 dark:text-zinc-600"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.5"
          >
            <path d="M3 12h18" />
            <path d="M12 3v18" />
          </svg>

          <h3 class="text-sm font-medium text-zinc-800 dark:text-zinc-300">
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
        <h3 class="text-xl font-medium text-zinc-900 dark:text-white">Recently completed</h3>

        <p class="mt-1 text-sm text-zinc-500">Recently finished downloads</p>
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

    <!-- Recent imports -->
    <section v-if="displayedRecentImports.length" class="mt-12">
      <div class="mb-5 flex items-end justify-between gap-4">
        <div>
          <h3 class="text-xl font-medium text-zinc-900 dark:text-white">Recent imports</h3>

          <p class="mt-1 text-sm text-zinc-500">Recently added to your media library</p>
        </div>

        <button
          type="button"
          class="group flex cursor-pointer items-center gap-1.5 text-sm text-zinc-500 transition hover:text-zinc-900 dark:hover:text-white"
          @click="router.push('/history')"
        >
          View all

          <svg
            viewBox="0 0 24 24"
            fill="none"
            class="h-4 w-4 transition-transform group-hover:translate-x-0.5"
          >
            <path
              d="M9 18L15 12L9 6"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </button>
      </div>

      <div
        class="rounded-xl border border-zinc-200 bg-white px-4 dark:border-white/6 dark:bg-[#181818] sm:px-5"
      >
        <RecentImportListItem
          v-for="importItem in displayedRecentImports"
          :key="importItem.id"
          :import-item="importItem"
        />
      </div>
    </section>
  </template>
</template>
