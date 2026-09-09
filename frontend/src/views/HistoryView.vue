<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from 'vue'

import RecentImportFilters from '../components/filters/RecentImportFilters.vue'
import RecentImportListItem from '../components/RecentImportListItem.vue'

import {
  getImportHistory,
  type RecentImport,
} from '../api/downloads'
import type { RecentImportFilterState } from '../interfaces/filter'

const imports = ref<RecentImport[]>([])

const filters = ref<RecentImportFilterState>({
  search: '',
  mediaType: '',
  source: '',
  quality: '',
  season: null,
  fromDate: '',
  toDate: '',
  sort: 'imported_at',
  sortDirection: 'desc',
})

const page = ref(1)
const pageSize = ref(25)
const hasMore = ref(false)

const loading = ref(true)
const refreshing = ref(false)
const error = ref<string | null>(null)

let historyRequestId = 0

async function loadHistory(showLoading = true): Promise<void> {
  const requestId = ++historyRequestId

  try {
    if (showLoading) {
      loading.value = true
    } else {
      refreshing.value = true
    }

    error.value = null

    const response = await getImportHistory(
      filters.value,
      page.value,
      pageSize.value,
    )

    // Ignore an older request if a newer one has started.
    if (requestId !== historyRequestId) {
      return
    }

    imports.value = response.items
    hasMore.value = response.has_more
  } catch (err) {
    if (requestId !== historyRequestId) {
      return
    }

    error.value =
      err instanceof Error
        ? err.message
        : 'Unable to load import history.'
  } finally {
    if (requestId === historyRequestId) {
      loading.value = false
      refreshing.value = false
    }
  }
}

async function nextPage(): Promise<void> {
  if (
    !hasMore.value ||
    loading.value ||
    refreshing.value
  ) {
    return
  }

  page.value += 1

  await loadHistory(false)
}

async function previousPage(): Promise<void> {
  if (
    page.value <= 1 ||
    loading.value ||
    refreshing.value
  ) {
    return
  }

  page.value -= 1

  await loadHistory(false)
}

let filterTimeout: ReturnType<typeof setTimeout> | null = null

const debouncedFilterKeys = new Set([
  'search',
  'quality',
  'season',
])

function scheduleHistoryReload(): void {
  if (filterTimeout) {
    clearTimeout(filterTimeout)
  }

  filterTimeout = setTimeout(() => {
    filterTimeout = null
    page.value = 1
    void loadHistory(true)
  }, 300)
}

function loadHistoryImmediately(): void {
  if (filterTimeout) {
    clearTimeout(filterTimeout)
    filterTimeout = null
  }

  page.value = 1
  void loadHistory(true)
}

watch(
  filters,
  (newFilters, oldFilters) => {
    const changedKeys = Object.keys(newFilters).filter(
      (key) =>
        newFilters[key as keyof RecentImportFilterState] !==
        oldFilters[key as keyof RecentImportFilterState],
    )

    if (changedKeys.length === 0) {
      return
    }

    const hasImmediateChange = changedKeys.some(
      (key) => !debouncedFilterKeys.has(key),
    )

    if (hasImmediateChange) {
      loadHistoryImmediately()
      return
    }

    scheduleHistoryReload()
  },
)

onMounted(() => {
  loadHistory()
})

onUnmounted(() => {
  if (filterTimeout) {
    clearTimeout(filterTimeout)
  }
})
</script>

