import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

export type Theme = 'dark' | 'light' | 'system'

export const useThemeStore = defineStore('theme', () => {
  const storedTheme = localStorage.getItem('progressarr-theme')

  const theme = ref<Theme>(
    storedTheme === 'light' || storedTheme === 'dark' || storedTheme === 'system'
      ? storedTheme
      : 'dark',
  )
  const systemPrefersDark = ref(window.matchMedia('(prefers-color-scheme: dark)').matches)

  const isDark = computed(() => {
    if (theme.value === 'system') {
      return systemPrefersDark.value
    }

    return theme.value === 'dark'
  })

  function applyTheme(): void {
    document.documentElement.classList.toggle('dark', isDark.value)
    document.documentElement.style.colorScheme = isDark.value ? 'dark' : 'light'
  }

  function setTheme(newTheme: Theme): void {
    theme.value = newTheme

    localStorage.setItem('progressarr-theme', newTheme)

    applyTheme()
  }

  function toggleTheme(): void {
    setTheme(isDark.value ? 'light' : 'dark')
  }

  function initialise(): void {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')

    systemPrefersDark.value = mediaQuery.matches

    mediaQuery.addEventListener('change', (event) => {
      systemPrefersDark.value = event.matches

      if (theme.value === 'system') {
        applyTheme()
      }
    })

    applyTheme()
  }

  return {
    theme,
    isDark,
    setTheme,
    toggleTheme,
    initialise,
  }
})
