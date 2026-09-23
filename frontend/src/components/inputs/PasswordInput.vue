<script setup lang="ts">
import { ref } from 'vue'

defineProps<{
  modelValue: string
  placeholder?: string
  disabled?: boolean
  autocomplete?: string
  id?: string
  required?: boolean
  minlength?: number
}>()

const emit = defineEmits<{ 'update:modelValue': [value: string] }>()

const showPassword = ref(false)
const pasteError = ref(false)

async function pasteFromClipboard() {
  pasteError.value = false

  try {
    const text = await navigator.clipboard.readText()
    emit('update:modelValue', text)
  } catch {
    pasteError.value = true
  }
}
</script>

<template>
  <div>
    <div class="relative">
      <input
        :id="id"
        :value="modelValue"
        :type="showPassword ? 'text' : 'password'"
        :required="required"
        :minlength="minlength"
        :autocomplete="autocomplete"
        :placeholder="placeholder"
        :disabled="disabled"
        class="w-full rounded-lg border border-zinc-300 bg-white py-2.5 pl-3 pr-20 text-zinc-900 outline-none transition placeholder:text-zinc-400 focus:border-zinc-400 dark:border-zinc-700 dark:bg-zinc-950 dark:text-white dark:placeholder:text-zinc-600 dark:focus:border-zinc-500 disabled:cursor-not-allowed disabled:opacity-50"
        @input="emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      />

      <div class="absolute inset-y-0 right-2 flex items-center gap-1">
        <!-- Paste -->
        <button
          type="button"
          :disabled="disabled"
          title="Paste from clipboard"
          class="flex h-8 w-8 items-center justify-center rounded-md text-zinc-500 transition hover:bg-zinc-100 hover:text-zinc-900 dark:hover:bg-zinc-800 dark:hover:text-white disabled:cursor-not-allowed disabled:opacity-50"
          @click="pasteFromClipboard"
        >
          <svg
            viewBox="0 0 24 24"
            fill="none"
            class="h-4 w-4"
            stroke="currentColor"
            stroke-width="1.8"
          >
            <rect x="8" y="4" width="11" height="16" rx="2" />
            <path d="M8 7H6a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h7a2 2 0 0 0 2-2v-1" />
            <path d="M10 4h7" />
          </svg>
        </button>

        <!-- Toggle visibility -->
        <button
          type="button"
          :disabled="disabled"
          :title="showPassword ? 'Hide password' : 'Show password'"
          class="flex h-8 w-8 items-center justify-center rounded-md text-zinc-500 transition hover:bg-zinc-100 hover:text-zinc-900 dark:hover:bg-zinc-800 dark:hover:text-white disabled:cursor-not-allowed disabled:opacity-50"
          @click="showPassword = !showPassword"
        >
          <!-- Eye -->
          <svg
            v-if="!showPassword"
            viewBox="0 0 24 24"
            fill="none"
            class="h-4 w-4"
            stroke="currentColor"
            stroke-width="1.8"
          >
            <path d="M2.5 12s3.5-6 9.5-6 9.5 6 9.5 6-3.5 6-9.5 6-9.5-6-9.5-6Z" />
            <circle cx="12" cy="12" r="2.5" />
          </svg>

          <!-- Eye off -->
          <svg
            v-else
            viewBox="0 0 24 24"
            fill="none"
            class="h-4 w-4"
            stroke="currentColor"
            stroke-width="1.8"
          >
            <path d="M3 3l18 18" />
            <path d="M10.6 6.2A10.7 10.7 0 0 1 12 6c6 0 9.5 6 9.5 6a17.5 17.5 0 0 1-3.2 3.8" />
            <path d="M6.7 6.7C4 8.2 2.5 12 2.5 12s3.5 6 9.5 6c1.5 0 2.8-.3 4-.8" />
            <path d="M9.9 9.9a3 3 0 0 0 4.2 4.2" />
          </svg>
        </button>
      </div>
    </div>

    <p v-if="pasteError" class="mt-2 text-xs text-red-600 dark:text-red-400">
      Unable to access the clipboard. Please paste manually.
    </p>
  </div>
</template>
