<script setup>
import { ref, computed } from 'vue'
import { useInventoryStore } from '../stores/inventory'
import AppIcon from '../components/AppIcon.vue'
import Button from '../components/ui/Button.vue'
import EquipmentCard from '../components/ui/EquipmentCard.vue'
import EmptyState from '../components/ui/EmptyState.vue'

const store = useInventoryStore()

const query = ref('')
const tip = ref('all')
const recentlyRequested = ref({})

const filtered = computed(() => {
  const q = query.value.trim().toLowerCase()
  return store.models.filter(m => {
    if (tip.value !== 'all' && m.tip !== tip.value) return false
    if (!q) return true
    return m.model_adi.toLowerCase().includes(q) || m.marka.toLowerCase().includes(q) || m.kategori.toLowerCase().includes(q)
  })
})

const myPendingByModel = computed(() => {
  const map = {}
  store.myPendingRequests.forEach(t => { map[t.model_id] = t })
  return map
})

function handleRequest(model) {
  store.requestModel(model)
  recentlyRequested.value[model.id] = Date.now()
  setTimeout(() => {
    delete recentlyRequested.value[model.id]
  }, 1800)
}

const tipOptions = [
  { id: 'all',    label: 'Tümü' },
  { id: 'teknik', label: 'Teknik Malzeme' },
  { id: 'kitap',  label: 'Yayın' },
]
</script>

<template>
  <main class="max-w-7xl mx-auto px-4 md:px-8 py-6 md:py-8">
    <header class="mb-6 anim-fade">
      <div class="flex items-baseline justify-between gap-4 flex-wrap">
        <div>
          <h1 class="text-3xl font-bold text-slate-900 dark:text-slate-50 tracking-tight">Malzeme Kataloğu</h1>
          <p class="text-sm text-slate-500 dark:text-slate-400 mt-1">Kullanılabilir model ve yayınlardan talep oluşturun.</p>
        </div>
        <div class="text-xs text-slate-500 dark:text-slate-400">
          <span class="font-semibold text-slate-700 dark:text-slate-300">{{ filtered.length }}</span> / {{ store.models.length }} model
        </div>
      </div>
    </header>

    <!-- Sticky filter bar -->
    <div class="sticky top-16 z-20 -mx-4 md:-mx-8 px-4 md:px-8 py-3 bg-background-light/80 dark:bg-background-dark/80 backdrop-blur-md border-y border-slate-200 dark:border-slate-800 mb-6">
      <div class="flex flex-col md:flex-row items-stretch md:items-center gap-3">
        <div class="relative flex-1">
          <AppIcon name="Search" :size="16" class="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            v-model="query"
            type="text"
            placeholder="Model, marka veya kategori ara…"
            class="w-full h-11 pl-10 pr-3 rounded-alpine bg-surface-light dark:bg-surface-dark border border-slate-200 dark:border-slate-700 text-sm text-slate-900 dark:text-slate-100 placeholder:text-slate-400 focus:border-brand focus:ring-2 focus:ring-brand/20 outline-none transition"
            aria-label="Ara"
          />
          <button
            v-if="query"
            @click="query = ''"
            class="absolute right-2.5 top-1/2 -translate-y-1/2 w-7 h-7 inline-flex items-center justify-center rounded-md text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800"
            aria-label="Aramayı temizle"
          >
            <AppIcon name="X" :size="14" />
          </button>
        </div>
        <div class="inline-flex p-1 rounded-alpine bg-slate-100 dark:bg-slate-800">
          <button
            v-for="t in tipOptions"
            :key="t.id"
            @click="tip = t.id"
            :class="[
              'h-9 px-3 rounded-md text-sm font-medium transition-colors',
              tip === t.id
                ? 'bg-white dark:bg-slate-700 text-slate-900 dark:text-slate-50 shadow-alpine'
                : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100',
            ]"
          >
            {{ t.label }}
          </button>
        </div>
      </div>
    </div>

    <!-- Empty state -->
    <EmptyState
      v-if="filtered.length === 0"
      icon="Box"
      title="Eşleşen malzeme bulunamadı"
      body="Farklı bir anahtar kelime veya kategori deneyin."
    >
      <template #action>
        <Button variant="secondary" @click="query = ''; tip = 'all'">Filtreleri Temizle</Button>
      </template>
    </EmptyState>

    <!-- Grid -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 md:gap-6 anim-fade">
      <EquipmentCard
        v-for="m in filtered"
        :key="m.id"
        :model="m"
        :count-available="store.availableItemsForModel(m.id).length"
      >
        <template #action>
          <Button
            v-if="recentlyRequested[m.id]"
            variant="primary"
            class="w-full !bg-emerald-500 hover:!bg-emerald-600"
            :disabled="true"
            icon="Check"
          >
            Talep alındı
          </Button>
          <Button
            v-else-if="myPendingByModel[m.id]"
            variant="secondary"
            class="w-full"
            :disabled="true"
            icon="Clock"
          >
            Beklemede
          </Button>
          <Button
            v-else-if="store.availableItemsForModel(m.id).length === 0"
            variant="outline"
            class="w-full"
            :disabled="true"
          >
            Stokta yok
          </Button>
          <Button
            v-else
            variant="primary"
            class="w-full"
            icon="Plus"
            @click="handleRequest(m)"
          >
            Talep Et
          </Button>
        </template>
      </EquipmentCard>
    </div>
  </main>
</template>
