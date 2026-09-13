<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useSetupStore } from '../stores/setup'
import { testJellyfinConnection } from '../api/settings.ts'
import PasswordInput from '../components/inputs/PasswordInput.vue'

const router = useRouter()
const setup = useSetupStore()

const jellyfinUrl = ref('')
const jellyfinApiKey = ref('')
const adminPassword = ref('')
const confirmPassword = ref('')

const error = ref('')
const message = ref('')
const loading = ref(false)
const testing = ref(false)

async function testConnection() {
  testing.value = true
  message.value = ''
  error.value = ''

  try {
    const result = await testJellyfinConnection(jellyfinUrl.value, jellyfinApiKey.value)

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

const submitSetup = async () => {
  error.value = ''
  message.value = ''

  if (adminPassword.value !== confirmPassword.value) {
    error.value = 'Administrator passwords do not match.'
    return
  }

  if (adminPassword.value.length < 8) {
    error.value = 'Administrator password must be at least 8 characters.'
    return
  }

  loading.value = true

  try {
    const response = await fetch('/api/setup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify({
        jellyfin_url: jellyfinUrl.value,
        jellyfin_api_key: jellyfinApiKey.value,
        admin_password: adminPassword.value,
      }),
    })

    const data = await response.json()

    if (!response.ok) {
      error.value = data.detail ?? 'Unable to complete setup.'
      return
    }

    setup.completeSetup()

    await router.push('/')
  } catch {
    error.value = 'Unable to connect to Progressarr.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div
    class="min-h-screen bg-zinc-50 px-6 py-12 text-zinc-900 transition-colors duration-200 dark:bg-[#101010] dark:text-white lg:px-8"
  >
    <div class="mx-auto w-full max-w-2xl">
      <!-- Header -->
      <div class="mb-10">
        <div
          class="mb-5 flex h-10 w-10 items-center justify-center rounded-xl bg-linear-to-br from-[#aa5cc3] to-[#00a4dc] shadow-lg shadow-[#00a4dc]/10"
        >
          <svg viewBox="0 0 24 24" fill="none" class="h-6 w-6 text-white">
            <path
              d="M5 19V5M5 19H19M9 15L12 11L15 14L20 7"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </div>

        <p class="mb-2 text-sm font-medium uppercase tracking-widest text-[#00a4dc]">
          Initial setup
        </p>

        <h1 class="text-3xl font-semibold tracking-tight text-zinc-900 dark:text-white sm:text-4xl">
          Welcome to Progressarr
        </h1>

        <p class="mt-3 max-w-xl text-sm leading-6 text-zinc-600 dark:text-zinc-400">
          Before you can use Progressarr, you need to connect it to Jellyfin and create a local
          administrator password. These two settings serve different purposes and are explained
          below.
        </p>
      </div>

      <!-- Setup card -->
      <form
        class="overflow-hidden rounded-xl border border-zinc-200 bg-white transition-colors duration-200 dark:border-zinc-800 dark:bg-zinc-900"
        @submit.prevent="submitSetup"
      >
        <!-- Jellyfin connection -->
        <div class="border-b border-zinc-200 px-6 py-5 dark:border-zinc-800">
          <h2 class="font-medium text-zinc-900 dark:text-white">Jellyfin connection</h2>

          <p class="mt-1 text-sm leading-5 text-zinc-500">
            Progressarr uses Jellyfin as its primary user authentication system. Your normal
            Progressarr login uses the same username and password as your Jellyfin account.
          </p>
        </div>

        <div class="space-y-6 p-6">
          <!-- Jellyfin URL -->
          <div>
            <label
              for="jellyfin-url"
              class="mb-2 block text-sm font-medium text-zinc-700 dark:text-zinc-300"
            >
              Jellyfin URL
            </label>

            <input
              id="jellyfin-url"
              v-model="jellyfinUrl"
              type="url"
              required
              placeholder="http://jellyfin:8096"
              :disabled="loading || testing"
              class="w-full rounded-lg border border-zinc-300 bg-white px-3 py-2.5 text-zinc-900 outline-none transition placeholder:text-zinc-400 focus:border-zinc-400 dark:border-zinc-700 dark:bg-zinc-950 dark:text-white dark:placeholder:text-zinc-600 dark:focus:border-zinc-500 disabled:cursor-not-allowed disabled:opacity-50"
            />

            <p class="mt-2 text-xs leading-5 text-zinc-500">
              The URL Progressarr uses to communicate with your Jellyfin server. This should be
              reachable from the Progressarr server.
            </p>
          </div>

          <!-- Jellyfin API key -->
          <div>
            <label
              for="jellyfin-api-key"
              class="mb-2 block text-sm font-medium text-zinc-700 dark:text-zinc-300"
            >
              Jellyfin API Key
            </label>

            <PasswordInput
              id="jellyfin-api-key"
              v-model="jellyfinApiKey"
              required
              autocomplete="off"
              placeholder="Enter your Jellyfin API key"
              :disabled="loading || testing"
            />

            <p class="mt-2 text-xs leading-5 text-zinc-500">
              Progressarr uses this API key to communicate with Jellyfin. It is separate from your
              Jellyfin account password.
            </p>
          </div>

          <!-- Connection result -->
          <div
            v-if="message"
            class="rounded-lg border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-700 dark:border-emerald-900/50 dark:bg-emerald-950/30 dark:text-emerald-400"
          >
            {{ message }}
          </div>

          <div
            v-if="error"
            class="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 dark:border-red-900/50 dark:bg-red-950/30 dark:text-red-400"
          >
            {{ error }}
          </div>

          <!-- Jellyfin authentication explanation -->
          <div
            class="rounded-lg border border-zinc-200 bg-zinc-50 px-4 py-4 dark:border-zinc-800 dark:bg-zinc-950/50"
          >
            <div class="flex gap-3">
              <svg viewBox="0 0 24 24" fill="none" class="mt-0.5 h-5 w-5 shrink-0 text-[#00a4dc]">
                <path
                  d="M12 8V12M12 16H12.01M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                />
              </svg>

              <div>
                <p class="text-sm font-medium text-zinc-800 dark:text-zinc-300">
                  How normal login works
                </p>

                <p class="mt-1 text-xs leading-5 text-zinc-500">
                  Once setup is complete, users sign in to Progressarr using their Jellyfin username
                  and password. Progressarr checks those credentials with Jellyfin and uses the
                  account's Jellyfin permissions to determine access.
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Administrator account -->
        <div class="border-t border-zinc-200 dark:border-zinc-800">
          <div class="border-b border-zinc-200 px-6 py-5 dark:border-zinc-800">
            <h2 class="font-medium text-zinc-900 dark:text-white">Progressarr administrator</h2>

            <p class="mt-1 text-sm leading-5 text-zinc-500">
              Create a separate local administrator password for Progressarr.
            </p>
          </div>

          <div class="space-y-6 p-6">
            <!-- Explanation -->
            <div class="rounded-lg border border-[#aa5cc3]/20 bg-[#aa5cc3]/5 px-4 py-4">
              <div class="flex gap-3">
                <svg viewBox="0 0 24 24" fill="none" class="mt-0.5 h-5 w-5 shrink-0 text-[#aa5cc3]">
                  <path
                    d="M12 15C13.6569 15 15 13.6569 15 12C15 10.3431 13.6569 9 12 9C10.3431 9 9 10.3431 9 12C9 13.6569 10.3431 15 12 15Z"
                    stroke="currentColor"
                    stroke-width="2"
                  />
                  <path
                    d="M19.4 15C19.2669 15.3016 19.0998 15.5866 18.9 15.85L20 17.5L17.5 20L15.85 18.9C15.5866 19.0998 15.3016 19.2669 15 19.4C14.6984 19.5331 14.3822 19.6332 14.05 19.7L13.75 21.75H10.25L9.95 19.7C9.61777 19.6332 9.30161 19.5331 9 19.4C8.69839 19.2669 8.41343 19.0998 8.15 18.9L6.5 20L4 17.5L5.1 15.85C4.9002 15.5866 4.73309 15.3016 4.6 15C4.46691 14.6984 4.36677 14.3822 4.3 14.05L2.25 13.75V10.25L4.3 9.95C4.36677 9.61777 4.46691 9.3016 4.6 9C4.73309 8.69839 4.9002 8.41343 5.1 8.15L4 6.5L6.5 4L8.15 5.1C8.41343 4.9002 8.69839 4.73309 9 4.6C9.30161 4.46691 9.61777 4.46691 9.95 4.3L10.25 2.25H13.75L14.05 4.3C14.3822 4.36691 14.6984 4.46691 15 4.6C15.3016 4.73309 15.5866 4.9002 15.85 5.1L17.5 4L20 6.5L18.9 8.15C19.0998 8.41343 19.2669 8.69839 19.4 9C19.5331 9.30161 19.6332 9.61777 19.7 9.95L21.75 10.25V13.75L19.7 14.05C19.6331 14.3822 19.5331 14.6984 19.4 15Z"
                    stroke="currentColor"
                    stroke-width="1.5"
                    stroke-linejoin="round"
                  />
                </svg>

                <div>
                  <p class="text-sm font-medium text-zinc-800 dark:text-zinc-300">
                    Why does Progressarr need its own administrator password?
                  </p>

                  <p class="mt-1 text-xs leading-5 text-zinc-500">
                    This password belongs to Progressarr, not Jellyfin. It provides a local
                    administrator account that can be used for administrative or recovery access if
                    Jellyfin authentication is unavailable.
                  </p>

                  <p class="mt-2 text-xs leading-5 text-zinc-500">
                    You should choose a password you can keep separate from your Jellyfin password.
                    It will not change or affect your Jellyfin account.
                  </p>
                </div>
              </div>
            </div>

            <!-- Administrator password -->
            <div>
              <label
                for="admin-password"
                class="mb-2 block text-sm font-medium text-zinc-700 dark:text-zinc-300"
              >
                Administrator Password
              </label>

              <PasswordInput
                id="admin-password"
                v-model="adminPassword"
                required
                :minlength="8"
                autocomplete="new-password"
                placeholder="At least 8 characters"
                :disabled="loading || testing"
              />

              <p class="mt-2 text-xs leading-5 text-zinc-500">
                This is your Progressarr administrator password. It is not your Jellyfin password.
              </p>
            </div>

            <!-- Confirm password -->
            <div>
              <label
                for="confirm-password"
                class="mb-2 block text-sm font-medium text-zinc-700 dark:text-zinc-300"
              >
                Confirm Password
              </label>

              <PasswordInput
                id="confirm-password"
                v-model="confirmPassword"
                required
                :minlength="8"
                autocomplete="new-password"
                placeholder="Re-enter your password"
                :disabled="loading || testing"
              />
            </div>
          </div>
        </div>

        <!-- Final explanation -->
        <div
          class="border-t border-zinc-200 bg-zinc-50 px-6 py-5 dark:border-zinc-800 dark:bg-zinc-950/30"
        >
          <p class="text-xs leading-5 text-zinc-500">
            <span class="font-medium text-zinc-700 dark:text-zinc-400"> In short: </span>
            Jellyfin handles normal user authentication, while the local Progressarr administrator
            account provides a separate way to manage and recover the application.
          </p>
        </div>

        <!-- Actions -->
        <div
          class="flex items-center justify-end gap-3 border-t border-zinc-200 px-6 py-4 dark:border-zinc-800"
        >
          <button
            type="button"
            :disabled="loading || testing || !jellyfinUrl.trim() || !jellyfinApiKey.trim()"
            class="rounded-lg border border-zinc-300 px-4 py-2.5 text-sm font-medium text-zinc-700 transition hover:bg-zinc-100 hover:text-zinc-900 dark:border-zinc-700 dark:text-zinc-300 dark:hover:bg-zinc-800 dark:hover:text-white disabled:cursor-not-allowed disabled:opacity-50"
            @click="testConnection"
          >
            {{ testing ? 'Testing...' : 'Test Connection' }}
          </button>

          <button
            type="submit"
            :disabled="loading || testing"
            class="rounded-lg bg-zinc-900 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-zinc-800 dark:bg-white dark:text-zinc-900 dark:hover:bg-zinc-200 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {{ loading ? 'Setting up Progressarr...' : 'Complete Setup' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
