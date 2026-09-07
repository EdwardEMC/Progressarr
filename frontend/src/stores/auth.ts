import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

interface User {
  id: number
  username: string
  is_admin: boolean
}

type AuthType = 'jellyfin' | 'local_admin' | null

interface SessionResponse {
  auth_type: AuthType
  user: User | null
}

export const useAuthStore = defineStore('auth', () => {
  const initialized = ref(false)
  const user = ref<User | null>(null)
  const authType = ref<AuthType>(null)
  const loading = ref(false)

  const isAuthenticated = computed(() => authType.value !== null)

  const isAdmin = computed(() => {
    if (authType.value === 'local_admin') {
      return true
    }

    return user.value?.is_admin === true
  })

  async function checkSession(): Promise<void> {
    if (initialized.value) {
      return
    }

    loading.value = true

    try {
      const response = await fetch('/api/auth/me', {
        credentials: 'include',
      })

      if (!response.ok) {
        user.value = null
        authType.value = null
        return
      }

      const data: SessionResponse = await response.json()

      authType.value = data.auth_type
      user.value = data.user
    } catch {
      user.value = null
      authType.value = null
    } finally {
      initialized.value = true
      loading.value = false
    }
  }

  async function login(username: string, password: string): Promise<void> {
    loading.value = true

    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',

        headers: {
          'Content-Type': 'application/json',
        },

        credentials: 'include',

        body: JSON.stringify({
          username,
          password,
        }),
      })

      if (!response.ok) {
        throw new Error('Invalid username or password.')
      }

      const data = await response.json()

      user.value = data.user
      authType.value = 'jellyfin'
    } finally {
      loading.value = false
    }
  }

  async function adminLogin(password: string): Promise<void> {
    loading.value = true

    try {
      const response = await fetch('/api/auth/admin-login', {
        method: 'POST',

        headers: {
          'Content-Type': 'application/json',
        },

        credentials: 'include',

        body: JSON.stringify({
          password,
        }),
      })

      if (!response.ok) {
        const data = await response.json().catch(() => null)

        throw new Error(data?.detail ?? 'Administrator login failed.')
      }

      user.value = null
      authType.value = 'local_admin'
    } finally {
      loading.value = false
    }
  }

  async function logout(): Promise<void> {
    await fetch('/api/auth/logout', {
      method: 'POST',
      credentials: 'include',
    })

    user.value = null
    authType.value = null
  }

  return {
    user,
    authType,
    loading,
    initialized,
    isAuthenticated,
    isAdmin,
    checkSession,
    login,
    adminLogin,
    logout,
  }
})
