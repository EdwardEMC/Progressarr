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
  <div
    class="rounded-xl border border-zinc-200 bg-white transition-colors duration-200 dark:border-zinc-800 dark:bg-zinc-900"
  >
    <!-- Header -->
    <div class="border-b border-zinc-200 px-6 py-5 dark:border-zinc-800">
      <h3 class="font-medium text-zinc-900 dark:text-white">Connection</h3>

      <p class="mt-1 text-sm text-zinc-500">
        Connect Progressarr to your {{ serviceName }} instance.
      </p>
    </div>

    <!-- Form -->
    <div class="space-y-6 p-6">
      <!-- URL -->
      <div>
        <label
          :for="`${serviceName}-url`"
          class="mb-2 block text-sm font-medium text-zinc-700 dark:text-zinc-300"
        >
          {{ serviceName }} URL
        </label>

        <input
          :id="`${serviceName}-url`"
          v-model="url"
          type="url"
          :placeholder="`http://${serviceName.toLowerCase()}:7878`"
          :disabled="loading || saving || testing"
          class="w-full rounded-lg border border-zinc-300 bg-white px-3 py-2.5 text-zinc-900 outline-none transition placeholder:text-zinc-400 focus:border-zinc-400 dark:border-zinc-700 dark:bg-zinc-950 dark:text-white dark:placeholder:text-zinc-600 dark:focus:border-zinc-500 disabled:opacity-50"
        />

        <p class="mt-2 text-xs text-zinc-500">
          The URL Progressarr uses to reach {{ serviceName }}.
        </p>
      </div>

      <!-- API Key -->
      <div>
        <label
          :for="`${serviceName}-api-key`"
          class="mb-2 block text-sm font-medium text-zinc-700 dark:text-zinc-300"
        >
          API Key
        </label>

        <input
          :id="`${serviceName}-api-key`"
          v-model="apiKey"
          type="password"
          autocomplete="new-password"
          placeholder="Enter API key"
          :disabled="loading || saving || testing"
          class="w-full rounded-lg border border-zinc-300 bg-white px-3 py-2.5 text-zinc-900 outline-none transition placeholder:text-zinc-400 focus:border-zinc-400 dark:border-zinc-700 dark:bg-zinc-950 dark:text-white dark:placeholder:text-zinc-600 dark:focus:border-zinc-500 disabled:opacity-50"
        />

        <p class="mt-2 text-xs text-zinc-500">Leave blank to keep the existing API key.</p>
      </div>

      <!-- Connection result -->
      <div
        v-if="connectionMessage"
        class="rounded-lg border px-4 py-3 text-sm"
        :class="
          connectionSuccess
            ? 'border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-900/50 dark:bg-emerald-950/30 dark:text-emerald-400'
            : 'border-red-200 bg-red-50 text-red-700 dark:border-red-900/50 dark:bg-red-950/30 dark:text-red-400'
        "
      >
        {{ connectionMessage }}
      </div>

      <!-- Error -->
      <div
        v-if="error"
        class="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 dark:border-red-900/50 dark:bg-red-950/30 dark:text-red-400"
      >
        {{ error }}
      </div>

      <!-- Success -->
      <div
        v-if="success"
        class="rounded-lg border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-700 dark:border-emerald-900/50 dark:bg-emerald-950/30 dark:text-emerald-400"
      >
        {{ success }}
      </div>
    </div>

    <!-- Actions -->
    <div
      class="flex items-center justify-end gap-3 border-t border-zinc-200 px-6 py-4 dark:border-zinc-800"
    >
      <button
        type="button"
        class="rounded-lg border border-zinc-300 px-4 py-2 text-sm font-medium text-zinc-700 transition hover:bg-zinc-100 hover:text-zinc-900 dark:border-zinc-700 dark:text-zinc-300 dark:hover:bg-zinc-800 dark:hover:text-white disabled:cursor-not-allowed disabled:opacity-50"
        :disabled="loading || saving || testing || !url.trim() || !apiKey.trim()"
        @click="handleTest"
      >
        {{ testing ? 'Testing...' : 'Test Connection' }}
      </button>

      <button
        type="button"
        class="rounded-lg bg-zinc-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-zinc-800 dark:bg-white dark:text-zinc-900 dark:hover:bg-zinc-200 disabled:cursor-not-allowed disabled:opacity-50"
        :disabled="loading || saving || testing || !url.trim()"
        @click="handleSave"
      >
        {{ saving ? 'Saving...' : 'Save' }}
      </button>
    </div>
  </div>
</template>
