import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import './style.css'
import { useThemeStore } from './stores/theme.ts'

const app = createApp(App)

const pinia = createPinia()

app.use(pinia)
app.use(router)

const theme = useThemeStore(pinia)

theme.initialise()

app.mount('#app')
