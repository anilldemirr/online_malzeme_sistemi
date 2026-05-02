<script setup>
import { computed } from 'vue'
import { useInventoryStore } from '../../stores/inventory'
import AppIcon from '../AppIcon.vue'

const store = useInventoryStore()
const toasts = computed(() => store.toasts)

function toneClass(tone) {
  if (tone === 'warn')  return 'bg-amber-500 text-white'
  if (tone === 'info')  return 'bg-sky-500 text-white'
  if (tone === 'error') return 'bg-rose-500 text-white'
  return 'bg-slate-900 dark:bg-slate-100 text-white dark:text-slate-900'
}

function toneIcon(tone) {
  if (tone === 'warn')  return 'AlertTriangle'
  if (tone === 'info')  return 'Bell'
  if (tone === 'error') return 'X'
  return 'CheckCircle'
}
</script>

<template>
  <div class="fixed bottom-6 right-6 z-50 flex flex-col gap-2 pointer-events-none">
    <TransitionGroup name="toast">
      <div
        v-for="t in toasts"
        :key="t.id"
        :class="[
          'anim-slide pointer-events-auto flex items-center gap-2.5 shadow-alpine-lg rounded-alpine px-4 py-3 text-sm font-medium',
          toneClass(t.tone),
        ]"
      >
        <AppIcon :name="toneIcon(t.tone)" :size="18" />
        <span>{{ t.msg }}</span>
      </div>
    </TransitionGroup>
  </div>
</template>

<style scoped>
.toast-enter-active, .toast-leave-active { transition: all .25s ease; }
.toast-enter-from { opacity: 0; transform: translateY(12px); }
.toast-leave-to { opacity: 0; transform: translateX(20px); }
</style>
