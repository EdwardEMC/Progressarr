<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import { useAuthStore } from '../stores/auth'


const router = useRouter()
const auth = useAuthStore()

const username = ref('')
const password = ref('')
const error = ref('')


async function handleLogin() {
  error.value = ''

  if (!username.value || !password.value) {
    error.value = 'Please enter your username and password.'
    return
  }

  try {
    await auth.login(
      username.value,
      password.value,
    )

    await router.push({
      name: 'dashboard',
    })
  } catch {
    error.value = 'Invalid username or password.'
  }
}
</script>


<template>
  <main
    class="min-h-screen flex items-center justify-center bg-zinc-950 px-4"
  >
    <div class="w-full max-w-md">

      <div class="mb-8 text-center">
        <h1 class="text-3xl font-semibold text-white">
          Progressarr
        </h1>

        <p class="mt-2 text-sm text-zinc-400">
          Sign in to manage your configuration
        </p>
      </div>


      <form
        class="rounded-xl border border-zinc-800 bg-zinc-900 p-6 shadow-xl"
        @submit.prevent="handleLogin"
      >

        <h2 class="text-xl font-medium text-white">
          Sign in
        </h2>


        <div class="mt-6 space-y-5">

          <div>
            <label
              for="username"
              class="mb-2 block text-sm font-medium text-zinc-300"
            >
              Username
            </label>

            <input
              id="username"
              v-model="username"
              type="text"
              autocomplete="username"
              class="w-full rounded-lg border border-zinc-700 bg-zinc-950 px-3 py-2.5 text-white outline-none transition focus:border-zinc-500"
              :disabled="auth.loading"
            />
          </div>


          <div>
            <label
              for="password"
              class="mb-2 block text-sm font-medium text-zinc-300"
            >
              Password
            </label>

            <input
              id="password"
              v-model="password"
              type="password"
              autocomplete="current-password"
              class="w-full rounded-lg border border-zinc-700 bg-zinc-950 px-3 py-2.5 text-white outline-none transition focus:border-zinc-500"
              :disabled="auth.loading"
            />
          </div>


          <div
            v-if="error"
            class="rounded-lg border border-red-900/50 bg-red-950/30 px-3 py-2.5 text-sm text-red-400"
          >
            {{ error }}
          </div>


          <button
            type="submit"
            class="w-full rounded-lg bg-white px-4 py-2.5 font-medium text-zinc-900 transition hover:bg-zinc-200 disabled:cursor-not-allowed disabled:opacity-50"
            :disabled="auth.loading"
          >
            {{ auth.loading ? 'Signing in...' : 'Sign in' }}
          </button>

        </div>
      </form>

    </div>
  </main>
</template>
