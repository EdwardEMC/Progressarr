<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import { useAuthStore } from '../stores/auth'

import PasswordInput from '../components/inputs/PasswordInput.vue'

const router = useRouter()
const auth = useAuthStore()

const loginType = ref<'jellyfin' | 'admin'>('jellyfin')

const username = ref('')
const password = ref('')
const error = ref('')

async function handleLogin() {
  error.value = ''

  if (!password.value) {
    error.value =
      loginType.value === 'jellyfin'
        ? 'Please enter your username and password.'
        : 'Please enter your administrator password.'

    return
  }

  if (loginType.value === 'jellyfin' && !username.value) {
    error.value = 'Please enter your username and password.'
    return
  }

  try {
    if (loginType.value === 'jellyfin') {
      await auth.login(username.value, password.value)
    } else {
      await auth.adminLogin(password.value)
    }

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
    class="flex min-h-screen items-center justify-center bg-zinc-50 px-4 transition-colors duration-200 dark:bg-[#101010]"
  >
    <div class="w-full max-w-md">
      <div class="mb-8 text-center">
        <h1 class="text-3xl font-semibold text-zinc-900 dark:text-white">Progressarr</h1>

        <p class="mt-2 text-sm text-zinc-500">Sign in to manage your configuration</p>
      </div>

      <form
        class="overflow-hidden rounded-xl border border-zinc-200 bg-white shadow-xl transition-colors duration-200 dark:border-zinc-800 dark:bg-zinc-900"
        @submit.prevent="handleLogin"
      >
        <!-- Login type -->
        <div class="border-b border-zinc-200 p-2 dark:border-zinc-800">
          <div class="grid grid-cols-2 gap-1 rounded-lg bg-zinc-100 p-1 dark:bg-zinc-950">
            <button
              type="button"
              :class="[
                'rounded-md px-3 py-2 text-sm font-medium transition',
                loginType === 'jellyfin'
                  ? 'bg-white text-zinc-900 shadow-sm dark:bg-zinc-800 dark:text-white'
                  : 'text-zinc-500 hover:text-zinc-800 dark:text-zinc-500 dark:hover:text-zinc-300',
              ]"
              :disabled="auth.loading"
              @click="((loginType = 'jellyfin'), (error = ''))"
            >
              Jellyfin
            </button>

            <button
              type="button"
              :class="[
                'rounded-md px-3 py-2 text-sm font-medium transition',
                loginType === 'admin'
                  ? 'bg-white text-zinc-900 shadow-sm dark:bg-zinc-800 dark:text-white'
                  : 'text-zinc-500 hover:text-zinc-800 dark:text-zinc-500 dark:hover:text-zinc-300',
              ]"
              :disabled="auth.loading"
              @click="((loginType = 'admin'), (error = ''))"
            >
              Administrator
            </button>
          </div>
        </div>

        <div class="p-6">
          <!-- Jellyfin login -->
          <template v-if="loginType === 'jellyfin'">
            <div>
              <h2 class="text-xl font-medium text-zinc-900 dark:text-white">
                Sign in with Jellyfin
              </h2>

              <p class="mt-1 text-sm leading-5 text-zinc-500">
                Use your Jellyfin username and password to sign in to Progressarr.
              </p>
            </div>

            <div class="mt-6 space-y-5">
              <div>
                <label
                  for="username"
                  class="mb-2 block text-sm font-medium text-zinc-700 dark:text-zinc-300"
                >
                  Username
                </label>

                <input
                  id="username"
                  v-model="username"
                  type="text"
                  autocomplete="username"
                  class="w-full rounded-lg border border-zinc-300 bg-white px-3 py-2.5 text-zinc-900 outline-none transition placeholder:text-zinc-400 focus:border-zinc-400 dark:border-zinc-700 dark:bg-zinc-950 dark:text-white dark:placeholder:text-zinc-600 dark:focus:border-zinc-500"
                  :disabled="auth.loading"
                />
              </div>

              <div>
                <label
                  for="jellyfin-password"
                  class="mb-2 block text-sm font-medium text-zinc-700 dark:text-zinc-300"
                >
                  Password
                </label>

                <PasswordInput
                  id="jellyfin-password"
                  v-model="password"
                  required
                  autocomplete="current-password"
                  :disabled="auth.loading"
                />
              </div>

              <div
                class="rounded-lg border border-zinc-200 bg-zinc-50 px-4 py-3 dark:border-zinc-800 dark:bg-zinc-950/50"
              >
                <p class="text-xs leading-5 text-zinc-500">
                  Your Jellyfin account controls your normal Progressarr access. Progressarr does
                  not store your Jellyfin password.
                </p>
              </div>
            </div>
          </template>

          <!-- Progressarr administrator login -->
          <template v-else>
            <div>
              <h2 class="text-xl font-medium text-zinc-900 dark:text-white">
                Progressarr Administrator
              </h2>

              <p class="mt-1 text-sm leading-5 text-zinc-500">
                Use the administrator password you created during the initial Progressarr setup.
              </p>
            </div>

            <div class="mt-6 space-y-5">
              <div>
                <label
                  for="admin-password"
                  class="mb-2 block text-sm font-medium text-zinc-700 dark:text-zinc-300"
                >
                  Administrator Password
                </label>

                <PasswordInput
                  id="admin-password"
                  v-model="password"
                  required
                  autocomplete="current-password"
                  :disabled="auth.loading"
                />

                <p class="mt-2 text-xs leading-5 text-zinc-500">
                  This is your Progressarr password, not your Jellyfin password.
                </p>
              </div>

              <div class="rounded-lg border border-[#aa5cc3]/20 bg-[#aa5cc3]/5 px-4 py-3">
                <p class="text-xs leading-5 text-zinc-600 dark:text-zinc-400">
                  The Progressarr administrator account provides local administrative access and can
                  be used when Jellyfin authentication is unavailable.
                </p>
              </div>
            </div>
          </template>

          <!-- Error -->
          <div
            v-if="error"
            class="mt-5 rounded-lg border border-red-200 bg-red-50 px-3 py-2.5 text-sm text-red-700 dark:border-red-900/50 dark:bg-red-950/30 dark:text-red-400"
          >
            {{ error }}
          </div>

          <!-- Submit -->
          <button
            type="submit"
            class="mt-6 w-full rounded-lg bg-zinc-900 px-4 py-2.5 font-medium text-white transition hover:bg-zinc-800 dark:bg-white dark:text-zinc-900 dark:hover:bg-zinc-200 disabled:cursor-not-allowed disabled:opacity-50"
            :disabled="auth.loading"
          >
            {{ auth.loading ? 'Signing in...' : 'Sign in' }}
          </button>
        </div>
      </form>

      <p class="mt-5 text-center text-xs text-zinc-500 dark:text-zinc-600">
        {{
          loginType === 'jellyfin'
            ? 'Use your Jellyfin account for normal access.'
            : 'Use the Progressarr administrator password created during setup.'
        }}
      </p>
    </div>
  </main>
</template>
