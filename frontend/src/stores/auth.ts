import { computed, ref } from 'vue'
import { defineStore } from 'pinia'


interface User {
  id: number
  username: string
  is_admin: boolean
}


export const useAuthStore = defineStore(
  'auth',
  () => {
    const initialized = ref(false)
    const user = ref<User | null>(null)
    const loading = ref(false)

    const isAuthenticated = computed(
      () => user.value !== null,
    )

    const isAdmin = computed(
      () => user.value?.is_admin === true,
    )


    async function checkSession(): Promise<void> {
      if (initialized.value) {
        return
      }

      loading.value = true

      try {
        const response = await fetch(
          '/api/auth/me',
          {
            credentials: 'include',
          },
        )

        if (!response.ok) {
          user.value = null
          return
        }

        user.value = await response.json()
      } catch {
        user.value = null
      } finally {
        initialized.value = true
        loading.value = false
      }
    }


    async function login(
      username: string,
      password: string,
    ): Promise<void> {
      loading.value = true

      try {
        const response = await fetch(
          '/api/auth/login',
          {
            method: 'POST',

            headers: {
              'Content-Type': 'application/json',
            },

            credentials: 'include',

            body: JSON.stringify({
              username,
              password,
            }),
          },
        )

        if (!response.ok) {
          throw new Error(
            'Invalid username or password.',
          )
        }

        const data = await response.json()

        user.value = data.user
      } finally {
        loading.value = false
      }
    }


    async function logout(): Promise<void> {
      await fetch(
        '/api/auth/logout',
        {
          method: 'POST',
          credentials: 'include',
        },
      )

      user.value = null
    }


    return {
      user,
      loading,
      initialized,
      isAuthenticated,
      isAdmin,
      checkSession,
      login,
      logout,
    }
  },
)
