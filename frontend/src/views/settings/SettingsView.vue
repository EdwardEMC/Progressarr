<script setup lang="ts">
import { onMounted, ref } from 'vue'

import AppLayout from '../../components/AppLayout.vue'
import { getSettings } from '../../api/settings.ts'

const radarrConfigured = ref(false)
const sonarrConfigured = ref(false)
const seerrConfigured = ref(false)
const jellyfinConfigured = ref(false)

onMounted(async () => {
  try {
    const settings = await getSettings()

    radarrConfigured.value = settings.radarr.configured
    sonarrConfigured.value = settings.sonarr.configured
    seerrConfigured.value = settings.seerr.configured
    jellyfinConfigured.value = settings.jellyfin.configured
  } catch {
    // The individual settings pages handle detailed errors.
  }
})
</script>

<template>
  <AppLayout>
    <template #header>
      <h1 class="text-lg font-semibold">Settings</h1>
    </template>

    <div>
      <div class="mb-8">
        <h2 class="text-2xl font-semibold">Settings</h2>

        <p class="mt-1 text-sm text-zinc-400">Configure your Progressarr services.</p>
      </div>

      <div class="grid gap-4 md:grid-cols-2">
        <RouterLink
          to="/settings/radarr"
          class="rounded-xl border border-zinc-800 bg-zinc-900 p-6 transition hover:border-zinc-700 hover:bg-zinc-800"
        >
          <div class="flex items-start justify-between gap-4">
            <div>
              <h3 class="font-medium text-white">Radarr</h3>

              <p class="mt-2 text-sm text-zinc-400">Configure your Radarr connection.</p>
            </div>

            <span
              class="rounded-full px-2.5 py-1 text-xs font-medium"
              :class="
                radarrConfigured ? 'bg-green-500/10 text-green-400' : 'bg-zinc-800 text-zinc-400'
              "
            >
              {{ radarrConfigured ? 'Configured' : 'Not configured' }}
            </span>
          </div>
        </RouterLink>

        <RouterLink
          to="/settings/sonarr"
          class="rounded-xl border border-zinc-800 bg-zinc-900 p-6 transition hover:border-zinc-700 hover:bg-zinc-800"
        >
          <div class="flex items-start justify-between gap-4">
            <div>
              <h3 class="font-medium text-white">Sonarr</h3>

              <p class="mt-2 text-sm text-zinc-400">Configure your Sonarr connection.</p>
            </div>

            <span
              class="rounded-full px-2.5 py-1 text-xs font-medium"
              :class="
                sonarrConfigured ? 'bg-green-500/10 text-green-400' : 'bg-zinc-800 text-zinc-400'
              "
            >
              {{ sonarrConfigured ? 'Configured' : 'Not configured' }}
            </span>
          </div>
        </RouterLink>

        <RouterLink
          to="/settings/seerr"
          class="rounded-xl border border-zinc-800 bg-zinc-900 p-6 transition hover:border-zinc-700 hover:bg-zinc-800"
        >
          <div class="flex items-start justify-between gap-4">
            <div>
              <h3 class="font-medium text-white">Seerr</h3>

              <p class="mt-2 text-sm text-zinc-400">Configure your Seerr connection.</p>
            </div>

            <span
              class="rounded-full px-2.5 py-1 text-xs font-medium"
              :class="
                seerrConfigured ? 'bg-green-500/10 text-green-400' : 'bg-zinc-800 text-zinc-400'
              "
            >
              {{ seerrConfigured ? 'Configured' : 'Not configured' }}
            </span>
          </div>
        </RouterLink>

        <RouterLink
          to="/settings/jellyfin"
          class="rounded-xl border border-zinc-800 bg-zinc-900 p-6 transition hover:border-zinc-700 hover:bg-zinc-800"
        >
          <div class="flex items-start justify-between gap-4">
            <div>
              <h3 class="font-medium text-white">Jellyfin</h3>

              <p class="mt-2 text-sm text-zinc-400">Configure your Jellyfin connection.</p>
            </div>

            <span
              class="rounded-full px-2.5 py-1 text-xs font-medium"
              :class="
                jellyfinConfigured ? 'bg-green-500/10 text-green-400' : 'bg-zinc-800 text-zinc-400'
              "
            >
              {{ jellyfinConfigured ? 'Configured' : 'Not configured' }}
            </span>
          </div>
        </RouterLink>
      </div>
    </div>
  </AppLayout>
</template>
