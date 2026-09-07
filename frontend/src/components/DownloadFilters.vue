<script setup lang="ts">
import { computed, ref } from 'vue'
import type { Download } from '../api/downloads'
import type { DownloadFilterState } from '../interfaces/filter';

const props = defineProps<{
  downloads: Download[]
  modelValue: DownloadFilterState
}>()

const emit = defineEmits<{
  'update:modelValue': [value: DownloadFilterState]
}>()

const filtersExpanded = ref(false)

const filters = computed({
  get: () => props.modelValue,
  set: (value: DownloadFilterState) => {
    emit('update:modelValue', value)
  },
})

const statuses = computed(() => {
  return uniqueValues(props.downloads.map((download) => download.status))
})

const mediaTypes = computed(() => {
  return uniqueValues(props.downloads.map((download) => download.media_type))
})

const protocols = computed(() => {
  return uniqueValues(props.downloads.map((download) => download.protocol))
})

const downloadClients = computed(() => {
  return uniqueValues(
    props.downloads.map((download) => download.download_client),
  )
})

const indexers = computed(() => {
  return uniqueValues(props.downloads.map((download) => download.indexer))
})

const requestedByUsers = computed(() => {
  return uniqueValues(
    props.downloads.map((download) => download.requested_by_username),
  )
})

const activeFilterCount = computed(() => {
  let count = 0

  if (filters.value.search.trim()) count++
  if (filters.value.status) count++
  if (filters.value.mediaType) count++
  if (filters.value.protocol) count++
  if (filters.value.downloadClient) count++
  if (filters.value.indexer) count++
  if (filters.value.requestedBy) count++
  if (filters.value.progress) count++

  return count
})

function uniqueValues(values: Array<string | null | undefined>): string[] {
  return [...new Set(values.filter((value): value is string => Boolean(value)))]
    .sort((a, b) => a.localeCompare(b))
}

function humanize(value: string): string {
  return value
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (character) => character.toUpperCase())
}

function toggleFilters() {
  filtersExpanded.value = !filtersExpanded.value
}

