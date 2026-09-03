import { createRouter, createWebHistory } from 'vue-router'

import DashboardView from '../views/DashboardView.vue'
import LoginView from '../views/LoginView.vue'
import SettingsView from '../views/settings/SettingsView.vue'
import RadarrSettingsView from '../views/settings/RadarrSettingsView.vue'
import SonarrSettingsView from '../views/settings/SonarrSettingsView.vue'
import SeerrSettings from '../views/settings/SeerrSettingsView.vue'
import JellyfinSettingsView from '../views/settings/JellyfinSettingsView.vue'

import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory(),

  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: DashboardView,
    },

    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },

    {
      path: '/settings',
      name: 'settings',
      component: SettingsView,
      meta: {
        requiresAuth: true,
      },
    },

    {
      path: '/settings/radarr',
      name: 'settings-radarr',
      component: RadarrSettingsView,
      meta: {
        requiresAuth: true,
      },
    },

    {
      path: '/settings/sonarr',
      name: 'settings-sonarr',
      component: SonarrSettingsView,
      meta: {
        requiresAuth: true,
      },
    },

    {
      path: '/settings/seerr',
      component: SeerrSettings,
      meta: {
        requiresAuth: true,
      },
    },

    {
      path: '/settings/jellyfin',
      name: 'settings-jellyfin',
      component: JellyfinSettingsView,
      meta: {
        requiresAuth: true,
      },
    },
  ],
})

router.beforeEach(async (to) => {
  const auth = useAuthStore()

  if (!auth.isAuthenticated && !auth.loading) {
    await auth.checkSession()
  }

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return {
      name: 'login',
    }
  }

  if (to.name === 'login' && auth.isAuthenticated) {
    return {
      name: 'dashboard',
    }
  }
})

export default router
