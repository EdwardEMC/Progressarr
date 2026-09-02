<script setup lang="ts">
import AppLayout from '../components/AppLayout.vue'
</script>


<template>
  <AppLayout>

    <template #header>
      <h1 class="text-lg font-semibold">
        Settings
      </h1>
    </template>


    <div>

      <div class="mb-8">
        <h2 class="text-2xl font-semibold">
          Settings
        </h2>

        <p class="mt-1 text-sm text-zinc-400">
          Configure your Progressarr services.
        </p>
      </div>


      <div class="grid gap-4 md:grid-cols-2">

        <RouterLink
          to="/settings/radarr"
          class="rounded-xl border border-zinc-800 bg-zinc-900 p-6 transition hover:border-zinc-700 hover:bg-zinc-800"
        >
          <h3 class="font-medium text-white">
            Radarr
          </h3>

          <p class="mt-2 text-sm text-zinc-400">
            Configure your Radarr connection.
          </p>
        </RouterLink>


        <RouterLink
          to="/settings/sonarr"
          class="rounded-xl border border-zinc-800 bg-zinc-900 p-6 transition hover:border-zinc-700 hover:bg-zinc-800"
        >
          <h3 class="font-medium text-white">
            Sonarr
          </h3>

          <p class="mt-2 text-sm text-zinc-400">
            Configure your Sonarr connection.
          </p>
        </RouterLink>


        <RouterLink
          to="/settings/jellyfin"
          class="rounded-xl border border-zinc-800 bg-zinc-900 p-6 transition hover:border-zinc-700 hover:bg-zinc-800"
        >
          <h3 class="font-medium text-white">
            Jellyfin
          </h3>

          <p class="mt-2 text-sm text-zinc-400">
            Configure your Jellyfin connection.
          </p>
        </RouterLink>

      </div>

    </div>

  </AppLayout>
</template>
