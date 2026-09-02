<script setup lang="ts">
import { onMounted, ref } from 'vue'

import AppLayout from '../components/AppLayout.vue'
import ServiceSettingsForm from '../components/ServiceSettingsForm.vue'

import {
  getSettings,
  testRadarrConnection,
  updateSettings,
} from '../api/settings'


const url = ref('')
const configured = ref(false)

const loading = ref(true)
const saving = ref(false)
const testing = ref(false)

const error = ref('')
const success = ref('')

const connectionMessage = ref('')
const connectionSuccess = ref(false)

const form = ref<
  InstanceType<typeof ServiceSettingsForm> | null
>(null)


async function loadSettings() {
  loading.value = true
  error.value = ''

  try {
    const settings = await getSettings()

    url.value = settings.radarr.url ?? ''
    configured.value = settings.radarr.configured
  } catch {
    error.value = 'Unable to load Radarr settings.'
  } finally {
    loading.value = false
  }
}


async function testConnection(payload: {
  url: string
  apiKey: string
}) {
  error.value = ''
  success.value = ''
  connectionMessage.value = ''

  testing.value = true

  try {
    const result = await testRadarrConnection(
      payload.url,
      payload.apiKey,
    )

    connectionSuccess.value = result.success
    connectionMessage.value = result.message
  } catch {
    connectionSuccess.value = false
    connectionMessage.value =
      'Unable to test the Radarr connection.'
  } finally {
    testing.value = false
  }
}


async function save(payload: {
  url: string
  apiKey?: string
}) {
  error.value = ''
  success.value = ''

  saving.value = true

  try {
    await updateSettings({
      radarr: {
        url: payload.url,
        ...(payload.apiKey
          ? { api_key: payload.apiKey }
          : {}),
      },
    })

    url.value = payload.url
    configured.value = true

    form.value?.clearApiKey()

    success.value =
      'Radarr settings saved successfully.'
  } catch {
    error.value =
      'Unable to save Radarr settings.'
  } finally {
    saving.value = false
  }
}


onMounted(loadSettings)
</script>


<template>
  <AppLayout>

    <template #header>
      <h1 class="text-lg font-semibold">
        Radarr
      </h1>
    </template>


    <div class="mx-auto max-w-3xl">

      <div class="mb-8">
        <h2 class="text-2xl font-semibold">
          Radarr
        </h2>

        <p class="mt-1 text-sm text-zinc-400">
          Configure your Radarr connection.
        </p>
      </div>


      <div v-if="loading">
        <div
          class="rounded-xl border border-zinc-800 bg-zinc-900 p-6 text-sm text-zinc-500"
        >
          Loading settings...
        </div>
      </div>


      <ServiceSettingsForm
        v-else
        ref="form"
        service-name="Radarr"
        :url="url"
        :configured="configured"
        :loading="loading"
        :saving="saving"
        :testing="testing"
        :error="error"
        :success="success"
        :connection-message="connectionMessage"
        :connection-success="connectionSuccess"
        @save="save"
        @test="testConnection"
      />

    </div>

  </AppLayout>
</template>
