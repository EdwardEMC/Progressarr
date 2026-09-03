<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{
  serviceName: string
  url: string
  configured: boolean
  loading?: boolean
  saving?: boolean
  testing?: boolean
  error?: string
  success?: string
  connectionMessage?: string
  connectionSuccess?: boolean
}>()

const emit = defineEmits<{
  save: [
    payload: {
      url: string
      apiKey?: string
    },
  ]

  test: [
    payload: {
      url: string
      apiKey: string
    },
  ]
}>()

const url = ref(props.url)
const apiKey = ref('')

watch(
  () => props.url,
  (value) => {
    url.value = value
  },
)

function handleTest() {
  if (!url.value.trim() || !apiKey.value.trim()) {
    return
  }

  emit('test', {
    url: url.value,
    apiKey: apiKey.value,
  })
}

function handleSave() {
  emit('save', {
    url: url.value,
    ...(apiKey.value.trim() ? { apiKey: apiKey.value } : {}),
  })
}

function clearApiKey() {
  apiKey.value = ''
}

defineExpose({
  clearApiKey,
})
</script>

<template>
  <div class="rounded-xl border border-zinc-800 bg-zinc-900">
    <!-- Header -->
    <div class="border-b border-zinc-800 px-6 py-5">
      <h3 class="font-medium text-white">Connection</h3>

      <p class="mt-1 text-sm text-zinc-500">
        Connect Progressarr to your {{ serviceName }} instance.
      </p>
    </div>

    <!-- Form -->
    <div class="space-y-6 p-6">
      <!-- URL -->
      <div>
        <label :for="`${serviceName}-url`" class="mb-2 block text-sm font-medium text-zinc-300">
          {{ serviceName }} URL
        </label>

        <input
          :id="`${serviceName}-url`"
          v-model="url"
          type="url"
          :placeholder="`http://${serviceName.toLowerCase()}:7878`"
          :disabled="loading || saving || testing"
          class="w-full rounded-lg border border-zinc-700 bg-zinc-950 px-3 py-2.5 text-white outline-none transition placeholder:text-zinc-600 focus:border-zinc-500 disabled:opacity-50"
        />

        <p class="mt-2 text-xs text-zinc-500">
          The URL Progressarr uses to reach {{ serviceName }}.
        </p>
      </div>

      <!-- API Key -->
      <div>
        <label :for="`${serviceName}-api-key`" class="mb-2 block text-sm font-medium text-zinc-300">
          API Key
        </label>

        <input
          :id="`${serviceName}-api-key`"
          v-model="apiKey"
          type="password"
          autocomplete="new-password"
          placeholder="Enter API key"
          :disabled="loading || saving || testing"
          class="w-full rounded-lg border border-zinc-700 bg-zinc-950 px-3 py-2.5 text-white outline-none transition placeholder:text-zinc-600 focus:border-zinc-500 disabled:opacity-50"
        />

        <p class="mt-2 text-xs text-zinc-500">Leave blank to keep the existing API key.</p>
      </div>

      <!-- Connection result -->
      <div
        v-if="connectionMessage"
        class="rounded-lg border px-4 py-3 text-sm"
        :class="
          connectionSuccess
            ? 'border-emerald-900/50 bg-emerald-950/30 text-emerald-400'
            : 'border-red-900/50 bg-red-950/30 text-red-400'
        "
      >
        {{ connectionMessage }}
      </div>

      <!-- Error -->
      <div
        v-if="error"
        class="rounded-lg border border-red-900/50 bg-red-950/30 px-4 py-3 text-sm text-red-400"
      >
        {{ error }}
      </div>

      <!-- Success -->
      <div
        v-if="success"
        class="rounded-lg border border-emerald-900/50 bg-emerald-950/30 px-4 py-3 text-sm text-emerald-400"
      >
        {{ success }}
      </div>
    </div>

    <!-- Actions -->
    <div class="flex items-center justify-end gap-3 border-t border-zinc-800 px-6 py-4">
      <button
        type="button"
        class="rounded-lg border border-zinc-700 px-4 py-2 text-sm font-medium text-zinc-300 transition hover:bg-zinc-800 hover:text-white disabled:cursor-not-allowed disabled:opacity-50"
        :disabled="loading || saving || testing || !url.trim() || !apiKey.trim()"
        @click="handleTest"
      >
        {{ testing ? 'Testing...' : 'Test Connection' }}
      </button>

      <button
        type="button"
        class="rounded-lg bg-white px-4 py-2 text-sm font-medium text-zinc-900 transition hover:bg-zinc-200 disabled:cursor-not-allowed disabled:opacity-50"
        :disabled="loading || saving || testing || !url.trim()"
        @click="handleSave"
      >
        {{ saving ? 'Saving...' : 'Save' }}
      </button>
    </div>
  </div>
</template>
