<script setup lang="ts">
import { onMounted, ref } from "vue";

import AppLayout from "../components/AppLayout.vue";
import {
  getSettings,
  testJellyfinConnection,
  updateSettings,
} from "../api/settings";

const url = ref("");
const apiKey = ref("");

const loading = ref(true);
const saving = ref(false);
const testing = ref(false);

const message = ref("");
const error = ref("");

onMounted(async () => {
  try {
    const settings = await getSettings();

    url.value = settings.jellyfin.url ?? "";
  } catch (err) {
    error.value =
      err instanceof Error ? err.message : "Unable to load Jellyfin settings.";
  } finally {
    loading.value = false;
  }
});

async function save() {
  saving.value = true;
  message.value = "";
  error.value = "";

  try {
    await updateSettings({
      jellyfin: {
        url: url.value,
        api_key: apiKey.value || undefined,
      },
    });

    message.value = "Jellyfin settings saved.";
    apiKey.value = "";
  } catch (err) {
    error.value =
      err instanceof Error ? err.message : "Unable to save Jellyfin settings.";
  } finally {
    saving.value = false;
  }
}

async function testConnection() {
  testing.value = true;
  message.value = "";
  error.value = "";

  try {
    const result = await testJellyfinConnection(url.value, apiKey.value);

    if (result.success) {
      message.value = result.message;
    } else {
      error.value = result.message;
    }
  } catch (err) {
    error.value =
      err instanceof Error
        ? err.message
        : "Unable to test Jellyfin connection.";
  } finally {
    testing.value = false;
  }
}
</script>

<template>
  <AppLayout>
    <template #header>
      <h1 class="text-lg font-semibold">Jellyfin</h1>
    </template>

    <div class="max-w-2xl">
      <h2 class="text-2xl font-semibold">Jellyfin</h2>

      <p class="mt-2 text-sm text-gray-400">
        Configure your Jellyfin server connection.
      </p>

      <div v-if="loading" class="mt-6 text-sm text-gray-400">
        Loading settings...
      </div>

      <form v-else class="mt-6 space-y-6" @submit.prevent="save">
        <div>
          <label
            for="jellyfin-url"
            class="block text-sm font-medium text-gray-300"
          >
            URL
          </label>

          <input
            id="jellyfin-url"
            v-model="url"
            type="url"
            placeholder="http://localhost:8096"
            required
            class="mt-2 block w-full rounded-md border border-gray-700 bg-gray-900 px-3 py-2 text-sm text-white placeholder-gray-500 focus:border-indigo-500 focus:outline-none"
          />
        </div>

        <div>
          <label
            for="jellyfin-api-key"
            class="block text-sm font-medium text-gray-300"
          >
            API Key
          </label>

          <input
            id="jellyfin-api-key"
            v-model="apiKey"
            type="password"
            placeholder="Enter Jellyfin API key"
            required
            class="mt-2 block w-full rounded-md border border-gray-700 bg-gray-900 px-3 py-2 text-sm text-white placeholder-gray-500 focus:border-indigo-500 focus:outline-none"
          />
        </div>

        <div class="flex gap-3">
          <button
            type="button"
            :disabled="testing"
            class="rounded-md border border-gray-700 px-4 py-2 text-sm font-medium text-gray-300 hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-50"
            @click="testConnection"
          >
            {{ testing ? "Testing..." : "Test Connection" }}
          </button>

          <button
            type="submit"
            :disabled="saving"
            class="rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {{ saving ? "Saving..." : "Save" }}
          </button>
        </div>

        <p v-if="message" class="text-sm text-green-400">
          {{ message }}
        </p>

        <p v-if="error" class="text-sm text-red-400">
          {{ error }}
        </p>
      </form>
    </div>
  </AppLayout>
</template>
