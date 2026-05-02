<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useInventoryStore } from '../stores/inventory'
import AppIcon from './AppIcon.vue'
import Avatar from './ui/Avatar.vue'
import Button from './ui/Button.vue'

const store = useInventoryStore()
const router = useRouter()
const route = useRoute()

const userMenu = ref(false)
const mobileOpen = ref(false)
const dark = ref(document.documentElement.classList.contains('dark'))

function toggleDark() {
  dark.value = !dark.value
  document.documentElement.classList.toggle('dark', dark.value)
}

const links = computed(() => {
  const base = [
    { name: 'dashboard',    label: 'Genel Bakış',         icon: 'Home' },
    { name: 'equipment',    label: 'Malzeme Kataloğu',    icon: 'Box' },
    { name: 'my-inventory', label: 'Üzerimdeki Malzeme',  icon: 'Backpack' },
  ]
  if (store.isManager) base.push({ name: 'manager', label: 'Yönetici Paneli', icon: 'Shield' })
  return base
})

function navigate(name) {
  router.push({ name })
  mobileOpen.value = false
}

function switchUser(id) {
  store.setUser(id)
  userMenu.value = false
}
</script>

<template>
  <nav class="sticky top-0 z-30 bg-surface-light/90 dark:bg-surface-dark/90 backdrop-blur-md border-b border-slate-200 dark:border-slate-800">
    <div class="max-w-7xl mx-auto px-4 md:px-8">
      <div class="flex items-center justify-between h-16">
        <!-- Brand -->
        <button @click="navigate('dashboard')" class="flex items-center gap-2.5 group" aria-label="Ana sayfaya git">
          <div class="w-9 h-9 rounded-alpine bg-gradient-to-br from-brand to-brand-dark flex items-center justify-center text-white shadow-alpine">
            <AppIcon name="Mountain" :size="20" :stroke="2" />
          </div>
          <div class="hidden sm:block text-left leading-tight">
            <div class="font-bold text-sm text-slate-900 dark:text-slate-100">Alpin</div>
            <div class="text-[11px] text-slate-500 dark:text-slate-400 -mt-0.5">Malzeme Takip</div>
          </div>
        </button>

        <!-- Desktop nav -->
        <div class="hidden md:flex items-center gap-1">
          <button
            v-for="l in links"
            :key="l.name"
            @click="navigate(l.name)"
            :aria-current="route.name === l.name ? 'page' : undefined"
            :class="[
              'inline-flex items-center gap-2 h-11 px-3.5 rounded-alpine text-sm font-medium transition-colors',
              route.name === l.name
                ? 'bg-brand-soft text-brand-dark dark:bg-brand/20 dark:text-brand-light'
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100 dark:text-slate-400 dark:hover:text-slate-100 dark:hover:bg-slate-800',
            ]"
          >
            <AppIcon :name="l.icon" :size="18" />
            {{ l.label }}
          </button>
        </div>

        <!-- Right cluster -->
        <div class="flex items-center gap-2">
          <!-- Dark mode toggle -->
          <button
            @click="toggleDark"
            class="w-11 h-11 inline-flex items-center justify-center rounded-alpine text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
            aria-label="Tema değiştir"
          >
            <AppIcon :name="dark ? 'Sun' : 'Moon'" :size="18" />
          </button>

          <!-- User switcher -->
          <div class="relative">
            <button
              @click="userMenu = !userMenu"
              class="flex items-center gap-2 h-11 pl-1.5 pr-3 rounded-alpine hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
              aria-haspopup="menu"
              :aria-expanded="userMenu"
            >
              <Avatar :user="store.currentUser" :size="32" />
              <div class="hidden sm:block text-left leading-tight">
                <div class="text-sm font-semibold text-slate-900 dark:text-slate-100">{{ store.currentUser?.ad }}</div>
                <div class="text-[11px] text-slate-500 dark:text-slate-400 -mt-0.5 flex items-center gap-1">
                  <template v-if="store.isManager">
                    <AppIcon name="Shield" :size="10" /> Yönetici
                  </template>
                  <template v-else>Üye · {{ store.currentUser?.id }}</template>
                </div>
              </div>
              <AppIcon name="ChevronDown" :size="14" class="text-slate-400" />
            </button>

            <template v-if="userMenu">
              <div class="fixed inset-0 z-40" @click="userMenu = false" />
              <div
                class="absolute right-0 mt-2 w-72 rounded-alpine bg-surface-light dark:bg-surface-dark border border-slate-200 dark:border-slate-700 shadow-alpine-lg z-50 anim-scale overflow-hidden"
                role="menu"
              >
                <div class="px-4 py-2.5 border-b border-slate-200 dark:border-slate-700">
                  <span class="text-[11px] uppercase tracking-wider font-semibold text-slate-500 dark:text-slate-400">Aktif Kullanıcı (test)</span>
                </div>
                <div class="max-h-80 overflow-y-auto py-1">
                  <button
                    v-for="u in store.users"
                    :key="u.id"
                    @click="switchUser(u.id)"
                    :class="[
                      'w-full flex items-center gap-3 px-3 py-2.5 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors',
                      u.id === store.currentUserId ? 'bg-brand-soft/40 dark:bg-brand/10' : '',
                    ]"
                  >
                    <Avatar :user="u" :size="36" />
                    <div class="flex-1 text-left">
                      <div class="text-sm font-semibold text-slate-900 dark:text-slate-100 flex items-center gap-2">
                        {{ u.ad }}
                        <span v-if="u.rol === 'yonetici'" class="text-[10px] uppercase tracking-wider font-bold bg-brand text-white px-1.5 py-0.5 rounded">Yön.</span>
                      </div>
                      <div class="text-xs text-slate-500 dark:text-slate-400">{{ u.id }}</div>
                    </div>
                    <AppIcon v-if="u.id === store.currentUserId" name="Check" :size="16" class="text-brand" />
                  </button>
                </div>
                <div class="px-4 py-2.5 border-t border-slate-200 dark:border-slate-700 text-[11px] text-slate-500 dark:text-slate-400">
                  RBAC testi için kullanıcı değiştirin
                </div>
              </div>
            </template>
          </div>

          <!-- Mobile menu button -->
          <button
            @click="mobileOpen = !mobileOpen"
            class="md:hidden w-11 h-11 inline-flex items-center justify-center rounded-alpine hover:bg-slate-100 dark:hover:bg-slate-800"
            aria-label="Menüyü aç"
          >
            <AppIcon name="Menu" :size="20" />
          </button>
        </div>
      </div>

      <!-- Mobile nav -->
      <div v-if="mobileOpen" class="md:hidden pb-3 flex flex-col gap-1 anim-fade">
        <button
          v-for="l in links"
          :key="l.name"
          @click="navigate(l.name)"
          :class="[
            'flex items-center gap-3 h-12 px-3 rounded-alpine text-sm font-medium',
            route.name === l.name
              ? 'bg-brand-soft text-brand-dark dark:bg-brand/20 dark:text-brand-light'
              : 'text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800',
          ]"
        >
          <AppIcon :name="l.icon" :size="18" />
          {{ l.label }}
        </button>
      </div>
    </div>
  </nav>
</template>