function clearFilters() {
  emit('update:modelValue', {
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
}

function toggleSortDirection() {
  emit('update:modelValue', {
    ...filters.value,
    sortDirection:
      filters.value.sortDirection === 'asc' ? 'desc' : 'asc',
  })
}
</script>

<template>
  <div class="mb-8 rounded-xl border border-zinc-800 bg-zinc-900 shadow-xl">
    <!-- Search / filter toggle -->
    <div class="p-4">
      <div class="flex items-center gap-3">
        <!-- Search -->
        <div class="relative flex-1">
          <svg
            class="pointer-events-none absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-zinc-500"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <circle
              cx="11"
              cy="11"
              r="7"
            />
            <path d="m20 20-4-4" />
          </svg>

          <input
            v-model="filters.search"
            type="search"
            placeholder="Search downloads by title..."
            class="w-full rounded-lg border border-zinc-700 bg-zinc-950 py-2.5 pl-10 pr-4 text-sm text-white placeholder-zinc-500 outline-none transition focus:border-zinc-500 focus:ring-1 focus:ring-zinc-500"
          />
        </div>

        <!-- Active filter count -->
        <span
          v-if="activeFilterCount"
          class="hidden shrink-0 rounded-full border border-purple-500/30 bg-purple-500/10 px-3 py-1 text-xs font-medium text-purple-300 sm:block"
        >
          {{ activeFilterCount }}
          {{ activeFilterCount === 1 ? 'filter' : 'filters' }}
        </span>

        <!-- Clear filters -->
        <button
          v-if="activeFilterCount"
          type="button"
          class="hidden shrink-0 text-sm text-zinc-400 transition hover:text-white sm:block"
          @click="clearFilters"
        >
          Clear
        </button>

        <!-- Filter toggle -->
        <button
          type="button"
          :aria-expanded="filtersExpanded"
          aria-label="Toggle filters"
          :title="filtersExpanded ? 'Hide filters' : 'Show filters'"
          class="relative flex h-11 w-11 shrink-0 items-center justify-center rounded-lg border transition"
          :class="
            filtersExpanded || activeFilterCount
              ? 'border-purple-500/50 bg-purple-500/10 text-purple-300'
              : 'border-zinc-700 bg-zinc-950 text-zinc-400 hover:border-zinc-600 hover:text-white'
          "
          @click="toggleFilters"
        >
          <svg
            class="h-5 w-5"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path d="M4 6h16" />
            <path d="M7 12h10" />
            <path d="M10 18h4" />
          </svg>

          <!-- Active indicator -->
          <span
            v-if="activeFilterCount"
            class="absolute -right-1 -top-1 flex h-4 min-w-4 items-center justify-center rounded-full bg-purple-500 px-1 text-[10px] font-bold text-white"
          >
            {{ activeFilterCount }}
          </span>
        </button>
      </div>
    </div>

    <!-- Advanced filters -->
    <div
      v-if="filtersExpanded"
      class="border-t border-zinc-800 p-4"
    >
      <div class="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-4">
        <!-- Status -->
        <label class="block">
          <span
            class="mb-1.5 block text-xs font-medium uppercase tracking-wide text-zinc-500"
          >
            Status
          </span>

          <select
            v-model="filters.status"
            class="w-full rounded-lg border border-zinc-700 bg-zinc-950 px-3 py-2.5 text-sm text-white outline-none transition focus:border-zinc-500 focus:ring-1 focus:ring-zinc-500"
          >
            <option value="">
              All statuses
            </option>

            <option
              v-for="status in statuses"
              :key="status"
              :value="status"
            >
              {{ humanize(status) }}
            </option>
          </select>
        </label>

        <!-- Media type -->
        <label class="block">
          <span
            class="mb-1.5 block text-xs font-medium uppercase tracking-wide text-zinc-500"
          >
            Media type
          </span>

          <select
            v-model="filters.mediaType"
            class="w-full rounded-lg border border-zinc-700 bg-zinc-950 px-3 py-2.5 text-sm text-white outline-none transition focus:border-zinc-500 focus:ring-1 focus:ring-zinc-500"
          >
            <option value="">
              All media
            </option>

            <option
              v-for="mediaType in mediaTypes"
              :key="mediaType"
              :value="mediaType"
            >
              {{ humanize(mediaType) }}
            </option>
          </select>
        </label>

        <!-- Protocol -->
        <label class="block">
          <span
            class="mb-1.5 block text-xs font-medium uppercase tracking-wide text-zinc-500"
          >
            Protocol
          </span>

          <select
            v-model="filters.protocol"
            class="w-full rounded-lg border border-zinc-700 bg-zinc-950 px-3 py-2.5 text-sm text-white outline-none transition focus:border-zinc-500 focus:ring-1 focus:ring-zinc-500"
          >
            <option value="">
              All protocols
            </option>

            <option
              v-for="protocol in protocols"
              :key="protocol"
              :value="protocol"
            >
              {{ humanize(protocol) }}
            </option>
          </select>
        </label>

        <!-- Progress -->
        <label class="block">
          <span
            class="mb-1.5 block text-xs font-medium uppercase tracking-wide text-zinc-500"
          >
            Progress
          </span>

          <select
            v-model="filters.progress"
            class="w-full rounded-lg border border-zinc-700 bg-zinc-950 px-3 py-2.5 text-sm text-white outline-none transition focus:border-zinc-500 focus:ring-1 focus:ring-zinc-500"
          >
            <option value="">
              Any progress
            </option>

            <option value="0-25">
              0–25%
            </option>

            <option value="25-50">
              25–50%
            </option>

            <option value="50-75">
              50–75%
            </option>

            <option value="75-99">
              75–99%
            </option>

            <option value="100">
              100%
            </option>
          </select>
        </label>

        <!-- Download client -->
        <label class="block">
          <span
            class="mb-1.5 block text-xs font-medium uppercase tracking-wide text-zinc-500"
          >
            Download client
          </span>

          <select
            v-model="filters.downloadClient"
            class="w-full rounded-lg border border-zinc-700 bg-zinc-950 px-3 py-2.5 text-sm text-white outline-none transition focus:border-zinc-500 focus:ring-1 focus:ring-zinc-500"
          >
            <option value="">
              All clients
            </option>

            <option
              v-for="client in downloadClients"
              :key="client"
              :value="client"
            >
              {{ client }}
            </option>
          </select>
        </label>

        <!-- Indexer -->
        <label class="block">
          <span
            class="mb-1.5 block text-xs font-medium uppercase tracking-wide text-zinc-500"
          >
            Indexer
          </span>

          <select
            v-model="filters.indexer"
            class="w-full rounded-lg border border-zinc-700 bg-zinc-950 px-3 py-2.5 text-sm text-white outline-none transition focus:border-zinc-500 focus:ring-1 focus:ring-zinc-500"
          >
            <option value="">
              All indexers
            </option>

            <option
              v-for="indexer in indexers"
              :key="indexer"
              :value="indexer"
            >
              {{ indexer }}
            </option>
          </select>
        </label>

        <!-- Requested by -->
        <label class="block">
          <span
            class="mb-1.5 block text-xs font-medium uppercase tracking-wide text-zinc-500"
          >
            Requested by
          </span>

          <select
            v-model="filters.requestedBy"
            class="w-full rounded-lg border border-zinc-700 bg-zinc-950 px-3 py-2.5 text-sm text-white outline-none transition focus:border-zinc-500 focus:ring-1 focus:ring-zinc-500"
          >
            <option value="">
              Everyone
            </option>

            <option
              v-for="user in requestedByUsers"
              :key="user"
              :value="user"
            >
              {{ user }}
            </option>
          </select>
        </label>

        <!-- Sort -->
        <label class="block">
          <span
            class="mb-1.5 block text-xs font-medium uppercase tracking-wide text-zinc-500"
          >
            Sort by
          </span>

          <div class="flex gap-2">
            <select
              v-model="filters.sortBy"
              class="min-w-0 flex-1 rounded-lg border border-zinc-700 bg-zinc-950 px-3 py-2.5 text-sm text-white outline-none transition focus:border-zinc-500 focus:ring-1 focus:ring-zinc-500"
            >
              <option value="title">
                Title
              </option>

              <option value="status">
                Status
              </option>

              <option value="progress">
                Progress
              </option>

              <option value="size">
                Size
              </option>

              <option value="size_remaining">
                Remaining size
              </option>

              <option value="media_type">
                Media type
              </option>

              <option value="download_client">
                Download client
              </option>

              <option value="indexer">
                Indexer
              </option>

              <option value="requested_by">
                Requested by
              </option>
            </select>

            <button
              type="button"
              :title="
                filters.sortDirection === 'asc'
                  ? 'Ascending'
                  : 'Descending'
              "
              class="flex w-11 shrink-0 items-center justify-center rounded-lg border border-zinc-700 bg-zinc-950 text-zinc-400 transition hover:border-zinc-600 hover:text-white"
              @click="toggleSortDirection"
            >
              <!-- Ascending -->
              <svg
                v-if="filters.sortDirection === 'asc'"
                class="h-5 w-5"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <path d="m5 12 7-7 7 7" />
                <path d="M12 19V5" />
              </svg>

              <!-- Descending -->
              <svg
                v-else
                class="h-5 w-5"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <path d="m19 12-7 7-7-7" />
                <path d="M12 5v14" />
              </svg>
            </button>
          </div>
        </label>
      </div>

      <!-- Mobile clear button -->
      <div
        v-if="activeFilterCount"
        class="mt-4 flex items-center justify-between border-t border-zinc-800 pt-4 sm:hidden"
      >
        <span class="text-xs text-zinc-500">
          {{ activeFilterCount }}
          {{ activeFilterCount === 1 ? 'filter' : 'filters' }} active
        </span>

        <button
          type="button"
          class="text-sm text-zinc-400 transition hover:text-white"
          @click="clearFilters"
        >
          Clear filters
        </button>
      </div>
    </div>
  </div>
</template>