<template>
  <main class="mx-auto w-full max-w-7xl px-5 py-8 sm:px-8">
    <!-- Header -->
    <div class="mb-8">
      <div class="flex items-end justify-between gap-4">
        <div>
          <h1 class="text-2xl font-semibold tracking-tight text-white">
            Import history
          </h1>

          <p class="mt-1 text-sm text-zinc-500">
            Recently imported movies and episodes
          </p>
        </div>

        <button
          type="button"
          class="flex items-center gap-2 rounded-lg border border-white/8 bg-white/3 px-3 py-2 text-sm text-zinc-400 transition hover:border-white/12 hover:bg-white/5 hover:text-white disabled:cursor-not-allowed disabled:opacity-50"
          :disabled="loading || refreshing"
          @click="loadHistory(false)"
        >
          <svg
            viewBox="0 0 24 24"
            fill="none"
            class="h-4 w-4"
            :class="{ 'animate-spin': refreshing }"
          >
            <path
              d="M20 11A8.1 8.1 0 0 0 5.3 6.3L3 9"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
              stroke-linejoin="round"
            />

            <path
              d="M3 5V9H7"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
              stroke-linejoin="round"
            />

            <path
              d="M4 13A8.1 8.1 0 0 0 18.7 17.7L21 15"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
              stroke-linejoin="round"
            />

            <path
              d="M21 19V15H17"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>

          Refresh
        </button>
      </div>
    </div>

    <!-- Filters -->
    <RecentImportFilters
        :filters="filters"
        @update:filters="filters = $event"
    />

    <!-- Error -->
    <div
      v-if="error"
      class="mb-6 rounded-xl border border-red-500/15 bg-red-500/5 px-4 py-3 text-sm text-red-400"
    >
      {{ error }}
    </div>

    <!-- Loading -->
    <div
      v-if="loading"
      class="rounded-xl border border-white/6 bg-[#181818] px-5"
    >
      <div
        v-for="index in 8"
        :key="index"
        class="flex items-center gap-4 border-b border-white/5 py-3 last:border-b-0"
      >
        <div
          class="h-14 w-10 animate-pulse rounded-md bg-[#202020]"
        />

        <div class="min-w-0 flex-1">
          <div
            class="h-4 w-48 animate-pulse rounded bg-[#202020]"
          />

          <div
            class="mt-2 h-3 w-64 animate-pulse rounded bg-[#202020]"
          />
        </div>
      </div>
    </div>

    <!-- Results -->
    <template v-else>
      <section
        v-if="imports.length"
        class="rounded-xl border border-white/6 bg-[#181818] px-4 sm:px-5"
      >
        <RecentImportListItem
          v-for="importItem in imports"
          :key="importItem.id"
          :import-item="importItem"
        />
      </section>

      <!-- Empty -->
      <div
        v-else
        class="rounded-xl border border-white/6 bg-[#181818] px-6 py-16 text-center"
      >
        <div
          class="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-white/4 text-zinc-600"
        >
          <svg
            viewBox="0 0 24 24"
            fill="none"
            class="h-6 w-6"
          >
            <path
              d="M4 5.5C4 4.67 4.67 4 5.5 4H18.5C19.33 4 20 4.67 20 5.5V18.5C20 19.33 19.33 20 18.5 20H5.5C4.67 20 4 19.33 4 18.5V5.5Z"
              stroke="currentColor"
              stroke-width="1.5"
            />

            <path
              d="M8 9H16M8 13H13"
              stroke="currentColor"
              stroke-width="1.5"
              stroke-linecap="round"
            />
          </svg>
        </div>

        <h3 class="mt-4 text-sm font-medium text-zinc-300">
          No imports found
        </h3>

        <p class="mt-1 text-sm text-zinc-600">
          Try adjusting your filters or search.
        </p>
      </div>

      <!-- Pagination -->
      <div
        v-if="imports.length || page > 1"
        class="mt-5 flex items-center justify-between"
      >
        <button
          type="button"
          class="flex items-center gap-1.5 rounded-lg px-3 py-2 text-sm text-zinc-500 transition hover:bg-white/4 hover:text-white disabled:cursor-not-allowed disabled:opacity-30"
          :disabled="page <= 1 || refreshing"
          @click="previousPage"
        >
          <svg
            viewBox="0 0 24 24"
            fill="none"
            class="h-4 w-4"
          >
            <path
              d="M15 18L9 12L15 6"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>

          Previous
        </button>

        <span class="text-xs text-zinc-600">
          Page {{ page }}
        </span>

        <button
          type="button"
          class="flex items-center gap-1.5 rounded-lg px-3 py-2 text-sm text-zinc-500 transition hover:bg-white/4 hover:text-white disabled:cursor-not-allowed disabled:opacity-30"
          :disabled="!hasMore || refreshing"
          @click="nextPage"
        >
          Next

          <svg
            viewBox="0 0 24 24"
            fill="none"
            class="h-4 w-4"
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
    </template>
  </main>
</template>