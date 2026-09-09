<script setup lang="ts">
import { computed, ref } from 'vue'

import type { RecentImportFilterState } from '../../interfaces/filter'
import SelectInput from '../inputs/SelectInput.vue';

const props = defineProps<{
  filters: RecentImportFilterState
}>()

const emit = defineEmits<{
  'update:filters': [filters: RecentImportFilterState]
}>()

const filtersExpanded = ref(false)

const hasActiveFilters = computed(() => {
  return (
    props.filters.search.trim() !== '' ||
    props.filters.mediaType !== '' ||
    props.filters.source !== '' ||
    props.filters.quality !== '' ||
    props.filters.season !== null ||
    props.filters.fromDate !== '' ||
    props.filters.toDate !== '' ||
    props.filters.sort !== 'imported_at' ||
    props.filters.sortDirection !== 'desc'
  )
})

const activeFilterCount = computed(() => {
  let count = 0

  if (props.filters.search.trim()) count++
  if (props.filters.mediaType) count++
  if (props.filters.source) count++
  if (props.filters.quality) count++
  if (props.filters.season !== null) count++
  if (props.filters.fromDate) count++
  if (props.filters.toDate) count++
  if (props.filters.sort !== 'imported_at') count++
  if (props.filters.sortDirection !== 'desc') count++

  return count
})

function updateFilter<K extends keyof RecentImportFilterState>(
  key: K,
  value: RecentImportFilterState[K],
): void {
  emit('update:filters', {
    ...props.filters,
    [key]: value,
  })
}

function toggleFilters(): void {
  filtersExpanded.value = !filtersExpanded.value
}

function toggleSortDirection(): void {
  updateFilter(
    'sortDirection',
    props.filters.sortDirection === 'desc'
      ? 'asc'
      : 'desc',
  )
}

function clearFilters(): void {
  emit('update:filters', {
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
            :value="filters.search"
            type="search"
            placeholder="Search imports..."
            class="w-full rounded-lg border border-zinc-700 bg-zinc-950 py-2.5 pl-10 pr-4 text-sm text-white placeholder-zinc-500 outline-none transition focus:border-zinc-500 focus:ring-1 focus:ring-zinc-500"
            @input="
              updateFilter(
                'search',
                ($event.target as HTMLInputElement).value,
              )
            "
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
            filtersExpanded || hasActiveFilters
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
        <!-- Media type -->
        <label class="block">
          <span
            class="mb-1.5 block text-xs font-medium uppercase tracking-wide text-zinc-500"
          >
            Media type
          </span>

          <SelectInput
            :model-value="filters.mediaType"
            @update:model-value="updateFilter('mediaType', $event)"
          >
            <option value="">
              All media
            </option>

            <option value="movie">
              Movies
            </option>

            <option value="episode">
              Episodes
            </option>
          </SelectInput>
        </label>

        <!-- Source -->
        <label class="block">
          <span
            class="mb-1.5 block text-xs font-medium uppercase tracking-wide text-zinc-500"
          >
            Source
          </span>

          <SelectInput
            :model-value="filters.source"
            @update:model-value="updateFilter('source', $event)"
          >
            <option value="">
              All sources
            </option>

            <option value="radarr">
              Radarr
            </option>

            <option value="sonarr">
              Sonarr
            </option>
          </SelectInput>
        </label>

        <!-- Quality -->
        <label class="block">
          <span
            class="mb-1.5 block text-xs font-medium uppercase tracking-wide text-zinc-500"
          >
            Quality
          </span>

          <input
            :value="filters.quality"
            type="text"
            placeholder="All qualities"
            class="w-full rounded-lg border border-zinc-700 bg-zinc-950 px-3 py-2.5 text-sm text-white placeholder-zinc-500 outline-none transition focus:border-zinc-500 focus:ring-1 focus:ring-zinc-500"
            @input="
              updateFilter(
                'quality',
                ($event.target as HTMLInputElement).value,
              )
            "
          />
        </label>

        <!-- Season -->
        <label class="block">
          <span
            class="mb-1.5 block text-xs font-medium uppercase tracking-wide text-zinc-500"
          >
            Season
          </span>

          <input
            :value="filters.season ?? ''"
            type="number"
            min="0"
            placeholder="All seasons"
            class="w-full rounded-lg border border-zinc-700 bg-zinc-950 px-3 py-2.5 text-sm text-white placeholder-zinc-500 outline-none transition focus:border-zinc-500 focus:ring-1 focus:ring-zinc-500"
            @input="
              updateFilter(
                'season',
                ($event.target as HTMLInputElement).value === ''
                  ? null
                  : Number(($event.target as HTMLInputElement).value),
              )
            "
          />
        </label>

        <!-- From date -->
        <label class="block">
          <span
            class="mb-1.5 block text-xs font-medium uppercase tracking-wide text-zinc-500"
          >
            From
          </span>

          <input
            :value="filters.fromDate"
            type="datetime-local"
            class="w-full rounded-lg border border-zinc-700 bg-zinc-950 px-3 py-2.5 text-sm text-white outline-none transition [color-scheme:dark] focus:border-zinc-500 focus:ring-1 focus:ring-zinc-500"
            @input="
              updateFilter(
                'fromDate',
                ($event.target as HTMLInputElement).value,
              )
            "
          />
        </label>

        <!-- To date -->
        <label class="block">
          <span
            class="mb-1.5 block text-xs font-medium uppercase tracking-wide text-zinc-500"
          >
            To
          </span>

          <input
            :value="filters.toDate"
            type="datetime-local"
            class="w-full rounded-lg border border-zinc-700 bg-zinc-950 px-3 py-2.5 text-sm text-white outline-none transition [color-scheme:dark] focus:border-zinc-500 focus:ring-1 focus:ring-zinc-500"
            @input="
              updateFilter(
                'toDate',
                ($event.target as HTMLInputElement).value,
              )
            "
          />
        </label>

        <!-- Sort -->
        <label class="block">
          <span
            class="mb-1.5 block text-xs font-medium uppercase tracking-wide text-zinc-500"
          >
            Sort by
          </span>

          <div class="flex gap-2">
            <SelectInput
              :model-value="filters.sort"
              class="min-w-0 flex-1"
              @update:model-value="
                updateFilter(
                  'sort',
                  $event as RecentImportFilterState['sort'],
                )
              "
            >
              <option value="imported_at">
                Import date
              </option>

              <option value="title">
                Title
              </option>

              <option value="size">
                Size
              </option>

              <option value="quality">
                Quality
              </option>
            </SelectInput>

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