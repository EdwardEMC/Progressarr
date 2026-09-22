<script setup lang="ts">
import { useRouter } from 'vue-router'

import ThemeToggle from '../components/ThemeToggle.vue'
import { useAuthStore } from '../stores/auth'
import LogoutButton from '../components/LogoutButton.vue'

const router = useRouter()

const auth = useAuthStore()
</script>

<template>
  <div
    class="min-h-screen bg-zinc-50 text-zinc-900 transition-colors duration-200 dark:bg-[#101010] dark:text-white"
  >
    <!-- Header -->
    <header
      class="sticky top-0 z-50 border-b border-zinc-200/80 bg-zinc-50/90 backdrop-blur-xl transition-colors duration-200 dark:border-white/6 dark:bg-[#101010]/90"
    >
      <div class="mx-auto flex h-20 max-w-7xl items-center justify-between px-6 lg:px-8">
        <!-- Branding -->
        <div class="flex cursor-pointer items-center gap-4" @click="router.push('/')">
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
            <h1 class="text-lg font-semibold tracking-tight text-zinc-900 dark:text-white">
              Progressarr
            </h1>

            <p class="hidden text-xs text-zinc-500 sm:block">Download progress</p>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex items-center gap-1 sm:gap-2">
          <!-- Page-specific actions -->
          <slot name="actions" />

          <!-- Theme -->
          <ThemeToggle />

          <!-- Settings -->
          <button
            v-if="auth.isAdmin"
            type="button"
            class="flex h-9 w-9 items-center justify-center rounded-lg text-zinc-500 transition hover:bg-zinc-100 hover:text-zinc-900 dark:text-zinc-400 dark:hover:bg-white/5 dark:hover:text-white"
            title="Settings"
            aria-label="Settings"
            @click="router.push('/settings')"
          >
            <svg viewBox="0 0 24 24" fill="none" class="h-5 w-5">
              <path
                d="M12 15.5A3.5 3.5 0 1 0 12 8.5A3.5 3.5 0 0 0 12 15.5Z"
                stroke="currentColor"
                stroke-width="1.8"
              />

              <path
                d="M19.4 15A1.7 1.7 0 0 0 19.7 16.9L19.75 17 A2 2 0 0 1 16.9 19.75L16.8 19.7 A1.7 1.7 0 0 0 15 19.4 A1.7 1.7 0 0 0 14 21V21 A2 2 0 0 1 10 21V20.9 A1.7 1.7 0 0 0 9 19.4 A1.7 1.7 0 0 0 7.2 19.7L7.1 19.75 A2 2 0 0 1 4.25 16.9L4.3 16.8 A1.7 1.7 0 0 0 4.6 15 A1.7 1.7 0 0 0 3 14H3 A2 2 0 0 1 3 10H3 A1.7 1.7 0 0 0 4.6 9 A1.7 1.7 0 0 0 4.3 7.2L4.25 7.1 A2 2 0 0 1 7.1 4.25L7.2 4.3 A1.7 1.7 0 0 0 9 4.6 A1.7 1.7 0 0 0 10 3V3 A2 2 0 0 1 14 3V3 A1.7 1.7 0 0 0 15 4.6 A1.7 1.7 0 0 0 16.8 4.3L16.9 4.25 A2 2 0 0 1 19.75 7.1L19.7 7.2 A1.7 1.7 0 0 0 19.4 9 A1.7 1.7 0 0 0 21 10H21 A2 2 0 0 1 21 14H21 A1.7 1.7 0 0 0 19.4 15Z"
                stroke="currentColor"
                stroke-width="1.4"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
          </button>

          <!-- Logout -->
          <LogoutButton />
        </div>
      </div>
    </header>

    <!-- Page content -->
    <main class="mx-auto max-w-7xl px-6 py-10 lg:px-8">
      <router-view />
    </main>
  </div>
</template>
