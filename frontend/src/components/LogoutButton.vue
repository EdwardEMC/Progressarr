<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()

const auth = useAuthStore()

async function logout(): Promise<void> {
  await auth.logout()
  await router.push({ name: 'login' })
}
</script>

<template>
  <button
    type="button"
    class="cursor-pointer flex h-9 w-9 items-center justify-center rounded-lg text-zinc-500 transition hover:bg-red-500/10 hover:text-red-600 dark:text-zinc-400 dark:hover:text-red-300"
    title="Log out"
    aria-label="Log out"
    @click="logout"
  >
    <svg viewBox="0 0 24 24" fill="none" class="h-5 w-5">
      <path
        d="M10 5H6.5A1.5 1.5 0 0 0 5 6.5V17.5A1.5 1.5 0 0 0 6.5 19H10"
        stroke="currentColor"
        stroke-width="1.8"
        stroke-linecap="round"
      />

      <path
        d="M14 8L18 12L14 16"
        stroke="currentColor"
        stroke-width="1.8"
        stroke-linecap="round"
        stroke-linejoin="round"
      />

      <path d="M18 12H10" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
    </svg>
  </button>
</template>
