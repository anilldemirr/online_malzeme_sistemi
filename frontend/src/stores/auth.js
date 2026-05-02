import { defineStore } from 'pinia'

const STORAGE_KEY = 'club_inventory_user'

const DEMO_USERS = {
  1: {
    id: 1,
    ad_soyad: 'Ali',
    email: 'ali@example.com',
    rol: 'member',
  },
  2: {
    id: 2,
    ad_soyad: 'Veli',
    email: 'veli@example.com',
    rol: 'manager',
  },
}

function loadStoredUser() {
  try {
    const rawValue = localStorage.getItem(STORAGE_KEY)
    return rawValue ? JSON.parse(rawValue) : null
  } catch {
    return null
  }
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: loadStoredUser(),
  }),
  getters: {
    isManager: (state) => state.user?.rol === 'manager',
  },
  actions: {
    login(userId, role) {
      const numericUserId = Number(userId)
      const demoUser = DEMO_USERS[numericUserId]

      this.user = {
        id: numericUserId,
        ad_soyad: demoUser?.ad_soyad ?? `Kullanici ${numericUserId}`,
        email: demoUser?.email ?? `user${numericUserId}@example.com`,
        rol: role,
      }
      localStorage.setItem(STORAGE_KEY, JSON.stringify(this.user))
    },
  },
})
