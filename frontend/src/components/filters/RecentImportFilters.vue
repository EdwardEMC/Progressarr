<script setup lang="ts">
import { computed, ref } from 'vue'

import type { RecentImportFilterState } from '../../interfaces/filter'

const props = defineProps<{
  filters: RecentImportFilterState
}>()

const emit = defineEmits<{
  'update:filters': [filters: RecentImportFilterState]
}>()

const expanded = ref(false)

const hasActiveFilters = computed(() => {
  return (
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

function updateFilter<K extends keyof RecentImportFilterState>(
  key: K,
  value: RecentImportFilterState[K],
): void {
  emit('update:filters', {
    ...props.filters,
    [key]: value,
  })
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
  <section class="mb-6">
    <!-- Search bar -->
    <div class="flex items-center gap-2">
      <div class="relative min-w-0 flex-1">
        <svg
          viewBox="0 0 24 24"
          fill="none"
          class="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-zinc-600"
        >
          <circle
            cx="11"
            cy="11"
            r="7"
            stroke="currentColor"
            stroke-width="1.7"
          />

          <path
            d="M16.5 16.5L21 21"
            stroke="currentColor"
            stroke-width="1.7"
            stroke-linecap="round"
          />
        </svg>

        <input
          :value="filters.search"
          type="search"
          placeholder="Search imports..."
          class="h-11 w-full rounded-xl border border-white/7 bg-[#181818] pl-9 pr-3 text-sm text-white outline-none placeholder:text-zinc-600 transition focus:border-white/15"
          @input="
            updateFilter(
              'search',
              ($event.target as HTMLInputElement).value,
            )
          "
        />
      </div>

      <!-- Filter toggle -->
      <button
        type="button"
        class="relative flex h-11 w-11 shrink-0 items-center justify-center rounded-xl border border-white/7 bg-[#181818] text-zinc-500 transition hover:border-white/12 hover:bg-white/5 hover:text-white"
        :class="{
          'border-white/15 text-white': expanded || hasActiveFilters,
        }"
        aria-label="Toggle filters"
        :aria-expanded="expanded"
        @click="expanded = !expanded"
      >
        <svg
          viewBox="0 0 24 24"
          fill="none"
          class="h-4.5 w-4.5"
        >
          <path
            d="M4 6H20"
            stroke="currentColor"
            stroke-width="1.7"
            stroke-linecap="round"
          />

          <path
            d="M7 12H17"
            stroke="currentColor"
            stroke-width="1.7"
            stroke-linecap="round"
          />

          <path
            d="M10 18H14"
            stroke="currentColor"
            stroke-width="1.7"
            stroke-linecap="round"
          />
        </svg>

        <!-- Active filter indicator -->
        <span
          v-if="hasActiveFilters"
          class="absolute right-2 top-2 h-1.5 w-1.5 rounded-full bg-emerald-400"
        />
      </button>
    </div>

    <!-- Expanded filters -->
    <div
      v-if="expanded"
      class="mt-3 rounded-xl border border-white/6 bg-[#181818] p-4"
    >
      <div class="grid gap-3 md:grid-cols-2 lg:grid-cols-4">
        <!-- Media type -->
        <select
          :value="filters.mediaType"
          class="h-10 rounded-lg border border-white/7 bg-[#202020] px-3 text-sm text-zinc-300 outline-none focus:border-white/15"
          @change="
            updateFilter(
              'mediaType',
              ($event.target as HTMLSelectElement).value,
            )
          "
        >
          <option value="">All media</option>
          <option value="movie">Movies</option>
          <option value="episode">Episodes</option>
        </select>

        <!-- Source -->
        <select
          :value="filters.source"
          class="h-10 rounded-lg border border-white/7 bg-[#202020] px-3 text-sm text-zinc-300 outline-none focus:border-white/15"
          @change="
            updateFilter(
              'source',
              ($event.target as HTMLSelectElement).value,
            )
          "
        >
          <option value="">All sources</option>
          <option value="radarr">Radarr</option>
          <option value="sonarr">Sonarr</option>
        </select>

        <!-- Quality -->
        <input
          :value="filters.quality"
          type="text"
          placeholder="Quality"
          class="h-10 rounded-lg border border-white/7 bg-[#202020] px-3 text-sm text-zinc-300 outline-none placeholder:text-zinc-600 focus:border-white/15"
          @input="
            updateFilter(
              'quality',
              ($event.target as HTMLInputElement).value,
            )
          "
        />

        <!-- Season -->
        <input
          :value="filters.season ?? ''"
          type="number"
          min="0"
          placeholder="Season"
          class="h-10 rounded-lg border border-white/7 bg-[#202020] px-3 text-sm text-zinc-300 outline-none placeholder:text-zinc-600 focus:border-white/15"
          @input="
            updateFilter(
              'season',
              ($event.target as HTMLInputElement).value === ''
                ? null
                : Number(($event.target as HTMLInputElement).value),
            )
          "
        />

        <!-- From date -->
        <div>
          <label class="mb-1.5 block text-xs text-zinc-600">
            From
          </label>

          <input
            :value="filters.fromDate"
            type="datetime-local"
            class="h-10 w-full rounded-lg border border-white/7 bg-[#202020] px-3 text-sm text-zinc-300 outline-none focus:border-white/15"
            @input="
              updateFilter(
                'fromDate',
                ($event.target as HTMLInputElement).value,
              )
            "
          />
        </div>

        <!-- To date -->
        <div>
          <label class="mb-1.5 block text-xs text-zinc-600">
            To
          </label>

          <input
            :value="filters.toDate"
            type="datetime-local"
            class="h-10 w-full rounded-lg border border-white/7 bg-[#202020] px-3 text-sm text-zinc-300 outline-none focus:border-white/15"
            @input="
              updateFilter(
                'toDate',
                ($event.target as HTMLInputElement).value,
              )
            "
          />
        </div>
      </div>

      <!-- Sorting / clear -->
      <div
        class="mt-4 flex flex-wrap items-center justify-between gap-3 border-t border-white/5 pt-4"
      >
        <div class="flex items-center gap-2">
          <span class="text-xs text-zinc-600">
            Sort by
          </span>

          <select
            :value="filters.sort"
            class="h-9 rounded-lg border border-white/7 bg-[#202020] px-2.5 text-xs text-zinc-300 outline-none focus:border-white/15"
            @change="
              updateFilter(
                'sort',
                ($event.target as HTMLSelectElement).value as RecentImportFilterState['sort'],
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
          </select>

          <button
            type="button"
            class="flex h-9 items-center gap-1.5 rounded-lg border border-white/7 bg-[#202020] px-2.5 text-xs text-zinc-400 transition hover:border-white/12 hover:text-white"
            @click="toggleSortDirection"
          >
            <svg
              v-if="filters.sortDirection === 'desc'"
              viewBox="0 0 24 24"
              fill="none"
              class="h-3.5 w-3.5"
            >
              <path
                d="M12 5V19"
                stroke="currentColor"
                stroke-width="1.7"
                stroke-linecap="round"
              />

              <path
                d="M7 14L12 19L17 14"
                stroke="currentColor"
                stroke-width="1.7"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>

            <svg
              v-else
              viewBox="0 0 24 24"
              fill="none"
              class="h-3.5 w-3.5"
            >
              <path
                d="M12 19V5"
                stroke="currentColor"
                stroke-width="1.7"
                stroke-linecap="round"
              />

              <path
                d="M7 10L12 5L17 10"
                stroke="currentColor"
                stroke-width="1.7"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>

            {{ filters.sortDirection === 'desc' ? 'Newest' : 'Oldest' }}
          </button>
        </div>

        <button
          type="button"
          class="text-xs text-zinc-600 transition hover:text-zinc-300"
          @click="clearFilters"
        >
          Clear filters
        </button>
      </div>
    </div>
  </section>
</template>
