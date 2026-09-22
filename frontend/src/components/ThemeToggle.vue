<script setup lang="ts">
import { useThemeStore } from '../stores/theme'

const theme = useThemeStore()
</script>

<template>
  <button
    type="button"
    class="cursor-pointer relative flex h-9 w-9 items-center justify-center rounded-lg text-zinc-600 transition hover:bg-zinc-100 hover:text-zinc-900 dark:text-zinc-400 dark:hover:bg-white/5 dark:hover:text-white"
    :title="theme.isDark ? 'Switch to light mode' : 'Switch to dark mode'"
    :aria-label="theme.isDark ? 'Switch to light mode' : 'Switch to dark mode'"
    @click="theme.toggleTheme"
  >
    <!-- Sun -->
    <svg v-if="theme.isDark" viewBox="0 0 24 24" fill="none" class="h-5 w-5">
      <circle cx="12" cy="12" r="4" stroke="currentColor" stroke-width="1.8" />

      <path d="M12 2V4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />

      <path d="M12 20V22" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />

      <path
        d="M4.93 4.93L6.34 6.34"
        stroke="currentColor"
        stroke-width="1.8"
        stroke-linecap="round"
      />

      <path
        d="M17.66 17.66L19.07 19.07"
        stroke="currentColor"
        stroke-width="1.8"
        stroke-linecap="round"
      />

      <path d="M2 12H4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />

      <path d="M20 12H22" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />

      <path
        d="M4.93 19.07L6.34 17.66"
        stroke="currentColor"
        stroke-width="1.8"
        stroke-linecap="round"
      />

      <path
        d="M17.66 6.34L19.07 4.93"
        stroke="currentColor"
        stroke-width="1.8"
        stroke-linecap="round"
      />
    </svg>

    <!-- Moon -->
    <svg v-else viewBox="0 0 24 24" fill="none" class="h-5 w-5">
      <path
        d="M20.5 15.2A8.5 8.5 0 0 1 8.8 3.5A8.5 8.5 0 1 0 20.5 15.2Z"
        stroke="currentColor"
        stroke-width="1.8"
        stroke-linecap="round"
        stroke-linejoin="round"
      />
    </svg>
  </button>
</template>
