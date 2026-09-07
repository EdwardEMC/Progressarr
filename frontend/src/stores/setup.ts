import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useSetupStore = defineStore('setup', () => {
  const setupRequired = ref<boolean | null>(null)
  const loading = ref(false)

  const checkSetup = async () => {
    loading.value = true

    try {
      const response = await fetch('/api/setup/status')

      if (!response.ok) {
        throw new Error('Unable to determine setup status.')
      }

      const data: {
        setup_required: boolean
      } = await response.json()

      setupRequired.value = data.setup_required
    } finally {
      loading.value = false
    }
  }

  const completeSetup = () => {
    setupRequired.value = false
  }

  return {
    setupRequired,
    loading,
    checkSetup,
    completeSetup,
  }
})
