import axios from 'axios'

import { useAuthStore } from '../stores/auth'
import { pinia } from '../stores'

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
})

api.interceptors.request.use((config) => {
  const authStore = useAuthStore(pinia)
  if (authStore.user?.id) {
    config.headers = config.headers ?? {}
    config.headers['X-User-Id'] = String(authStore.user.id)
  }
  return config
})

export default api
