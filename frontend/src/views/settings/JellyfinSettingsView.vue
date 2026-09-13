<script setup lang="ts">
import { onMounted, ref } from 'vue'

import AppLayout from '../../components/AppLayout.vue'
import { getSettings, testJellyfinConnection, updateSettings } from '../../api/settings.ts'

const url = ref('')
const apiKey = ref('')

const loading = ref(true)
const saving = ref(false)
const testing = ref(false)

const message = ref('')
const error = ref('')

onMounted(async () => {
  try {
    const settings = await getSettings()

    url.value = settings.jellyfin.url ?? ''
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Unable to load Jellyfin settings.'
  } finally {
    loading.value = false
  }
})

async function save() {
  saving.value = true
  message.value = ''
  error.value = ''

  try {
    await updateSettings({
      jellyfin: {
        url: url.value,
        api_key: apiKey.value || undefined,
      },
    })

    message.value = 'Jellyfin settings saved.'
    apiKey.value = ''
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Unable to save Jellyfin settings.'
  } finally {
    saving.value = false
  }
}

async function testConnection() {
  testing.value = true
  message.value = ''
  error.value = ''

  try {
    const result = await testJellyfinConnection(url.value, apiKey.value)

    if (result.success) {
      message.value = result.message
    } else {
      error.value = result.message
    }
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Unable to test Jellyfin connection.'
  } finally {
    testing.value = false
  }
}
</script>

<template>
  <AppLayout>
    <template #header>
      <h1 class="text-lg font-semibold text-zinc-900 dark:text-white">Jellyfin</h1>
    </template>

    <div class="mx-auto max-w-3xl">
      <div class="mb-8">
        <h2 class="text-2xl font-semibold text-zinc-900 dark:text-white">Jellyfin</h2>

        <p class="mt-1 text-sm text-zinc-600 dark:text-zinc-400">
          Configure your Jellyfin server connection.
        </p>
      </div>

      <div v-if="loading">
        <div
          class="rounded-xl border border-zinc-200 bg-white p-6 text-sm text-zinc-500 transition-colors duration-200 dark:border-zinc-800 dark:bg-zinc-900"
        >
          Loading settings...
        </div>
      </div>

      <form
        v-else
        class="rounded-xl border border-zinc-200 bg-white transition-colors duration-200 dark:border-zinc-800 dark:bg-zinc-900"
        @submit.prevent="save"
      >
        <div class="border-b border-zinc-200 px-6 py-5 dark:border-zinc-800">
          <h3 class="font-medium text-zinc-900 dark:text-white">Connection</h3>

          <p class="mt-1 text-sm text-zinc-500">Connect Progressarr to your Jellyfin server.</p>
        </div>

        <div class="space-y-5 px-6 py-6">
          <div>
            <label
              for="jellyfin-url"
              class="block text-sm font-medium text-zinc-800 dark:text-zinc-300"
            >
              URL
            </label>

            <input
              id="jellyfin-url"
              v-model="url"
              type="url"
              placeholder="http://localhost:8096"
              required
              class="mt-2 block w-full rounded-lg border border-zinc-300 bg-white px-3 py-2.5 text-sm text-zinc-900 outline-none transition placeholder:text-zinc-400 focus:border-zinc-400 dark:border-zinc-700 dark:bg-zinc-950 dark:text-white dark:placeholder:text-zinc-600 dark:focus:border-zinc-500"
            />
          </div>

          <div>
            <label
              for="jellyfin-api-key"
              class="block text-sm font-medium text-zinc-800 dark:text-zinc-300"
            >
              API Key
            </label>

            <input
              id="jellyfin-api-key"
              v-model="apiKey"
              type="password"
              placeholder="Enter Jellyfin API key"
              required
              class="mt-2 block w-full rounded-lg border border-zinc-300 bg-white px-3 py-2.5 text-sm text-zinc-900 outline-none transition placeholder:text-zinc-400 focus:border-zinc-400 dark:border-zinc-700 dark:bg-zinc-950 dark:text-white dark:placeholder:text-zinc-600 dark:focus:border-zinc-500"
            />
          </div>
        </div>

        <div
          class="flex flex-wrap items-center gap-3 border-t border-zinc-200 px-6 py-4 dark:border-zinc-800"
        >
          <button
            type="button"
            :disabled="testing"
            class="rounded-lg border border-zinc-300 bg-white px-4 py-2 text-sm font-medium text-zinc-700 transition hover:border-zinc-400 hover:bg-zinc-50 hover:text-zinc-900 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-300 dark:hover:border-zinc-600 dark:hover:bg-zinc-800 dark:hover:text-white disabled:cursor-not-allowed disabled:opacity-50"
            @click="testConnection"
          >
            {{ testing ? 'Testing...' : 'Test Connection' }}
          </button>

          <button
            type="submit"
            :disabled="saving"
            class="rounded-lg bg-zinc-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-zinc-800 dark:bg-white dark:text-zinc-900 dark:hover:bg-zinc-200 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {{ saving ? 'Saving...' : 'Save' }}
          </button>
        </div>

        <div
          v-if="message || error"
          class="border-t border-zinc-200 px-6 py-4 dark:border-zinc-800"
        >
          <p
            v-if="message"
            class="rounded-lg border border-emerald-200 bg-emerald-50 px-3 py-2 text-sm text-emerald-700 dark:border-emerald-900/50 dark:bg-emerald-950/30 dark:text-emerald-400"
          >
            {{ message }}
          </p>

          <p
            v-if="error"
            class="rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700 dark:border-red-900/50 dark:bg-red-950/30 dark:text-red-400"
          >
            {{ error }}
          </p>
        </div>
      </form>
    </div>
  </AppLayout>
</template>
