<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import ThemeToggle from './ThemeToggle.vue'
import LogoutButton from './LogoutButton.vue'

const router = useRouter()
const auth = useAuthStore()

const username = computed(() => auth.user?.username ?? '')

async function logout() {
  await auth.logout()

  await router.push({
    name: 'login',
  })
}
</script>

<template>
  <div
    class="min-h-screen bg-zinc-50 text-zinc-900 transition-colors duration-200 dark:bg-[#101010] dark:text-zinc-100"
  >
    <div class="flex min-h-screen">
      <!-- Sidebar -->
      <aside
        class="flex w-64 shrink-0 flex-col border-r border-zinc-200 bg-white transition-colors duration-200 dark:border-zinc-800 dark:bg-zinc-900"
      >
        <!-- Logo -->
        <div class="flex h-16 items-center border-b border-zinc-200 px-6 dark:border-zinc-800">
          <span class="text-lg font-semibold tracking-tight text-zinc-900 dark:text-white">
            Progressarr
          </span>
        </div>

        <!-- Navigation -->
        <nav class="flex-1 px-3 py-5">
          <div class="mb-2 px-3 text-xs font-medium uppercase tracking-wider text-zinc-500">
            Main
          </div>

          <RouterLink
            to="/"
            class="mb-1 flex items-center rounded-lg px-3 py-2.5 text-sm font-medium text-zinc-600 transition hover:bg-zinc-100 hover:text-zinc-900 dark:text-zinc-300 dark:hover:bg-zinc-800 dark:hover:text-white"
            active-class="bg-zinc-200 text-zinc-900 dark:bg-zinc-800 dark:text-white"
          >
            Dashboard
          </RouterLink>

          <div class="mb-2 mt-8 px-3 text-xs font-medium uppercase tracking-wider text-zinc-500">
            Settings
          </div>

          <RouterLink
            to="/settings"
            class="mb-1 flex items-center rounded-lg px-3 py-2.5 text-sm font-medium text-zinc-600 transition hover:bg-zinc-100 hover:text-zinc-900 dark:text-zinc-300 dark:hover:bg-zinc-800 dark:hover:text-white"
            active-class="bg-zinc-200 text-zinc-900 dark:bg-zinc-800 dark:text-white"
          >
            General
          </RouterLink>

          <RouterLink
            to="/settings/radarr"
            class="mb-1 flex items-center rounded-lg px-3 py-2.5 text-sm font-medium text-zinc-600 transition hover:bg-zinc-100 hover:text-zinc-900 dark:text-zinc-300 dark:hover:bg-zinc-800 dark:hover:text-white"
            active-class="bg-zinc-200 text-zinc-900 dark:bg-zinc-800 dark:text-white"
          >
            Radarr
          </RouterLink>

          <RouterLink
            to="/settings/sonarr"
            class="mb-1 flex items-center rounded-lg px-3 py-2.5 text-sm font-medium text-zinc-600 transition hover:bg-zinc-100 hover:text-zinc-900 dark:text-zinc-300 dark:hover:bg-zinc-800 dark:hover:text-white"
            active-class="bg-zinc-200 text-zinc-900 dark:bg-zinc-800 dark:text-white"
          >
            Sonarr
          </RouterLink>

          <RouterLink
            to="/settings/seerr"
            class="mb-1 flex items-center rounded-lg px-3 py-2.5 text-sm font-medium text-zinc-600 transition hover:bg-zinc-100 hover:text-zinc-900 dark:text-zinc-300 dark:hover:bg-zinc-800 dark:hover:text-white"
            active-class="bg-zinc-200 text-zinc-900 dark:bg-zinc-800 dark:text-white"
          >
            Seerr
          </RouterLink>

          <RouterLink
            to="/settings/jellyfin"
            class="mb-1 flex items-center rounded-lg px-3 py-2.5 text-sm font-medium text-zinc-600 transition hover:bg-zinc-100 hover:text-zinc-900 dark:text-zinc-300 dark:hover:bg-zinc-800 dark:hover:text-white"
            active-class="bg-zinc-200 text-zinc-900 dark:bg-zinc-800 dark:text-white"
          >
            Jellyfin
          </RouterLink>
        </nav>

        <!-- User -->
        <div class="border-t border-zinc-200 p-3 dark:border-zinc-800">
          <div class="mb-2 rounded-lg px-3 py-2">
            <div class="text-sm font-medium text-zinc-900 dark:text-white">
              {{ username }}
            </div>

            <div class="text-xs text-zinc-500">Administrator</div>
          </div>

          <button
            type="button"
            class="w-full rounded-lg px-3 py-2 text-left text-sm text-zinc-500 transition hover:bg-zinc-100 hover:text-zinc-900 dark:text-zinc-400 dark:hover:bg-zinc-800 dark:hover:text-white"
            @click="logout"
          >
            Sign out
          </button>
        </div>
      </aside>

      <!-- Main -->
      <div class="min-w-0 flex-1">
        <!-- Header -->
        <header
          class="flex h-16 items-center justify-between border-b border-zinc-200 bg-zinc-50 px-8 transition-colors duration-200 dark:border-zinc-800 dark:bg-[#101010]"
        >
          <div class="flex w-full items-center justify-between">
            <slot name="header" />

            <div class="flex flex-row gap-1 sm:gap-2">
              <ThemeToggle />
              <LogoutButton />
            </div>
          </div>
        </header>

        <!-- Content -->
        <main class="p-8">
          <slot />
        </main>
      </div>
    </div>
  </div>
</template>
